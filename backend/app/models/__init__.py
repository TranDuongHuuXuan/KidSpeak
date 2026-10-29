# ─── Import all models so Alembic autogenerate can detect all tables ──────────
# Import order matters: Base → independent → dependent

from app.core.database import Base  # noqa: F401  (must be first)

from app.models.role import Role                                    # noqa: F401
from app.models.permission import Permission                        # noqa: F401
from app.models.role_permission import RolePermission              # noqa: F401
from app.models.user import User                                    # noqa: F401
from app.models.notification import Notification                    # noqa: F401
from app.models.student_teacher import StudentTeacher              # noqa: F401
from app.models.lesson_category import LessonCategory              # noqa: F401
from app.models.lesson import Lesson                               # noqa: F401
from app.models.vocabulary import Vocabulary                        # noqa: F401
from app.models.practice_suggestion import PracticeSuggestion      # noqa: F401
from app.models.practice_session import PracticeSession            # noqa: F401
from app.models.practice_detail import PracticeDetail              # noqa: F401

__all__ = [
    "Base",
    "Role",
    "Permission",
    "RolePermission",
    "User",
    "Notification",
    "StudentTeacher",
    "LessonCategory",
    "Lesson",
    "Vocabulary",
    "PracticeSuggestion",
    "PracticeSession",
    "PracticeDetail",
]
