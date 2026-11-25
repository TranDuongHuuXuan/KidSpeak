from fastapi import UploadFile
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.expert_upgrade_request import ExpertUpgradeRequest
from app.models.role import Role
from app.models.user import User
from app.models.notification import Notification
from datetime import datetime
from pathlib import PurePosixPath
from app.core.security import normalize_role_name
from app.core.roles import EXPERT_ROLE_ID, EXPERT_ROLE_NAME
from app.repository.expert_upgrade_repository import ExpertUpgradeRepository
from app.schemas.expert_upgrade_schema import ExpertUpgradeInput
from app.service.media_storage_service import media_storage_service


class ExpertUpgradeError(Exception):
    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message)
        self.status_code = status_code


class ExpertUpgradeService:
    @staticmethod
    def _document(item: dict) -> dict:
        return {
            "file_name": item["filename"],
            "file_key": item["object_key"],
            "file_type": item["content_type"],
            "file_size": item["file_size"],
            "uploaded_at": item["uploaded_at"],
        }

    async def submit(
        self, db: Session, user: User, data: ExpertUpgradeInput,
        files: list[UploadFile], previous_request_id: int | None = None,
        keep_document_keys: list[str] | None = None,
    ):
        role_name = (user.role.name if user.role else "").upper()
        db.query(User).filter(User.id == user.id).with_for_update().first()
        if role_name == "EXPERT":
            raise ExpertUpgradeError("This account already has the Expert role.", 409)
        if len(files) > 5:
            raise ExpertUpgradeError("Each request can contain at most 5 files.")
        request_history = ExpertUpgradeRepository.list_for_user(db, user.id)
        if any(item.status in {"pending", "approved", "activated"} for item in request_history):
            raise ExpertUpgradeError("An active or approved request already exists.", 409)

        retained: list[dict] = []
        keep_document_keys = keep_document_keys or []
        if previous_request_id is not None:
            previous = ExpertUpgradeRepository.get(db, previous_request_id)
            if not previous or previous.user_id != user.id:
                raise ExpertUpgradeError("Previous request not found.", 404)
            if previous.status != "rejected":
                raise ExpertUpgradeError("Only a rejected request can be resubmitted.", 409)
            previous_docs = {item.get("file_key"): item for item in previous.documents or []}
            if any(key not in previous_docs for key in keep_document_keys):
                raise ExpertUpgradeError("A selected document is not part of the previous request.", 403)
            retained = [previous_docs[key] for key in dict.fromkeys(keep_document_keys)]
            supported_extensions = {".jpg", ".jpeg", ".png", ".webp", ".docx", ".xls", ".xlsx", ".pdf"}
            if any(PurePosixPath(item.get("file_name", "")).suffix.lower() not in supported_extensions for item in retained):
                raise ExpertUpgradeError("Only images, DOCX, Excel, and PDF files can be resubmitted.")
        elif keep_document_keys:
            raise ExpertUpgradeError("A previous request is required to retain documents.", 400)
        if len(files) + len(retained) > 5:
            raise ExpertUpgradeError("Each request can contain at most 5 documents.")

        uploaded: list[dict] = []
        request = ExpertUpgradeRequest(
            user_id=user.id, specialty=data.specialty.strip(),
            experience=data.experience.strip(), reason=data.reason.strip(),
            introduction=data.introduction.strip(), documents=[],
        )
        try:
            ExpertUpgradeRepository.create(db, request)
            for file in files:
                uploaded.append(await media_storage_service.upload_document(
                    file, f"expert-upgrade-requests/user-{user.id}/{request.id}"
                ))
            request.documents = retained + [self._document(item) for item in uploaded]
            db.add(Notification(
                user_id=user.id,
                title="Teacher request received",
                content="Your teacher request is pending admin review.",
                type="teacher_verification",
                url="/student/profile",
            ))
            db.commit()
            db.refresh(request)
            return request
        except Exception as e:
            db.rollback()
            media_storage_service.delete_many([item["object_key"] for item in uploaded])
            raise

    @staticmethod
    def list_own(db: Session, user_id: int):
        return ExpertUpgradeRepository.list_for_user(db, user_id)

    @staticmethod
    def list_admin(
        db: Session, status: str | None = None, search: str | None = None,
        email: str | None = None, reason: str | None = None,
        experience: str | None = None, skip: int = 0, limit: int = 20,
    ):
        return ExpertUpgradeRepository.list_all(db, status, search, email, reason, experience, skip, limit)

    @staticmethod
    def get_authorized(db: Session, request_id: int, user: User, is_admin: bool):
        request = ExpertUpgradeRepository.get(db, request_id)
        if not request:
            raise ExpertUpgradeError("Không tìm thấy hồ sơ nâng cấp.", 404)
        if not is_admin and request.user_id != user.id:
            raise ExpertUpgradeError("Bạn không có quyền truy cập hồ sơ này.", 403)
        return request

    @staticmethod
    def document_for_user(db: Session, request_id: int, index: int, user: User, is_admin: bool):
        request = ExpertUpgradeService.get_authorized(db, request_id, user, is_admin)
        if index < 0 or index >= len(request.documents or []):
            raise ExpertUpgradeError("Không tìm thấy tài liệu trong hồ sơ.", 404)
        document = request.documents[index]
        prefixes = (
            f"expert-applications/user-{request.user_id}/",
            f"expert-upgrade-requests/user-{request.user_id}/",
        )
        if not any(document["file_key"].startswith(prefix) for prefix in prefixes):
            raise ExpertUpgradeError("Document key is invalid.")
        return document

    @staticmethod
    def review(db: Session, request_id: int, reviewer: User, status: str, note: str):
        request = db.query(ExpertUpgradeRequest).filter(
            ExpertUpgradeRequest.id == request_id
        ).with_for_update().first()
        if not request:
            raise ExpertUpgradeError("Không tìm thấy hồ sơ nâng cấp.")
        if request.status != "pending":
            raise ExpertUpgradeError("Hồ sơ này đã được xử lý.", 409)
        if status == "rejected" and not note.strip():
            raise ExpertUpgradeError("Vui lòng nhập lý do từ chối hồ sơ.")
        from datetime import datetime
        request.status = status
        request.review_note = note.strip()
        request.reviewed_by = reviewer.id
        request.reviewed_at = datetime.utcnow()
        try:
            applicant = db.query(User).filter(User.id == request.user_id).first()
            if not applicant:
                raise ExpertUpgradeError("Applicant not found.", 404)
            db.add(Notification(
                user_id=applicant.id,
                title="Teacher verification result",
                content=(
                    "Congratulations! Your teacher request was approved. Visit your profile to activate your teacher role."
                    if status == "approved"
                    else f"Your teacher request was rejected. Reason: {request.review_note}"
                ),
                type="teacher_verification",
                url="/student/profile",
            ))
            db.commit()
            db.refresh(request)
            return request
        except SQLAlchemyError:
            db.rollback()
            raise


    @staticmethod
    def activate(db: Session, user: User):
        # Middleware attaches a user loaded by a different, already-closed session.
        # Reload it here so the role change is tracked and committed by this session.
        applicant = db.query(User).filter(User.id == user.id).with_for_update().first()
        if not applicant:
            raise ExpertUpgradeError("User account was not found.", 404)
        request = (db.query(ExpertUpgradeRequest).filter(
            ExpertUpgradeRequest.user_id == applicant.id,
            ExpertUpgradeRequest.status == "approved",
        ).order_by(ExpertUpgradeRequest.submitted_at.desc()).with_for_update().first())
        if not request:
            raise ExpertUpgradeError("No approved teacher request is available to activate.", 409)
        if normalize_role_name(applicant.role.name if applicant.role else None) != "STUDENT":
            raise ExpertUpgradeError("Only student accounts can activate this role.", 409)
        expert_role = db.query(Role).filter(
            Role.id == EXPERT_ROLE_ID,
            Role.name == EXPERT_ROLE_NAME,
        ).first()
        if not expert_role:
            raise ExpertUpgradeError("Canonical EXPERT role (id=3) is not configured. Run Alembic migrations.", 500)
        from datetime import datetime
        try:
            applicant.role_id = expert_role.id
            request.status = "activated"
            request.activated_at = datetime.utcnow()
            db.commit()
            db.refresh(request)
            return request
        except SQLAlchemyError:
            db.rollback()
            raise


expert_upgrade_service = ExpertUpgradeService()
