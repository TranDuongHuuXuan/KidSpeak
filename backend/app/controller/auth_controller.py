from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.logger import logger
from app.core.security import get_current_user, normalize_role_name
from app.schemas.auth_schema import RegisterSchema, LoginSchema, LoginResponseSchema
from app.schemas.base_schema import DataResponse
from app.schemas.user_schema import UserProfileUpdateSchema, UserSchema
from app.models.user import User
from app.service.auth_service import (
    AuthService,
    InactiveAccountError,
    InvalidCredentialsError,
    RegistrationConflictError,
)
from app.service.auth_service import AuthService

auth_router = APIRouter(prefix="/auth", tags=["Auth"])


# ─── Đăng ký ─────────────────────────────────────────────────────────────────
@auth_router.post(
    "/register",
    response_model=DataResponse[UserSchema],
    status_code=status.HTTP_201_CREATED,
    summary="Đăng ký tài khoản mới",
    description=(
        "Nhận thông tin đăng ký, kiểm tra email đã tồn tại, "
        "lưu người dùng vào database với role STUDENT và kích hoạt tài khoản ngay lập tức."
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

    except InvalidCredentialsError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email hoặc mật khẩu không chính xác.",
        )

    except InactiveAccountError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Tài khoản không hoạt động hoặc chưa được cấp quyền hợp lệ.",
        )

    except Exception:
        logger.error("Unexpected error while authenticating an account.")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Không thể đăng nhập lúc này. Vui lòng thử lại sau.",
        )


@auth_router.get(
    "/me",
    response_model=DataResponse[UserSchema],
    summary="Lấy tài khoản đang đăng nhập",
)
def get_me(current_user=Depends(get_current_user)):
    user = UserSchema.model_validate(current_user).model_copy(
        update={
            "role_name": normalize_role_name(
                current_user.role.name if current_user.role else None
            )
        }
    )
    return DataResponse(data=user)


@auth_router.patch(
    "/me",
    response_model=DataResponse[UserSchema],
    summary="Cập nhật hồ sơ tài khoản đang đăng nhập",
)
def update_me(
    data: UserProfileUpdateSchema,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == current_user.id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy tài khoản.")

    changes = data.model_dump(exclude_unset=True)
    if "full_name" in changes and changes["full_name"] is not None:
        user.full_name = changes["full_name"].strip()
    if "date_of_birth" in changes:
        birth_date = changes["date_of_birth"]
        user.date_of_birth = datetime.combine(birth_date, datetime.min.time()) if birth_date else None

    try:
        db.commit()
        db.refresh(user)
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Không thể cập nhật hồ sơ lúc này.",
        )

    result = UserSchema.model_validate(user).model_copy(
        update={
            "role_name": normalize_role_name(user.role.name if user.role else None)
        }
    )
    return DataResponse(data=result, message="Đã cập nhật hồ sơ.")
