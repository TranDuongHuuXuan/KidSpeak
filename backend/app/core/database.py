from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from app.config.config import settings


# ─── Engine ──────────────────────────────────────────────────────────────────
engine = create_engine(
    settings.database_url,
    echo=settings.debug,          # In câu SQL ra console khi DEBUG=True
    pool_pre_ping=True,           # Kiểm tra kết nối trước khi dùng
    pool_size=10,
    max_overflow=20,
)

# ─── Session factory ──────────────────────────────────────────────────────────
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)

# ─── Base class cho tất cả models ────────────────────────────────────────────
class Base(DeclarativeBase):
    """Base class dùng chung cho mọi SQLAlchemy Model trong dự án."""
    pass


# ─── Dependency dùng trong FastAPI ───────────────────────────────────────────
def get_db():
    """Yield một session DB, tự đóng sau mỗi request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
