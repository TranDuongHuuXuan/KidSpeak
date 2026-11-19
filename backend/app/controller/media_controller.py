from typing import Optional

from fastapi import APIRouter, Depends, File, HTTPException, Request, UploadFile, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.logger import logger
from app.models.user import User
from app.schemas.base_schema import DataResponse
from app.schemas.media_schema import MediaObjectSchema, UserAvatarSchema
from app.service.media_storage_service import (
    MediaNotFoundError,
    MediaStorageError,
    MediaTooLargeError,
    MediaValidationError,
    media_storage_service,
)

media_router = APIRouter(prefix="/media", tags=["Media"])


def _owned_avatar_key(object_key: str | None, user_id: int) -> bool:
    return bool(object_key and object_key.startswith(f"users/avatars/{user_id}/"))


@media_router.post(
    "/avatar",
    response_model=DataResponse[MediaObjectSchema],
    status_code=status.HTTP_201_CREATED,
    summary="Upload ảnh đại diện",
)
async def upload_avatar(
    request: Request,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    user_id = request.state.user.id
    try:
        uploaded = await media_storage_service.upload_file(
            file=file,
            folder=f"users/avatars/{user_id}",
            media_type="image",
        )
    except MediaTooLargeError as error:
        raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail=str(error))
    except MediaValidationError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
    except MediaStorageError:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Không thể lưu ảnh đại diện lúc này.",
        )

    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Phiên đăng nhập không hợp lệ.",
            )
        previous_key = user.avatar
        user.avatar = uploaded["object_key"]
        db.commit()
    except HTTPException:
        db.rollback()
        try:
            media_storage_service.delete_file(uploaded["object_key"])
        except Exception:
            logger.exception("Could not clean up an unreferenced avatar object.")
        raise
    except SQLAlchemyError as error:
        db.rollback()
        try:
            media_storage_service.delete_file(uploaded["object_key"])
        except Exception:
            logger.exception("Could not clean up an unreferenced avatar object.")
        logger.error("Database error while updating a user's avatar.")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Không thể cập nhật ảnh đại diện lúc này.",
        ) from error

    if _owned_avatar_key(previous_key, user_id) and previous_key != uploaded["object_key"]:
        try:
            media_storage_service.delete_file(previous_key)
        except Exception:
            logger.exception("Could not remove a replaced avatar object.")

    return DataResponse.custom_response(
        data=uploaded,
        code="201",
        message="Cập nhật ảnh đại diện thành công.",
    )


@media_router.get(
    "/avatar",
    response_model=DataResponse[Optional[UserAvatarSchema]],
    summary="Lấy URL ảnh đại diện",
)
def get_avatar_url(
    request: Request,
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == request.state.user.id).first()
    if not user or not _owned_avatar_key(user.avatar, user.id):
        return DataResponse.custom_response(data=None, message="Chưa có ảnh đại diện.")

    try:
        url = media_storage_service.get_file_url(user.avatar)
    except MediaNotFoundError:
        logger.error("A user's avatar key references a missing media object.")
        return DataResponse.custom_response(data=None, message="Chưa có ảnh đại diện.")
    except MediaStorageError as error:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Không thể truy xuất ảnh đại diện lúc này.",
        ) from error

    return DataResponse.custom_response(
        data={"object_key": user.avatar, "url": url},
        message="Lấy ảnh đại diện thành công.",
    )


@media_router.delete(
    "/avatar",
    response_model=DataResponse[None],
    summary="Xóa ảnh đại diện",
)
def delete_avatar(
    request: Request,
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == request.state.user.id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Phiên đăng nhập không hợp lệ.",
        )

    object_key = user.avatar
    if _owned_avatar_key(object_key, user.id):
        try:
            media_storage_service.delete_file(object_key)
        except MediaNotFoundError:
            pass
        except MediaStorageError as error:
            logger.error("Could not remove a user's avatar object from MinIO.")
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Không thể xóa ảnh đại diện khỏi kho media.",
            ) from error

    user.avatar = None
    try:
        db.commit()
    except SQLAlchemyError as error:
        db.rollback()
        logger.error("Database error while deleting a user's avatar reference.")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Không thể xóa ảnh đại diện lúc này.",
        ) from error

    return DataResponse.custom_response(
        data=None,
        message="Đã xóa ảnh đại diện.",
    )
