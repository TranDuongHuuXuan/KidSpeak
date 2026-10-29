from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class NguoiDung(Base):
    """Bảng người dùng — dùng chung cho Admin, GiaoVien, HocSinh."""
    __tablename__ = "NguoiDung"

    ma_nguoi_dung = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ten_dang_nhap = Column(String(100), nullable=False, unique=True, index=True)
    email = Column(String(255), nullable=False, unique=True, index=True)
    mat_khau = Column(String(255), nullable=False)

    # FK → VaiTro
    ma_vai_tro = Column(
        Integer,
        ForeignKey("VaiTro.ma_vai_tro", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    ngay_sinh = Column(DateTime, nullable=True)
    anh_dai_dien = Column(String(500), nullable=True)           # URL ảnh (MinIO)
    trang_thai = Column(Boolean, nullable=False, default=True)  # True = active
    ngay_tao = Column(DateTime, nullable=False, default=datetime.utcnow)
    ngay_cap_nhat = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    # ── Quan hệ ──────────────────────────────────────────────────────────────
    vai_tro = relationship("VaiTro", back_populates="nguoi_dung")

    # 1-N: NguoiDung → ThongBao
    thong_bao = relationship(
        "ThongBao",
        back_populates="nguoi_dung",
        cascade="all, delete-orphan",
    )

    # 1-N: NguoiDung (GiaoVien) → HocSinh_GiaoVien
    lop_hoc_giao_vien = relationship(
        "HocSinh_GiaoVien",
        foreign_keys="HocSinh_GiaoVien.ma_giao_vien",
        back_populates="giao_vien",
        cascade="all, delete-orphan",
    )

    # 1-N: NguoiDung (HocSinh) → HocSinh_GiaoVien
    lop_hoc_hoc_sinh = relationship(
        "HocSinh_GiaoVien",
        foreign_keys="HocSinh_GiaoVien.ma_hoc_sinh",
        back_populates="hoc_sinh",
        cascade="all, delete-orphan",
    )

    # 1-N: NguoiDung (GiaoVien) → GoiY_LuyenTap (người gợi ý)
    goi_y_da_tao = relationship(
        "GoiY_LuyenTap",
        foreign_keys="GoiY_LuyenTap.ma_giao_vien",
        back_populates="giao_vien",
        cascade="all, delete-orphan",
    )

    # 1-N: NguoiDung (HocSinh) → GoiY_LuyenTap (người nhận gợi ý)
    goi_y_nhan_duoc = relationship(
        "GoiY_LuyenTap",
        foreign_keys="GoiY_LuyenTap.ma_hoc_sinh",
        back_populates="hoc_sinh",
        cascade="all, delete-orphan",
    )

    # 1-N: NguoiDung (người tạo) → BaiHoc
    bai_hoc = relationship(
        "BaiHoc",
        back_populates="nguoi_tao",
        cascade="all, delete-orphan",
    )

    # 1-N: NguoiDung (HocSinh) → PhienLuyenTap
    phien_luyen_tap = relationship(
        "PhienLuyenTap",
        back_populates="nguoi_dung",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<NguoiDung id={self.ma_nguoi_dung} email={self.email!r}>"
