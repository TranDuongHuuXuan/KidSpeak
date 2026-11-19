from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from app.core.database import Base


class Comment(Base):
    """A user comment on a lesson or vocabulary item, optionally a reply."""

    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    lesson_id = Column(
        Integer,
        ForeignKey("lessons.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    vocabulary_id = Column(
        Integer,
        ForeignKey("vocabularies.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    content = Column(Text, nullable=False)
    parent_comment_id = Column(
        Integer,
        ForeignKey("comments.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    user = relationship("User", back_populates="comments")
    lesson = relationship("Lesson", back_populates="comments")
    vocabulary = relationship("Vocabulary", back_populates="comments")
    parent = relationship(
        "Comment",
        remote_side=[id],
        foreign_keys=[parent_comment_id],
        back_populates="replies",
    )
    replies = relationship(
        "Comment",
        foreign_keys=[parent_comment_id],
        back_populates="parent",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Comment id={self.id} user={self.user_id}>"
