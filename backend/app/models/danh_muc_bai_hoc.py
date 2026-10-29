from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.orm import relationship

from app.core.database import Base


class DanhMucBaiHoc(Base):
    """Bảng danh mục / chủ đề bài học."""
    __tablename__ = "DanhMucBaiHoc"

    ma_danh_muc = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ten_danh_muc = Column(String(200), nullable=False, unique=True)
    mo_ta = Column(Text, nullable=True)
    thu_tu = Column(Integer, nullable=True, default=0)  # Thứ tự hiển thị
    ngay_tao = Column(DateTime, nullable=False, default=datetime.utcnow)

    # ── Quan hệ ──────────────────────────────────────────────────────────────
    # 1-N: DanhMucBaiHoc → BaiHoc
    bai_hoc = relationship(
        "BaiHoc",
        back_populates="danh_muc",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<DanhMucBaiHoc id={self.ma_danh_muc} ten={self.ten_danh_muc!r}>"
