from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship

from app.core.database import Base


class Quyen(Base):
    """Bảng quyền hạn (permission) trong hệ thống."""
    __tablename__ = "Quyen"

    ma_quyen = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ten_quyen = Column(String(150), nullable=False, unique=True)
    mo_ta = Column(Text, nullable=True)

    # ── Quan hệ ──────────────────────────────────────────────────────────────
    # 1-N: Quyen → VaiTro_Quyen
    vai_tro_quyen = relationship(
        "VaiTro_Quyen",
        back_populates="quyen",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Quyen id={self.ma_quyen} ten={self.ten_quyen!r}>"
