from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import require_roles
from app.models.user import User
from app.schemas.admin_expert_message_schema import AdminExpertMessageResponse, SendAdminExpertMessageSchema
from app.schemas.base_schema import DataResponse
from app.service.admin_expert_message_service import AdminExpertMessagingError, admin_expert_message_service
from app.service.media_storage_service import MediaNotFoundError, MediaStorageError, media_storage_service


admin_messages_router = APIRouter(prefix="/admin/expert-messages", tags=["Admin expert messaging"])
expert_messages_router = APIRouter(prefix="/expert/admin-messages", tags=["Expert admin messaging"])


def _fail(error: AdminExpertMessagingError):
    raise HTTPException(status_code=error.status_code, detail=str(error))


def _message_data(message):
    return AdminExpertMessageResponse.model_validate(message).model_dump(mode="json")


def _avatar_url(user_id: int, avatar: str | None):
    if not avatar:
        return None
    if avatar.startswith(("https://", "http://", "data:")):
        return avatar
    if not avatar.startswith(f"users/avatars/{user_id}/"):
        return None
    try:
        return media_storage_service.get_file_url(avatar)
    except (MediaNotFoundError, MediaStorageError):
        return None


@admin_messages_router.get("/experts", dependencies=[Depends(require_roles("ADMIN"))])
def list_experts(
    request: Request,
    search: str | None = Query(None, max_length=120),
    page: int = Query(1, ge=1),
    page_size: int = Query(30, ge=1, le=100),
    db: Session = Depends(get_db),
):
    items, total = admin_expert_message_service.list_experts(db, request.state.user.id, search, page, page_size)
    for item in items:
        item["avatar"] = _avatar_url(item["id"], item["avatar"])
    return DataResponse(data={"items": items, "total": total, "page": page, "page_size": page_size, "total_pages": (total + page_size - 1) // page_size})


@admin_messages_router.get("/experts/{expert_id}/messages", dependencies=[Depends(require_roles("ADMIN"))])
def get_admin_expert_messages(
    expert_id: int,
    request: Request,
    before_id: int | None = Query(None, ge=1),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
):
    try:
        result = admin_expert_message_service.admin_messages(db, request.state.user.id, expert_id, before_id, limit)
        result["items"] = [_message_data(row) for row in result["items"]]
        return DataResponse(data=result)
    except AdminExpertMessagingError as error:
        _fail(error)


@admin_messages_router.post("/experts/{expert_id}/messages", status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_roles("ADMIN"))])
def send_admin_expert_message(
    expert_id: int,
    data: SendAdminExpertMessageSchema,
    request: Request,
    db: Session = Depends(get_db),
):
    try:
        message = admin_expert_message_service.send_admin_message(db, request.state.user.id, expert_id, data.content)
        return DataResponse(data=_message_data(message), code="201", message="Đã gửi tin nhắn.")
    except AdminExpertMessagingError as error:
        _fail(error)


@admin_messages_router.patch("/experts/{expert_id}/read", dependencies=[Depends(require_roles("ADMIN"))])
def mark_admin_expert_messages_read(expert_id: int, request: Request, db: Session = Depends(get_db)):
    try:
        changed = admin_expert_message_service.mark_admin_read(db, request.state.user.id, expert_id)
        return DataResponse(data={"updated_count": changed})
    except AdminExpertMessagingError as error:
        _fail(error)


@expert_messages_router.get("", dependencies=[Depends(require_roles("EXPERT"))])
def list_admin_conversations(request: Request, db: Session = Depends(get_db)):
    items = admin_expert_message_service.expert_conversations(db, request.state.user.id)
    for item in items:
        admin = db.query(User).filter(User.id == item["admin_id"]).first()
        item["avatar"] = _avatar_url(item["admin_id"], admin.avatar) if admin else None
    return DataResponse(data=items)


@expert_messages_router.get("/{admin_id}/messages", dependencies=[Depends(require_roles("EXPERT"))])
def get_expert_admin_messages(
    admin_id: int,
    request: Request,
    before_id: int | None = Query(None, ge=1),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
):
    try:
        result = admin_expert_message_service.expert_messages(db, request.state.user.id, admin_id, before_id, limit)
        result["items"] = [_message_data(row) for row in result["items"]]
        return DataResponse(data=result)
    except AdminExpertMessagingError as error:
        _fail(error)


@expert_messages_router.post("/{admin_id}/messages", status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_roles("EXPERT"))])
def send_expert_admin_message(
    admin_id: int,
    data: SendAdminExpertMessageSchema,
    request: Request,
    db: Session = Depends(get_db),
):
    try:
        message = admin_expert_message_service.send_expert_message(db, request.state.user.id, admin_id, data.content)
        return DataResponse(data=_message_data(message), code="201", message="Đã gửi tin nhắn.")
    except AdminExpertMessagingError as error:
        _fail(error)


@expert_messages_router.patch("/{admin_id}/read", dependencies=[Depends(require_roles("EXPERT"))])
def mark_expert_admin_messages_read(admin_id: int, request: Request, db: Session = Depends(get_db)):
    try:
        changed = admin_expert_message_service.mark_expert_read(db, request.state.user.id, admin_id)
        return DataResponse(data={"updated_count": changed})
    except AdminExpertMessagingError as error:
        _fail(error)
