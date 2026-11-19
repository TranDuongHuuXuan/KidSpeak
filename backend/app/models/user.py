from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class User(Base):
    """User table shared by administrators, teachers, and students."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False, unique=True, index=True)
    password = Column(String(255), nullable=False)
    role_id = Column(
        Integer,
        ForeignKey("roles.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    date_of_birth = Column(DateTime, nullable=True)
    avatar = Column(String(500), nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    role = relationship("Role", back_populates="users")
    notifications = relationship(
        "Notification",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    teacher_classes = relationship(
        "StudentTeacher",
        foreign_keys="StudentTeacher.teacher_id",
        back_populates="teacher",
        cascade="all, delete-orphan",
    )
    student_classes = relationship(
        "StudentTeacher",
        foreign_keys="StudentTeacher.student_id",
        back_populates="student",
        cascade="all, delete-orphan",
    )
    suggestions_created = relationship(
        "PracticeSuggestion",
        foreign_keys="PracticeSuggestion.teacher_id",
        back_populates="teacher",
        cascade="all, delete-orphan",
    )
    suggestions_received = relationship(
        "PracticeSuggestion",
        foreign_keys="PracticeSuggestion.student_id",
        back_populates="student",
        cascade="all, delete-orphan",
    )
    lessons = relationship(
        "Lesson",
        back_populates="creator",
        cascade="all, delete-orphan",
    )
    practice_sessions = relationship(
        "PracticeSession",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    course_enrollments = relationship(
        "CourseEnrollment",
        back_populates="student",
        cascade="all, delete-orphan",
    )
    classes_taught = relationship(
        "Classroom",
        back_populates="teacher",
        cascade="all, delete-orphan",
    )
    comments = relationship(
        "Comment",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    reviews = relationship(
        "Review",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    activity_logs = relationship(
        "ActivityLog",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    practice_histories = relationship(
        "PracticeHistory",
        back_populates="student",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<User id={self.id} email={self.email!r}>"
