from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class CourseEnrollment(Base):
    """A student's enrollment and progress in a course."""

    __tablename__ = "course_enrollments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    student_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    course_id = Column(
        Integer,
        ForeignKey("courses.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    registered_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    progress = Column(Float, nullable=False, default=0.0)
    status = Column(String(50), nullable=False, default="active")

    student = relationship("User", back_populates="course_enrollments")
    course = relationship("Course", back_populates="enrollments")

    def __repr__(self) -> str:
        return (
            f"<CourseEnrollment id={self.id} "
            f"student={self.student_id} course={self.course_id}>"
        )
