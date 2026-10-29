from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.core.database import Base


class PhienLuyenTap(Base):
    """Bảng phiên luyện tập — mỗi lần học sinh bắt đầu luyện tập là một phiên."""
    __tablename__ = "PhienLuyenTap"

    ma_phien = Column(Integer, primary_key=True, index=True, autoincrement=True)

    # FK → NguoiDung (HocSinh)
    ma_nguoi_dung = Column(
        Integer,
        ForeignKey("NguoiDung.ma_nguoi_dung", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    ngay_bat_dau = Column(DateTime, nullable=False, default=datetime.utcnow)
    ngay_ket_thuc = Column(DateTime, nullable=True)
    tong_so_diem = Column(Float, nullable=True, default=0.0)  # Tổng điểm phiên

    # ── Quan hệ ──────────────────────────────────────────────────────────────
    nguoi_dung = relationship("NguoiDung", back_populates="phien_luyen_tap")

    # 1-N: PhienLuyenTap → ChiTietLuyenTap
    chi_tiet_luyen_tap = relationship(
        "ChiTietLuyenTap",
        back_populates="phien_luyen_tap",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<PhienLuyenTap id={self.ma_phien} nguoi_dung={self.ma_nguoi_dung}>"
