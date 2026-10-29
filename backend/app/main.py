import socket
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.config import settings
from app.core.logger import logger

def check_connection(host: str, port: int, timeout: float = 1.0) -> bool:
    try:
        with socket.create_connection((host, int(port)), timeout=timeout):
            return True
    except (socket.timeout, ConnectionRefusedError, OSError):
        return False

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup & Shutdown event handler"""
    # 1. Hiển thị banner KidSpeak
    logger.show_banner(app_name=settings.APP_NAME, version="1.0.0", env=settings.APP_ENV)

    # 2. Kiểm tra kết nối cơ sở dữ liệu (PostgreSQL Local)
    logger.info(f"🔌 Connecting to database at {settings.DB_HOST}:{settings.DB_PORT}...")
    if check_connection(settings.DB_HOST, settings.DB_PORT):
        logger.db_connected(f"PostgreSQL at {settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}")
    else:
        logger.db_error(f"Cannot reach PostgreSQL at {settings.DB_HOST}:{settings.DB_PORT} (Hãy đảm bảo PostgreSQL Local đang chạy trên cổng {settings.DB_PORT})")

    # 3. Kiểm tra kết nối MinIO Storage
    try:
        parts = settings.MINIO_ENDPOINT.split(":")
        m_host = parts[0]
        m_port = int(parts[1]) if len(parts) > 1 else 9000
        if check_connection(m_host, m_port):
            logger.minio_connected(f"MinIO at {settings.MINIO_ENDPOINT} (Bucket: {settings.MINIO_BUCKET_NAME})")
        else:
            logger.minio_error(f"Cannot reach MinIO at {settings.MINIO_ENDPOINT} (chưa bật MinIO container)")
    except Exception as e:
        logger.minio_error(str(e))

    # 4. Hiển thị thông tin tài liệu API
    doc_host = "127.0.0.1" if settings.HOST == "0.0.0.0" else settings.HOST

    logger.info("-" * 70)
    logger.info("📚 API Documentation:")
    logger.info(f"   Swagger UI: http://{doc_host}:{settings.PORT}/docs")
    logger.info(f"   ReDoc:      http://{doc_host}:{settings.PORT}/redoc")
    logger.info("-" * 70 + "\n")

    yield

    # Shutdown handler
    logger.info("👋 KidSpeak Backend is shutting down...")

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description="Backend API for KidSpeak - AI-powered Vietnamese pronunciation learning platform for children",
    lifespan=lifespan,
)

# Cấu hình CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {
        "status": "online",
        "service": settings.APP_NAME,
        "environment": settings.APP_ENV,
        "docs_url": "/docs",
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "services": {
            "api": "up",
            "ai_service_url": settings.AI_SERVICE_URL,
            "minio_endpoint": settings.MINIO_ENDPOINT,
            "db_host": f"{settings.DB_HOST}:{settings.DB_PORT}",
        }
    }
