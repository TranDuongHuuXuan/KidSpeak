from sqlalchemy.orm import Session, joinedload

from app.models.expert_upgrade_request import ExpertUpgradeRequest
from app.models.user import User


class ExpertUpgradeRepository:
    @staticmethod
    def create(db: Session, request: ExpertUpgradeRequest) -> ExpertUpgradeRequest:
        db.add(request)
        db.flush()
        return request

    @staticmethod
    def get(db: Session, request_id: int) -> ExpertUpgradeRequest | None:
        return (
            db.query(ExpertUpgradeRequest)
            .options(joinedload(ExpertUpgradeRequest.user))
            .filter(ExpertUpgradeRequest.id == request_id)
            .first()
        )

    @staticmethod
    def list_for_user(db: Session, user_id: int) -> list[ExpertUpgradeRequest]:
        return db.query(ExpertUpgradeRequest).filter(
            ExpertUpgradeRequest.user_id == user_id
        ).order_by(ExpertUpgradeRequest.submitted_at.desc()).all()

    @staticmethod
    def list_all(
        db: Session, status: str | None = None, search: str | None = None,
        email: str | None = None, reason: str | None = None,
        experience: str | None = None, skip: int = 0, limit: int = 20,
    ):
        query = db.query(ExpertUpgradeRequest).options(
            joinedload(ExpertUpgradeRequest.user)
        )
        if status:
            query = query.filter(ExpertUpgradeRequest.status == status)
        if search or email:
            query = query.join(ExpertUpgradeRequest.user)
        if search:
            query = query.filter(User.full_name.ilike(f"%{search.strip()}%"))
        if email:
            query = query.filter(User.email.ilike(f"%{email.strip()}%"))
        if reason:
            query = query.filter(ExpertUpgradeRequest.reason.ilike(f"%{reason.strip()}%"))
        if experience:
            query = query.filter(ExpertUpgradeRequest.experience.ilike(f"%{experience.strip()}%"))
        total = query.count()
        items = query.order_by(ExpertUpgradeRequest.submitted_at.desc()).offset(skip).limit(limit).all()
        return items, total
