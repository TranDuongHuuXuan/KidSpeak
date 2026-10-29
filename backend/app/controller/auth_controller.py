from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.auth_schema import RegisterSchema, LoginSchema, LoginResponseSchema
from app.schemas.base_schema import DataResponse
from app.schemas.user_schema import UserSchema
from app.service.auth_service import AuthService

auth_router = APIRouter(prefix="/auth", tags=["Auth"])


# ─── Đăng ký ─────────────────────────────────────────────────────────────────
@auth_router.post(
    "/register",
    response_model=DataResponse[UserSchema],
    status_code=status.HTTP_201_CREATED,
    summary="Đăng ký tài khoản mới",
    description=(
        "Nhận thông tin đăng ký, kiểm tra trùng email/tên đăng nhập, "
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

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

    except IntegrityError as e:
        db.rollback()
        err_msg = str(e.orig).lower() if e.orig else ""
        if "email" in err_msg:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email này đã tồn tại",
            )
        if "username" in err_msg:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tên đăng nhập này đã được sử dụng",
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Lỗi cơ sở dữ liệu",
        )

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Đã xảy ra lỗi: {str(e)}",
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
