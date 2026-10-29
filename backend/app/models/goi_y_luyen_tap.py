from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from app.core.database import Base


class GoiY_LuyenTap(Base):
    """Bảng gợi ý luyện tập — GiaoVien gửi gợi ý cho HocSinh về một bài học."""
    __tablename__ = "GoiY_LuyenTap"

    ma_goi_y = Column(Integer, primary_key=True, index=True, autoincrement=True)

    # FK → NguoiDung (GiaoVien — người tạo gợi ý)
    ma_giao_vien = Column(
        Integer,
        ForeignKey("NguoiDung.ma_nguoi_dung", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # FK → NguoiDung (HocSinh — người nhận gợi ý)
    ma_hoc_sinh = Column(
        Integer,
        ForeignKey("NguoiDung.ma_nguoi_dung", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # FK → BaiHoc
    ma_bai_hoc = Column(
        Integer,
        ForeignKey("BaiHoc.ma_bai_hoc", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    noi_dung = Column(Text, nullable=True)
    da_doc = Column(Boolean, nullable=False, default=False)
    ngay_tao = Column(DateTime, nullable=False, default=datetime.utcnow)

    # ── Quan hệ ──────────────────────────────────────────────────────────────
    giao_vien = relationship(
        "NguoiDung",
        foreign_keys=[ma_giao_vien],
        back_populates="goi_y_da_tao",
    )
    hoc_sinh = relationship(
        "NguoiDung",
        foreign_keys=[ma_hoc_sinh],
        back_populates="goi_y_nhan_duoc",
    )
    bai_hoc = relationship("BaiHoc", back_populates="goi_y_luyen_tap")

    def __repr__(self) -> str:
        return (
            f"<GoiY_LuyenTap id={self.ma_goi_y} "
            f"gv={self.ma_giao_vien} hs={self.ma_hoc_sinh}>"
        )
