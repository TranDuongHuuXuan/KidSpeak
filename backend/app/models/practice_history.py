from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.core.database import Base


class PracticeHistory(Base):
    """A student's saved result for a practice session."""

    __tablename__ = "practice_histories"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    student_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    session_id = Column(
        Integer,
        ForeignKey("practice_sessions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    score = Column(Float, nullable=True)
    recording_file = Column(String(500), nullable=True)
    ai_feedback = Column(Text, nullable=True)
    duration_seconds = Column(Integer, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    student = relationship("User", back_populates="practice_histories")
    session = relationship("PracticeSession", back_populates="history")

    def __repr__(self) -> str:
        return (
            f"<PracticeHistory id={self.id} "
            f"student={self.student_id} session={self.session_id}>"
        )
