from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.core.database import Base


class ThongBao(Base):
    """Bảng thông báo gửi đến người dùng."""
    __tablename__ = "ThongBao"

    ma_thong_bao = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ma_nguoi_dung = Column(
        Integer,
        ForeignKey("NguoiDung.ma_nguoi_dung", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    tieu_de = Column(String(255), nullable=False)
    noi_dung = Column(Text, nullable=True)
    loai_thong_bao = Column(String(100), nullable=True)   # vd: "goi_y", "he_thong", ...
    duong_dan = Column(String(500), nullable=True)         # URL điều hướng khi click
    da_doc = Column(Boolean, nullable=False, default=False)
    ngay_tao = Column(DateTime, nullable=False, default=datetime.utcnow)

    # ── Quan hệ ──────────────────────────────────────────────────────────────
    nguoi_dung = relationship("NguoiDung", back_populates="thong_bao")

    def __repr__(self) -> str:
        return f"<ThongBao id={self.ma_thong_bao} tieu_de={self.tieu_de!r}>"
