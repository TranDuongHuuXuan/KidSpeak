from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.core.database import Base


class StudentTeacher(Base):
    """Junction table linking students and teachers."""

    __tablename__ = "student_teachers"

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
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    teacher = relationship(
        "User",
        foreign_keys=[teacher_id],
        back_populates="teacher_classes",
    )
    student = relationship(
        "User",
        foreign_keys=[student_id],
        back_populates="student_classes",
    )

    def __repr__(self) -> str:
        return (
            f"<StudentTeacher id={self.id} "
            f"teacher={self.teacher_id} student={self.student_id}>"
        )
