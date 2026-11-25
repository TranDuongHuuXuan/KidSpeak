from collections.abc import Callable

from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session, joinedload

from app.config.config import settings
from app.core.database import get_db
from app.models.user import User

_bearer_scheme = HTTPBearer(auto_error=False)
def normalize_role_name(role_name: str | None) -> str | None:
    if not role_name:
        return None
    return role_name.strip().upper()


def unauthorized(detail: str = "Not authenticated") -> HTTPException:
    return HTTPException(
        status_code=401,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"},
    )


def resolve_current_user(token: str, db: Session) -> User:
    try:
        claims = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
    except JWTError as error:
        raise unauthorized("Token không hợp lệ hoặc đã hết hạn.") from error

    subject = claims.get("sub")
    if not isinstance(subject, str) or not subject.isdecimal():
        raise unauthorized("Token không chứa định danh người dùng hợp lệ.")
    if not isinstance(claims.get("exp"), (int, float)):
        raise unauthorized("Token không có thời hạn hợp lệ.")

    user = (
        db.query(User)
        .options(joinedload(User.role))
        .filter(User.id == int(subject))
        .first()
    )
    if not user:
        raise unauthorized("Tài khoản không còn tồn tại.")
    if not user.is_active:
        raise HTTPException(
            status_code=403,
            detail="Tài khoản đã bị vô hiệu hóa.",
        )
    if not user.role:
        raise HTTPException(
            status_code=403,
            detail="Tài khoản chưa được cấp quyền.",
        )
    return user


def get_current_user(
    request: Request,
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    user = getattr(request.state, "user", None)
    if user is not None:
        return user
    if not credentials or credentials.scheme.lower() != "bearer":
        raise unauthorized()
    return resolve_current_user(credentials.credentials, db)


def require_roles(*roles: str) -> Callable:
    allowed_roles = {
        normalized
        for role in roles
        if (normalized := normalize_role_name(role)) is not None
    }

    def role_dependency(
        current_user: User = Depends(get_current_user),
    ) -> User:
        current_role = normalize_role_name(
            current_user.role.name if current_user.role else None
        )
        if current_role not in allowed_roles:
            raise HTTPException(
                status_code=403,
                detail="Bạn không có quyền truy cập tài nguyên này.",
            )
        return current_user

    return role_dependency
