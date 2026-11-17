from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.logger import logger
from app.schemas.auth_schema import RegisterSchema, LoginSchema, LoginResponseSchema
from app.schemas.base_schema import DataResponse
from app.schemas.user_schema import UserSchema
from app.service.auth_service import AuthService, RegistrationConflictError

auth_router = APIRouter(prefix="/auth", tags=["Auth"])


# ─── Đăng ký ─────────────────────────────────────────────────────────────────
@auth_router.post(
    "/register",
    response_model=DataResponse[UserSchema],
    status_code=status.HTTP_201_CREATED,
    summary="Đăng ký tài khoản mới",
    description=(
        "Nhận thông tin đăng ký, kiểm tra email đã tồn tại, "
        "lưu người dùng vào database với role USER và kích hoạt tài khoản ngay lập tức."
    ),
)
async def register(
    data: RegisterSchema,
    db: Session = Depends(get_db),
):
    try:
        user = await AuthService.register_user(db, data)

        return DataResponse.custom_response(
            data=user,
            code="201",
            message="Đăng ký tài khoản thành công.",
        )

    except RegistrationConflictError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        )

    except IntegrityError as e:
        db.rollback()
        err_msg = str(e.orig).lower() if e.orig else ""
        if "email" in err_msg or "ix_users_email" in err_msg:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email này đã được đăng ký.",
            )
        logger.error("Database error while registering an account.")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Không thể tạo tài khoản lúc này. Vui lòng thử lại sau.",
        )

    except Exception:
        db.rollback()
        logger.error("Unexpected error while registering an account.")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Không thể tạo tài khoản lúc này. Vui lòng thử lại sau.",
        )

@auth_router.post(
    "/login",
    response_model=DataResponse[LoginResponseSchema],
    status_code=status.HTTP_200_OK,
)
async def login(
    data: LoginSchema,
    db: Session = Depends(get_db)
):
    try:
        result = AuthService.login_user(db, data)

        return DataResponse.custom_response(
            data=result,
            code="200",
            message="Login successfully"
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}"
        )
