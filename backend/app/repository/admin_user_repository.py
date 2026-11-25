from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from app.core.roles import EXPERT_ROLE_ID, STUDENT_ROLE_ID
from app.models.expert_upgrade_request import ExpertUpgradeRequest
from app.models.course_enrollment import CourseEnrollment
from app.models.practice_history import PracticeHistory
from app.models.practice_session import PracticeSession
from app.models.user import User


class AdminUserRepository:
    @staticmethod
    def _base_query(db: Session):
        return db.query(User).options(joinedload(User.role)).filter(
            User.role_id.in_((STUDENT_ROLE_ID, EXPERT_ROLE_ID))
        )

    @classmethod
    def list_users(
        cls, db: Session, *, search: str | None, role_id: int | None,
        is_active: bool | None, created_from: datetime | None,
        created_to: datetime | None, offset: int, page_size: int,
    ):
        query = cls._base_query(db)
        if search:
            needle = f"%{search.strip().lower()}%"
            query = query.filter(func.lower(User.full_name).like(needle) | func.lower(User.email).like(needle))
        if role_id is not None:
            query = query.filter(User.role_id == role_id)
        if is_active is not None:
            query = query.filter(User.is_active.is_(is_active))
        if created_from is not None:
            query = query.filter(User.created_at >= created_from)
        if created_to is not None:
            query = query.filter(User.created_at <= created_to)

        total = query.order_by(None).count()
        users = query.order_by(User.created_at.desc(), User.id.desc()).offset(offset).limit(page_size).all()
        return users, total

    @classmethod
    def get_by_id(cls, db: Session, user_id: int):
        return db.query(User).options(joinedload(User.role)).filter(User.id == user_id).first()

    @staticmethod
    def email_in_use(db: Session, email: str, user_id: int) -> bool:
        return db.query(User.id).filter(
            func.lower(User.email) == email.lower(), User.id != user_id
        ).first() is not None

    @staticmethod
    def latest_expert_request(db: Session, user_id: int):
        return db.query(ExpertUpgradeRequest).filter(
            ExpertUpgradeRequest.user_id == user_id
        ).order_by(ExpertUpgradeRequest.submitted_at.desc(), ExpertUpgradeRequest.id.desc()).first()

    @staticmethod
    def student_learning_summary(db: Session, user_id: int) -> dict[str, int]:
        return {
            "course_enrollment_count": db.query(func.count(CourseEnrollment.id)).filter(CourseEnrollment.student_id == user_id).scalar() or 0,
            "practice_session_count": db.query(func.count(PracticeSession.id)).filter(PracticeSession.user_id == user_id).scalar() or 0,
            "practice_history_count": db.query(func.count(PracticeHistory.id)).filter(PracticeHistory.student_id == user_id).scalar() or 0,
        }


admin_user_repository = AdminUserRepository()
