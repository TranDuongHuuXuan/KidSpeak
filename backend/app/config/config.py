from functools import lru_cache
from typing import List, Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    KidSpeak Backend Settings.
    Toàn bộ cấu hình được nạp từ file .env thông qua alias của từng Field.
    """
    # Cấu hình ứng dụng
    app_name: str = Field(default="KidSpeak-Backend", alias="APP_NAME")
    app_env: str = Field(default="development", alias="APP_ENV")
    debug: bool = Field(default=True, alias="DEBUG")
    host: str = Field(default="0.0.0.0", alias="HOST")
    port: int = Field(default=8000, alias="PORT")

    # Bảo mật & JWT
    secret_key: str = Field(..., alias="SECRET_KEY")
    algorithm: str = Field(default="HS256", alias="ALGORITHM")
    access_token_expire_minutes: int = Field(default=60, alias="ACCESS_TOKEN_EXPIRE_MINUTES")

    # Cơ sở dữ liệu (PostgreSQL Local)
    db_host: str = Field(default="localhost", alias="DB_HOST")
    db_port: int = Field(default=5432, alias="DB_PORT")
    db_user: str = Field(default="postgres", alias="DB_USER")
    db_password: str = Field(..., alias="DB_PASSWORD")
    db_name: str = Field(default="kidspeak_db", alias="DB_NAME")
    database_url_env: Optional[str] = Field(default=None, alias="DATABASE_URL")

    # CORS
    allowed_origins: str = Field(default="http://localhost:5173,http://127.0.0.1:5173", alias="ALLOWED_ORIGINS")

    # AI Service
    ai_service_url: str = Field(default="http://localhost:8001", alias="AI_SERVICE_URL")

    # Media Storage (MinIO)
    minio_endpoint: str = Field(default="localhost:9000", alias="MINIO_ENDPOINT")
    minio_root_user: str = Field(default="minioadmin", alias="MINIO_ROOT_USER")
    minio_root_password: str = Field(default="minioadmin", alias="MINIO_ROOT_PASSWORD")
    minio_bucket_name: str = Field(default="kidspeak-media", alias="MINIO_BUCKET_NAME")
    minio_secure: bool = Field(default=False, alias="MINIO_SECURE")

    # Cấu hình nạp .env (Tương thích Pydantic v2 & pydantic-settings)
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    @property
    def database_url(self) -> str:
        """Tự động xây dựng connection string PostgreSQL chuẩn driver psycopg2"""
        url = self.database_url_env
        if not url:
            url = f"postgresql+psycopg2://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
        elif url.startswith("postgresql://"):
            url = url.replace("postgresql://", "postgresql+psycopg2://", 1)
        return url

    @property
    def cors_origins(self) -> List[str]:
        """Tách chuỗi CORS từ .env thành danh sách origins"""
        return [origin.strip() for origin in self.allowed_origins.split(",") if origin.strip()]

    def __getattr__(self, name: str):
        """Cho phép gọi biến dạng chữ HOA hoặc chữ thường (ví dụ: settings.DB_HOST hoặc settings.db_host)"""
        lower = name.lower()
        if lower in self.__dict__:
            return self.__dict__[lower]
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")


@lru_cache
def get_settings() -> Settings:
    """Dependency Provider có cache để nạp Settings singleton"""
    return Settings()


# Instance singleton để import trực tiếp ở các module khác
settings = get_settings()
