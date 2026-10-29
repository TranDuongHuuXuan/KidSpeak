from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.core.database import Base


class PracticeDetail(Base):
    """AI pronunciation scoring results for an individual vocabulary word."""

    __tablename__ = "practice_details"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    session_id = Column(
        Integer,
        ForeignKey("practice_sessions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    vocabulary_id = Column(
        Integer,
        ForeignKey("vocabularies.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    recording_url = Column(String(500), nullable=True)
    ai_transcription = Column(Text, nullable=True)
    initial_consonant_score = Column(Float, nullable=True)
    final_consonant_score = Column(Float, nullable=True)
    tone_score = Column(Float, nullable=True)
    overall_score = Column(Float, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    session = relationship("PracticeSession", back_populates="practice_details")
    vocabulary = relationship("Vocabulary", back_populates="practice_details")

    def __repr__(self) -> str:
        return (
            f"<PracticeDetail id={self.id} "
            f"session={self.session_id} vocabulary={self.vocabulary_id}>"
        )
