from datetime import datetime

from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_, func
from sqlalchemy.orm import Session, joinedload

from app.core.roles import ADMIN_ROLE_ID, EXPERT_ROLE_ID
from app.models.admin_expert_conversation import AdminExpertConversation
from app.models.admin_expert_message import AdminExpertMessage
from app.models.user import User


class AdminExpertMessageRepository:
    @staticmethod
    def list_experts(db: Session, admin_id: int, search: str | None, page: int, page_size: int):
        query = db.query(User, AdminExpertConversation).outerjoin(
            AdminExpertConversation,
            and_(
                AdminExpertConversation.expert_id == User.id,
                AdminExpertConversation.admin_id == admin_id,
            ),
        ).filter(User.role_id == EXPERT_ROLE_ID)
        if search:
            pattern = f"%{search.strip().lower()}%"
            query = query.filter(func.lower(User.full_name).like(pattern) | func.lower(User.email).like(pattern))
        total = query.order_by(None).count()
        pairs = query.order_by(
            AdminExpertConversation.updated_at.desc().nullslast(),
            User.created_at.desc(),
            User.id.desc(),
        ).offset((page - 1) * page_size).limit(page_size).all()
        rows = []
        for expert, conversation in pairs:
            latest = None
            unread_count = 0
            if conversation:
                latest = db.query(AdminExpertMessage).filter(
                    AdminExpertMessage.conversation_id == conversation.id
                ).order_by(AdminExpertMessage.id.desc()).first()
                unread_count = db.query(func.count(AdminExpertMessage.id)).filter(
                    AdminExpertMessage.conversation_id == conversation.id,
                    AdminExpertMessage.recipient_id == admin_id,
                    AdminExpertMessage.read_at.is_(None),
                ).scalar() or 0
            rows.append((expert, conversation, latest, unread_count))
        rows.sort(key=lambda row: (
            row[1].updated_at if row[1] else datetime.min,
            row[0].created_at or datetime.min,
            row[0].id,
        ), reverse=True)
        return rows, total

    @staticmethod
    def get_user(db: Session, user_id: int, role_id: int):
        return db.query(User).filter(User.id == user_id, User.role_id == role_id).first()

    @staticmethod
    def get_conversation(db: Session, admin_id: int, expert_id: int):
        return db.query(AdminExpertConversation).filter(
            AdminExpertConversation.admin_id == admin_id,
            AdminExpertConversation.expert_id == expert_id,
        ).first()

    @classmethod
    def get_or_create_conversation(cls, db: Session, admin_id: int, expert_id: int):
        conversation = cls.get_conversation(db, admin_id, expert_id)
        if conversation:
            return conversation
        conversation = AdminExpertConversation(admin_id=admin_id, expert_id=expert_id)
        db.add(conversation)
        try:
            db.flush()
            return conversation
        except IntegrityError:
            db.rollback()
            existing = cls.get_conversation(db, admin_id, expert_id)
            if existing:
                return existing
            raise

    @staticmethod
    def get_messages(db: Session, conversation_id: int, before_id: int | None, limit: int):
        query = db.query(AdminExpertMessage).filter(AdminExpertMessage.conversation_id == conversation_id)
        if before_id:
            query = query.filter(AdminExpertMessage.id < before_id)
        rows_desc = query.order_by(AdminExpertMessage.id.desc()).limit(limit + 1).all()
        has_more = len(rows_desc) > limit
        rows = list(reversed(rows_desc[:limit]))
        before = rows[0].id if has_more and rows else None
        return rows, has_more, before

    @staticmethod
    def unread_count(db: Session, conversation_id: int, recipient_id: int) -> int:
        return db.query(func.count(AdminExpertMessage.id)).filter(
            AdminExpertMessage.conversation_id == conversation_id,
            AdminExpertMessage.recipient_id == recipient_id,
            AdminExpertMessage.read_at.is_(None),
        ).scalar() or 0

    @staticmethod
    def list_expert_conversations(db: Session, expert_id: int):
        return db.query(AdminExpertConversation).options(
            joinedload(AdminExpertConversation.admin)
        ).filter(
            AdminExpertConversation.expert_id == expert_id
        ).order_by(AdminExpertConversation.updated_at.desc(), AdminExpertConversation.id.desc()).all()

    @staticmethod
    def list_admin_recipients(db: Session, expert_id: int):
        admins = db.query(User).filter(User.role_id == ADMIN_ROLE_ID).order_by(
            User.is_active.desc(), User.created_at.desc(), User.id.desc()
        ).all()
        rows = []
        for admin in admins:
            conversation = db.query(AdminExpertConversation).filter(
                AdminExpertConversation.admin_id == admin.id,
                AdminExpertConversation.expert_id == expert_id,
            ).first()
            if not admin.is_active and not conversation:
                continue
            latest = None
            unread = 0
            if conversation:
                latest = db.query(AdminExpertMessage).filter(
                    AdminExpertMessage.conversation_id == conversation.id
                ).order_by(AdminExpertMessage.id.desc()).first()
                unread = AdminExpertMessageRepository.unread_count(db, conversation.id, expert_id)
            rows.append((admin, conversation, latest, unread))
        rows.sort(key=lambda row: (
            row[1].updated_at if row[1] else datetime.min,
            row[0].is_active,
            row[0].created_at or datetime.min,
            row[0].id,
        ), reverse=True)
        return rows

    @staticmethod
    def commit(db: Session):
        db.commit()


admin_expert_message_repository = AdminExpertMessageRepository()
