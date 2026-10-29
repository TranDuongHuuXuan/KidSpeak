from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
try:
    from app.config.config import settings
except ImportError:
    from .config import settings
# Database URL (lấy từ biến môi trường hoặc tự động ghép từ DB_HOST, DB_USER, ...)
DATABASE_URL = getattr(settings, "database_url", None) or settings.DATABASE_URL

# Tạo engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    echo=False
)

# SessionLocal
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class với SQLAlchemy 2.x style (DeclarativeBase)
Base = declarative_base()


# Dependency để lấy database session
def get_db():
    """
    Dependency function để lấy database session.
    Sử dụng với FastAPI: db: Session = Depends(get_db)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()