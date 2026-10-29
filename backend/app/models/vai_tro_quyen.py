from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base


class VaiTro_Quyen(Base):
    """Bảng trung gian N-N giữa VaiTro và Quyen."""
    __tablename__ = "VaiTro_Quyen"

    # ── Composite Primary Key ─────────────────────────────────────────────────
    ma_vai_tro = Column(
        Integer,
        ForeignKey("VaiTro.ma_vai_tro", ondelete="CASCADE"),
        primary_key=True,
    )
    ma_quyen = Column(
        Integer,
        ForeignKey("Quyen.ma_quyen", ondelete="CASCADE"),
        primary_key=True,
    )

    # ── Quan hệ ──────────────────────────────────────────────────────────────
    vai_tro = relationship("VaiTro", back_populates="vai_tro_quyen")
    quyen = relationship("Quyen", back_populates="vai_tro_quyen")

    def __repr__(self) -> str:
        return f"<VaiTro_Quyen vai_tro={self.ma_vai_tro} quyen={self.ma_quyen}>"
