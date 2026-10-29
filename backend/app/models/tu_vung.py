from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class TuVung(Base):
    """Bảng từ vựng thuộc một bài học."""
    __tablename__ = "TuVung"

    ma_tu_vung = Column(Integer, primary_key=True, index=True, autoincrement=True)

    # FK → BaiHoc
    ma_bai_hoc = Column(
        Integer,
        ForeignKey("BaiHoc.ma_bai_hoc", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    tu_chuan = Column(String(200), nullable=False)          # Từ gốc (English word)
    phien_am = Column(String(200), nullable=True)            # IPA / phiên âm
    duong_dan_anh = Column(String(500), nullable=True)       # URL ảnh minh hoạ (MinIO)
    am_thanh_mau = Column(String(500), nullable=True)        # URL audio mẫu chuẩn (MinIO)
    thu_tu = Column(Integer, nullable=True, default=0)       # Thứ tự trong bài học
    ngay_tao = Column(DateTime, nullable=False, default=datetime.utcnow)

    # ── Quan hệ ──────────────────────────────────────────────────────────────
    bai_hoc = relationship("BaiHoc", back_populates="tu_vung")

    # 1-N: TuVung → ChiTietLuyenTap
    chi_tiet_luyen_tap = relationship(
        "ChiTietLuyenTap",
        back_populates="tu_vung",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<TuVung id={self.ma_tu_vung} tu={self.tu_chuan!r}>"
