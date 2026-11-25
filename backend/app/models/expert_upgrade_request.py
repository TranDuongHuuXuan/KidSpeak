from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import relationship

from app.core.database import Base


class ExpertUpgradeRequest(Base):
    """Student request to upgrade their account to expert."""

    __tablename__ = "expert_upgrade_requests"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    specialty = Column(String(120), nullable=False, default="")
    experience = Column(Text, nullable=False, default="")
    reason = Column(Text, nullable=False)
    introduction = Column(Text, nullable=False, default="")
    documents = Column(JSON, nullable=False, default=list)
    status = Column(String(20), nullable=False, default="pending", index=True)
    review_note = Column(Text, nullable=False, default="")
    reviewed_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    submitted_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    reviewed_at = Column(DateTime, nullable=True)
    activated_at = Column(DateTime, nullable=True)

    user = relationship("User", foreign_keys=[user_id])
    reviewer = relationship("User", foreign_keys=[reviewed_by])
