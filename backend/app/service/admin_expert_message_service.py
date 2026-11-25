from datetime import datetime

from sqlalchemy.orm import Session

from app.core.roles import ADMIN_ROLE_ID, EXPERT_ROLE_ID
from app.models.admin_expert_message import AdminExpertMessage
from app.repository.admin_expert_message_repository import admin_expert_message_repository as repository


class AdminExpertMessagingError(Exception):
    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message)
        self.status_code = status_code


class AdminExpertMessageService:
    def list_experts(self, db: Session, admin_id: int, search: str | None, page: int, page_size: int):
        rows, total = repository.list_experts(db, admin_id, search, page, page_size)
        items = []
        for expert, conversation, latest, unread in rows:
            items.append({
                "id": expert.id,
                "full_name": expert.full_name,
                "email": expert.email,
                "avatar": expert.avatar,
                "is_active": expert.is_active,
                "conversation_id": conversation.id if conversation else None,
                "last_message": latest.content if latest else "",
                "last_message_at": latest.sent_at if latest else None,
                "last_message_sender_id": latest.sender_id if latest else None,
                "unread_count": unread,
            })
        return items, total

    @staticmethod
    def _expert(db: Session, expert_id: int):
        expert = repository.get_user(db, expert_id, EXPERT_ROLE_ID)
        if not expert:
            raise AdminExpertMessagingError("Không tìm thấy Expert.", 404)
        return expert

    @staticmethod
    def _admin(db: Session, admin_id: int):
        admin = repository.get_user(db, admin_id, ADMIN_ROLE_ID)
        if not admin:
            raise AdminExpertMessagingError("Không tìm thấy tài khoản Admin.", 404)
        return admin

    def admin_messages(self, db: Session, admin_id: int, expert_id: int, before_id: int | None, limit: int):
        expert = self._expert(db, expert_id)
        conversation = repository.get_conversation(db, admin_id, expert_id)
        if conversation is None:
            return {"items": [], "has_more": False, "before_id": None, "unread_count": 0, "conversation_id": None}
        messages, has_more, next_before = repository.get_messages(db, conversation.id, before_id, limit)
        return {
            "items": messages,
            "has_more": has_more,
            "before_id": next_before,
            "unread_count": repository.unread_count(db, conversation.id, admin_id),
            "conversation_id": conversation.id,
        }

    def send_admin_message(self, db: Session, admin_id: int, expert_id: int, content: str):
        expert = self._expert(db, expert_id)
        if not expert.is_active:
            raise AdminExpertMessagingError("Expert đang bị khóa; không thể gửi tin nhắn.", 409)
        conversation = repository.get_or_create_conversation(db, admin_id, expert_id)
        message = AdminExpertMessage(
            conversation_id=conversation.id,
            sender_id=admin_id,
            recipient_id=expert_id,
            content=content,
        )
        conversation.updated_at = datetime.utcnow()
        db.add(message)
        repository.commit(db)
        db.refresh(message)
        return message

    def mark_admin_read(self, db: Session, admin_id: int, expert_id: int):
        self._expert(db, expert_id)
        conversation = repository.get_conversation(db, admin_id, expert_id)
        if not conversation:
            return 0
        changed = db.query(AdminExpertMessage).filter(
            AdminExpertMessage.conversation_id == conversation.id,
            AdminExpertMessage.recipient_id == admin_id,
            AdminExpertMessage.read_at.is_(None),
        ).update({AdminExpertMessage.read_at: datetime.utcnow()}, synchronize_session=False)
        repository.commit(db)
        return changed

    def expert_conversations(self, db: Session, expert_id: int):
        conversations = repository.list_admin_recipients(db, expert_id)
        items = []
        for admin, conversation, latest, unread in conversations:
            items.append({
                "admin_id": admin.id,
                "admin_name": admin.full_name,
                "admin_email": admin.email,
                "is_active": admin.is_active,
                "conversation_id": conversation.id if conversation else None,
                "last_message": latest.content if latest else "",
                "last_message_at": latest.sent_at if latest else conversation.updated_at if conversation else None,
                "last_message_sender_id": latest.sender_id if latest else None,
                "unread_count": unread,
            })
        return items

    def expert_messages(self, db: Session, expert_id: int, admin_id: int, before_id: int | None, limit: int):
        self._admin(db, admin_id)
        conversation = repository.get_conversation(db, admin_id, expert_id)
        if not conversation:
            admin = self._admin(db, admin_id)
            if not admin.is_active:
                raise AdminExpertMessagingError("Admin hiện không hoạt động.", 409)
            conversation = repository.get_or_create_conversation(db, admin_id, expert_id)
            repository.commit(db)
        messages, has_more, next_before = repository.get_messages(db, conversation.id, before_id, limit)
        return {"items": messages, "has_more": has_more, "before_id": next_before, "conversation_id": conversation.id}

    def send_expert_message(self, db: Session, expert_id: int, admin_id: int, content: str):
        admin = self._admin(db, admin_id)
        if not admin.is_active:
            raise AdminExpertMessagingError("Admin hiện không hoạt động; không thể gửi tin nhắn.", 409)
        conversation = repository.get_conversation(db, admin_id, expert_id)
        if not conversation:
            conversation = repository.get_or_create_conversation(db, admin_id, expert_id)
        message = AdminExpertMessage(
            conversation_id=conversation.id,
            sender_id=expert_id,
            recipient_id=admin_id,
            content=content,
        )
        conversation.updated_at = datetime.utcnow()
        db.add(message)
        repository.commit(db)
        db.refresh(message)
        return message

    def mark_expert_read(self, db: Session, expert_id: int, admin_id: int):
        self._admin(db, admin_id)
        conversation = repository.get_conversation(db, admin_id, expert_id)
        if not conversation:
            raise AdminExpertMessagingError("Không tìm thấy cuộc trò chuyện.", 404)
        changed = db.query(AdminExpertMessage).filter(
            AdminExpertMessage.conversation_id == conversation.id,
            AdminExpertMessage.recipient_id == expert_id,
            AdminExpertMessage.read_at.is_(None),
        ).update({AdminExpertMessage.read_at: datetime.utcnow()}, synchronize_session=False)
        repository.commit(db)
        return changed


admin_expert_message_service = AdminExpertMessageService()
