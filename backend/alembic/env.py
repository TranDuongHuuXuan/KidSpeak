"""
Alembic env.py — KidSpeak Backend
Tự động lấy DATABASE_URL từ .env qua app.config.config.Settings.
"""
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# ── Import Base và kích hoạt tất cả models ──────────────────────────────────
# import app.models sẽ chạy __init__.py → import từng model → register vào Base.metadata
from app.core.database import Base  # noqa: F401
import app.models  # noqa: F401

# ── Lấy DATABASE_URL từ Settings (.env) ─────────────────────────────────────
from app.config.config import settings

# ── Alembic config object ────────────────────────────────────────────────────
config = context.config

# Inject URL động — ưu tiên hơn giá trị trong [alembic] sqlalchemy.url
config.set_main_option("sqlalchemy.url", settings.database_url)

# Cấu hình logging từ alembic.ini (nếu có)
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata chứa toàn bộ bảng → Alembic so sánh để autogenerate
target_metadata = Base.metadata


# ────────────────────────────────────────────────────────────────────────────
def run_migrations_offline() -> None:
    """
    Chạy migration ở chế độ 'offline' — không cần kết nối DB thực sự.
    Hữu ích để xem SQL sẽ được tạo ra: alembic upgrade head --sql
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """
    Chạy migration ở chế độ 'online' — kết nối DB thực và áp dụng thay đổi.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,       # Phát hiện thay đổi kiểu cột
            compare_server_default=True,  # Phát hiện thay đổi default value
        )
        with context.begin_transaction():
            context.run_migrations()


# ── Entry point ──────────────────────────────────────────────────────────────
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
