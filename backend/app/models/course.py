from datetime import datetime
from decimal import Decimal
from enum import Enum as PyEnum

from sqlalchemy import Column, DateTime, Enum, Integer, Numeric, String, Text
from sqlalchemy.orm import relationship

from app.core.database import Base


class CourseStatus(PyEnum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class Course(Base):
    """A paid or free course containing a set of lessons."""

    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    fee = Column(Numeric(10, 2), nullable=False, default=Decimal("0.00"))
    status = Column(
        Enum(
            CourseStatus,
            name="course_status",
            values_callable=lambda enum_cls: [item.value for item in enum_cls],
        ),
        nullable=False,
        default=CourseStatus.ACTIVE,
    )
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    enrollments = relationship(
        "CourseEnrollment",
        back_populates="course",
        cascade="all, delete-orphan",
    )
    classes = relationship(
        "Classroom",
        back_populates="course",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Course id={self.id} name={self.name!r}>"
