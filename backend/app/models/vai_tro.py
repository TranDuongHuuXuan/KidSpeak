from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship

from app.core.database import Base


class VaiTro(Base):
    """Bảng vai trò người dùng (Admin, GiaoVien, HocSinh, ...)."""
    __tablename__ = "VaiTro"

    ma_vai_tro = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ten_vai_tro = Column(String(100), nullable=False, unique=True)
    mo_ta = Column(Text, nullable=True)

    # ── Quan hệ ──────────────────────────────────────────────────────────────
    # 1-N: VaiTro → VaiTro_Quyen
    vai_tro_quyen = relationship(
        "VaiTro_Quyen",
        back_populates="vai_tro",
        cascade="all, delete-orphan",
    )

    # 1-N: VaiTro → NguoiDung
    nguoi_dung = relationship(
        "NguoiDung",
        back_populates="vai_tro",
    )

    def __repr__(self) -> str:
        return f"<VaiTro id={self.ma_vai_tro} ten={self.ten_vai_tro!r}>"
