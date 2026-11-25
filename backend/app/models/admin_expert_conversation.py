from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import relationship

from app.core.database import Base


class AdminExpertConversation(Base):
    __tablename__ = "admin_expert_conversations"
    __table_args__ = (
        UniqueConstraint("admin_id", "expert_id", name="uq_admin_expert_conversation_pair"),
    )

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    admin_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    expert_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow, index=True)

    admin = relationship("User", foreign_keys=[admin_id])
    expert = relationship("User", foreign_keys=[expert_id])
    messages = relationship("AdminExpertMessage", back_populates="conversation", cascade="all, delete-orphan")
