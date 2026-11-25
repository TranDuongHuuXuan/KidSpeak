from datetime import date, datetime, time, timedelta

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import require_roles
from app.schemas.admin_user_schema import AdminUserResponseSchema, AdminUserUpdateSchema
from app.schemas.base_schema import DataResponse
from app.service.admin_user_service import AdminUserError, admin_user_service


admin_user_router = APIRouter(prefix="/admin/users", tags=["Admin user management"])
admin_guard = [Depends(require_roles("ADMIN"))]


def _map_user(user, details=None):
    details = details or {}
    expert_request = details.get("expert_request")
    learning_summary = details.get("learning_summary", {})
    return AdminUserResponseSchema(
        id=user.id, full_name=user.full_name, email=user.email,
        role_id=user.role_id, role_name=user.role.name if user.role else "",
        date_of_birth=user.date_of_birth, avatar=user.avatar,
        is_active=user.is_active, created_at=user.created_at, updated_at=user.updated_at,
        specialty=expert_request.specialty if expert_request else None,
        teaching_experience=expert_request.experience if expert_request else None,
        teacher_introduction=expert_request.introduction if expert_request else None,
        **learning_summary,
    )


def _handle_error(error: AdminUserError):
    raise HTTPException(status_code=error.status_code, detail=str(error))


@admin_user_router.get("", dependencies=admin_guard)
def list_users(
    search: str | None = Query(None, max_length=120),
    role_id: int | None = Query(None),
    is_active: bool | None = Query(None),
    created_from: date | None = Query(None),
    created_to: date | None = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    try:
        start = datetime.combine(created_from, time.min) if created_from else None
        end = datetime.combine(created_to + timedelta(days=1), time.min) - timedelta(microseconds=1) if created_to else None
        users, total = admin_user_service.list_users(
            db, search=search, role_id=role_id, is_active=is_active,
            created_from=start, created_to=end, page=page, page_size=page_size,
        )
        items = [_map_user(user).model_dump(mode="json") for user in users]
        pages = (total + page_size - 1) // page_size
        return DataResponse(data={"items": items, "total": total, "page": page, "page_size": page_size, "total_pages": pages})
    except AdminUserError as error:
        _handle_error(error)


@admin_user_router.get("/{user_id}", dependencies=admin_guard)
def get_user(user_id: int, db: Session = Depends(get_db)):
    try:
        user, details = admin_user_service.get_user(db, user_id)
        return DataResponse(data=_map_user(user, details))
    except AdminUserError as error:
        _handle_error(error)


@admin_user_router.patch("/{user_id}", dependencies=admin_guard)
def update_user(user_id: int, data: AdminUserUpdateSchema, db: Session = Depends(get_db)):
    try:
        return DataResponse(data=_map_user(admin_user_service.update_user(db, user_id, data)), message="Đã cập nhật người dùng.")
    except AdminUserError as error:
        _handle_error(error)


@admin_user_router.patch("/{user_id}/deactivate", dependencies=admin_guard)
def deactivate_user(user_id: int, db: Session = Depends(get_db)):
    try:
        user = admin_user_service.set_active(db, user_id, False)
        return DataResponse(data=_map_user(user), message="Đã khóa tài khoản.")
    except AdminUserError as error:
        _handle_error(error)


@admin_user_router.patch("/{user_id}/activate", dependencies=admin_guard)
def activate_user(user_id: int, db: Session = Depends(get_db)):
    try:
        user = admin_user_service.set_active(db, user_id, True)
        return DataResponse(data=_map_user(user), message="Đã kích hoạt tài khoản.")
    except AdminUserError as error:
        _handle_error(error)
