from fastapi import HTTPException, Request
from sqlalchemy.orm import Session
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from app.core.database import SessionLocal
from app.core.security import resolve_current_user

async def authenticate_user(request: Request):
    auth_header = request.headers.get("Authorization")
    scheme, separator, token = auth_header.partition(" ") if auth_header else ("", "", "")
    if not separator or scheme.lower() != "bearer" or not token.strip():
        raise HTTPException(
            status_code=401,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    db: Session = SessionLocal()
    try:
        request.state.user = resolve_current_user(token.strip(), db)
    finally:
        db.close()


class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, api_prefix: str = ""):
        super().__init__(app)
        self.__exact_path_rules = self.process_path_rules(
            self.__disable_auth_paths,
            api_prefix=api_prefix,
        )
        self.__prefix_path_rules = self.process_path_rules(
            self.__prefix_paths,
            api_prefix=api_prefix,
        )

        for path in self.__swagger_paths:
            self.__exact_path_rules[path] = None

    __disable_auth_paths = [
        "/auth/resend-code",
        "/auth/verify-email",
        "/auth/login",
        "/auth/register",  
        "/demo",
        "/auth/google/login",
        "/auth/google/callback",
        "/auth/facebook/login",
        "/auth/facebook/callback",
        "/payment/vnpay/return",
        "/payment/vnpay/ipn",
        "/payment/vnpay/status",
        "/payment/create-payment",
        "/products/flash-sale",
        "/health",
        "/"
    ]

    __prefix_paths = [
        ("/brands/logo/", ["GET"]),
        ("/products", ["GET"]),
        ("/brands", ["GET"]),
    ]

    __swagger_paths = ["/docs", "/redoc", "/openapi.json"]

    @staticmethod
    def process_path_rules(paths, api_prefix: str = ""):
        """
        Xử lý danh sách paths thành dictionary rules.
        Tự động thêm cả path có và không có API_PREFIX để hỗ trợ cả 2 trường hợp.
        
        Args:
            paths: List các path hoặc tuple (path, [methods])
            api_prefix: API path prefix to include in the bypass rules
        
        Returns:
            dict: {path: set(methods) hoặc None}
                - None nghĩa là bypass tất cả methods
                - set(methods) nghĩa là chỉ bypass các methods trong set
        """
        rules = {}
        for item in paths:
            if isinstance(item, str):
                # Path đơn giản: bypass tất cả methods
                # Thêm cả path có và không có prefix
                rules[item] = None  # Path gốc (không có prefix)
                if api_prefix:
                    path_with_prefix = api_prefix.rstrip("/") + item
                    rules[path_with_prefix] = None  # Path có prefix
            elif isinstance(item, tuple) and len(item) == 2:
                # Path với methods cụ thể: (path, [methods])
                path_str, method = item
                methods_set = set(method) if method else None
                # Thêm cả path có và không có prefix
                rules[path_str] = methods_set  # Path gốc (không có prefix)
                if api_prefix:
                    path_with_prefix = api_prefix.rstrip("/") + path_str
                    rules[path_with_prefix] = methods_set  # Path có prefix
        return rules

    def should_bypass_auth(self, path: str, method: str) -> bool:
        if path in self.__exact_path_rules:
            methods = self.__exact_path_rules[path]
            bypass = methods is None or method in methods
            if bypass:
                return True

        for prefix, methods in self.__prefix_path_rules.items():
            if path.rstrip("/").startswith(prefix.rstrip("/")):
                if methods is None or method in methods:
                    return True

        return False

    async def dispatch(self, request: Request, call_next):
        try:
            path = request.url.path
            method = request.method
            
            # Always bypass authentication for OPTIONS requests (CORS preflight)
            if method == "OPTIONS":
                return await call_next(request)
            
            if not self.should_bypass_auth(path, method):
                await authenticate_user(request)

            return await call_next(request)

        except HTTPException as e:
            return JSONResponse(
                status_code=e.status_code,
                content={"detail": e.detail},
                headers=e.headers,
            )
