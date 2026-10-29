from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.core.database import Base


class Lesson(Base):
    """Lesson table."""

    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    category_id = Column(
        Integer,
        ForeignKey("lesson_categories.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    creator_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    title = Column(String(300), nullable=False)
    description = Column(Text, nullable=True)
    level = Column(String(50), nullable=True)
    order = Column(Integer, nullable=True, default=0)
    is_published = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    category = relationship("LessonCategory", back_populates="lessons")
    creator = relationship("User", back_populates="lessons")
    vocabulary = relationship(
        "Vocabulary",
        back_populates="lesson",
        cascade="all, delete-orphan",
    )
    practice_suggestions = relationship(
        "PracticeSuggestion",
        back_populates="lesson",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Lesson id={self.id} title={self.title!r}>"
