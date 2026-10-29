from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.core.database import Base


class BaiHoc(Base):
    """Bảng bài học trong hệ thống."""
    __tablename__ = "BaiHoc"

    ma_bai_hoc = Column(Integer, primary_key=True, index=True, autoincrement=True)

    # FK → DanhMucBaiHoc
    ma_danh_muc = Column(
        Integer,
        ForeignKey("DanhMucBaiHoc.ma_danh_muc", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    # FK → NguoiDung (người tạo bài học)
    ma_nguoi_dung = Column(
        Integer,
        ForeignKey("NguoiDung.ma_nguoi_dung", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    tieu_de = Column(String(300), nullable=False)
    mo_ta = Column(Text, nullable=True)
    cap_do = Column(String(50), nullable=True)      # vd: "Beginner", "Intermediate", ...
    thu_tu = Column(Integer, nullable=True, default=0)
    trang_thai = Column(Boolean, nullable=False, default=True)  # True = published
    ngay_tao = Column(DateTime, nullable=False, default=datetime.utcnow)
    ngay_cap_nhat = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    # ── Quan hệ ──────────────────────────────────────────────────────────────
    danh_muc = relationship("DanhMucBaiHoc", back_populates="bai_hoc")
    nguoi_tao = relationship("NguoiDung", back_populates="bai_hoc")

    # 1-N: BaiHoc → TuVung
    tu_vung = relationship(
        "TuVung",
        back_populates="bai_hoc",
        cascade="all, delete-orphan",
    )

    # 1-N: BaiHoc → GoiY_LuyenTap
    goi_y_luyen_tap = relationship(
        "GoiY_LuyenTap",
        back_populates="bai_hoc",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<BaiHoc id={self.ma_bai_hoc} tieu_de={self.tieu_de!r}>"
