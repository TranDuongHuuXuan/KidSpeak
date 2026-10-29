from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.core.database import Base


class ChiTietLuyenTap(Base):
    """Bảng chi tiết luyện tập — lưu kết quả phát âm AI chấm điểm từng từ vựng."""
    __tablename__ = "ChiTietLuyenTap"

    ma_chi_tiet = Column(Integer, primary_key=True, index=True, autoincrement=True)

    # FK → PhienLuyenTap
    ma_phien = Column(
        Integer,
        ForeignKey("PhienLuyenTap.ma_phien", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # FK → TuVung
    ma_tu_vung = Column(
        Integer,
        ForeignKey("TuVung.ma_tu_vung", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # File ghi âm của học sinh (URL MinIO)
    duong_dan_file_ghi = Column(String(500), nullable=True)

    # Văn bản AI nhận dạng từ file ghi âm (Speech-to-Text output)
    van_ban_ai_nhan_dien = Column(Text, nullable=True)

    # Các thành phần điểm phát âm do AI trả về (0.0 – 100.0)
    am_thanh_dau = Column(Float, nullable=True)       # Điểm phụ âm đầu
    am_thanh_cuoi = Column(Float, nullable=True)      # Điểm phụ âm cuối / vần
    am_thanh_dieu = Column(Float, nullable=True)      # Điểm thanh điệu
    am_thanh_chi_tiet = Column(Float, nullable=True)  # Điểm tổng chi tiết / tổng hợp

    ngay_tao = Column(DateTime, nullable=False, default=datetime.utcnow)

    # ── Quan hệ ──────────────────────────────────────────────────────────────
    phien_luyen_tap = relationship("PhienLuyenTap", back_populates="chi_tiet_luyen_tap")
    tu_vung = relationship("TuVung", back_populates="chi_tiet_luyen_tap")

    def __repr__(self) -> str:
        return (
            f"<ChiTietLuyenTap id={self.ma_chi_tiet} "
            f"phien={self.ma_phien} tu_vung={self.ma_tu_vung}>"
        )
