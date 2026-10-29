from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.core.database import Base


class PracticeSession(Base):
    """A session started by a student to practice."""

    __tablename__ = "practice_sessions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    started_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    ended_at = Column(DateTime, nullable=True)
    total_score = Column(Float, nullable=True, default=0.0)

    user = relationship("User", back_populates="practice_sessions")
    practice_details = relationship(
        "PracticeDetail",
        back_populates="session",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<PracticeSession id={self.id} user={self.user_id}>"
