from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class Vocabulary(Base):
    """Vocabulary words belonging to a lesson."""

    __tablename__ = "vocabularies"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    lesson_id = Column(
        Integer,
        ForeignKey("lessons.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    word = Column(String(200), nullable=False)
    pronunciation = Column(String(200), nullable=True)
    image_url = Column(String(500), nullable=True)
    audio_url = Column(String(500), nullable=True)
    order = Column(Integer, nullable=True, default=0)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    lesson = relationship("Lesson", back_populates="vocabulary")
    practice_details = relationship(
        "PracticeDetail",
        back_populates="vocabulary",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Vocabulary id={self.id} word={self.word!r}>"
