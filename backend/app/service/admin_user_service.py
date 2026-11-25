from datetime import datetime

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.roles import EXPERT_ROLE_ID, STUDENT_ROLE_ID
from app.repository.admin_user_repository import admin_user_repository


class AdminUserError(Exception):
    def __init__(self, message: str, status_code: int):
        super().__init__(message)
        self.status_code = status_code


class AdminUserService:
    @staticmethod
    def _ensure_manageable(user):
        if user is None:
            raise AdminUserError("Không tìm thấy người dùng.", 404)
        if user.role_id not in (STUDENT_ROLE_ID, EXPERT_ROLE_ID):
            raise AdminUserError("Admin chỉ được quản lý tài khoản Student và Expert.", 403)

    def list_users(self, db: Session, *, search, role_id, is_active, created_from, created_to, page, page_size):
        if role_id is not None and role_id not in (STUDENT_ROLE_ID, EXPERT_ROLE_ID):
            raise AdminUserError("Role chỉ có thể là Student (2) hoặc Expert (3).", 422)
        users, total = admin_user_repository.list_users(
            db, search=search, role_id=role_id, is_active=is_active,
            created_from=created_from, created_to=created_to,
            offset=(page - 1) * page_size, page_size=page_size,
        )
        return users, total

    def get_user(self, db: Session, user_id: int):
        user = admin_user_repository.get_by_id(db, user_id)
        self._ensure_manageable(user)
        details = None
        if user.role_id == EXPERT_ROLE_ID:
            details = {"expert_request": admin_user_repository.latest_expert_request(db, user.id)}
        elif user.role_id == STUDENT_ROLE_ID:
            details = {"learning_summary": admin_user_repository.student_learning_summary(db, user.id)}
        return user, details

    def update_user(self, db: Session, user_id: int, data):
        user = admin_user_repository.get_by_id(db, user_id)
        self._ensure_manageable(user)
        changes = data.model_dump(exclude_unset=True)
        if not changes:
            raise AdminUserError("Cần cung cấp ít nhất một trường để cập nhật.", 422)
        if "email" in changes and changes["email"] != user.email.lower() and admin_user_repository.email_in_use(db, changes["email"], user.id):
            raise AdminUserError("Email đã được sử dụng.", 409)
        for field, value in changes.items():
            setattr(user, field, value)
        user.updated_at = datetime.utcnow()
        try:
            db.commit()
            db.refresh(user)
        except IntegrityError as error:
            db.rollback()
            raise AdminUserError("Email đã được sử dụng.", 409) from error
        except Exception:
            db.rollback()
            raise
        return user

    def set_active(self, db: Session, user_id: int, is_active: bool):
        user = admin_user_repository.get_by_id(db, user_id)
        self._ensure_manageable(user)
        user.is_active = is_active
        user.updated_at = datetime.utcnow()
        try:
            db.commit()
            db.refresh(user)
        except Exception:
            db.rollback()
            raise
        return user


admin_user_service = AdminUserService()
