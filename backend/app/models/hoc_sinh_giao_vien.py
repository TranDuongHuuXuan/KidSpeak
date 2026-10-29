from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.core.database import Base


class HocSinh_GiaoVien(Base):
    """Bảng liên kết N-N giữa GiaoVien và HocSinh (cùng bảng NguoiDung)."""
    __tablename__ = "HocSinh_GiaoVien"

    ma_quan_he = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ma_giao_vien = Column(
        Integer,
        ForeignKey("NguoiDung.ma_nguoi_dung", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    ma_hoc_sinh = Column(
        Integer,
        ForeignKey("NguoiDung.ma_nguoi_dung", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    ngay_tao = Column(DateTime, nullable=False, default=datetime.utcnow)

    # ── Quan hệ ──────────────────────────────────────────────────────────────
    giao_vien = relationship(
        "NguoiDung",
        foreign_keys=[ma_giao_vien],
        back_populates="lop_hoc_giao_vien",
    )
    hoc_sinh = relationship(
        "NguoiDung",
        foreign_keys=[ma_hoc_sinh],
        back_populates="lop_hoc_hoc_sinh",
    )

    def __repr__(self) -> str:
        return (
            f"<HocSinh_GiaoVien id={self.ma_quan_he} "
            f"gv={self.ma_giao_vien} hs={self.ma_hoc_sinh}>"
        )
