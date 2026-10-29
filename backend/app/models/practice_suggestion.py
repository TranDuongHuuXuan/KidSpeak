from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from app.core.database import Base


class PracticeSuggestion(Base):
    """Practice suggestion sent by a teacher to a student."""

    __tablename__ = "practice_suggestions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    teacher_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    student_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    lesson_id = Column(
        Integer,
        ForeignKey("lessons.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    content = Column(Text, nullable=True)
    is_read = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    teacher = relationship(
        "User",
        foreign_keys=[teacher_id],
        back_populates="suggestions_created",
    )
    student = relationship(
        "User",
        foreign_keys=[student_id],
        back_populates="suggestions_received",
    )
    lesson = relationship("Lesson", back_populates="practice_suggestions")

    def __repr__(self) -> str:
        return (
            f"<PracticeSuggestion id={self.id} "
            f"teacher={self.teacher_id} student={self.student_id}>"
        )
