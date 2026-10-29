# ─── Import toàn bộ models để Alembic autogenerate phát hiện đủ bảng ─────────
# Thứ tự import quan trọng: Base → độc lập → phụ thuộc

from app.core.database import Base  # noqa: F401  (phải import trước)

from app.models.vai_tro import VaiTro                          # noqa: F401
from app.models.quyen import Quyen                              # noqa: F401
from app.models.vai_tro_quyen import VaiTro_Quyen               # noqa: F401
from app.models.nguoi_dung import NguoiDung                     # noqa: F401
from app.models.thong_bao import ThongBao                       # noqa: F401
from app.models.hoc_sinh_giao_vien import HocSinh_GiaoVien      # noqa: F401
from app.models.danh_muc_bai_hoc import DanhMucBaiHoc           # noqa: F401
from app.models.bai_hoc import BaiHoc                           # noqa: F401
from app.models.tu_vung import TuVung                           # noqa: F401
from app.models.goi_y_luyen_tap import GoiY_LuyenTap            # noqa: F401
from app.models.phien_luyen_tap import PhienLuyenTap             # noqa: F401
from app.models.chi_tiet_luyen_tap import ChiTietLuyenTap       # noqa: F401

__all__ = [
    "Base",
    "VaiTro",
    "Quyen",
    "VaiTro_Quyen",
    "NguoiDung",
    "ThongBao",
    "HocSinh_GiaoVien",
    "DanhMucBaiHoc",
    "BaiHoc",
    "TuVung",
    "GoiY_LuyenTap",
    "PhienLuyenTap",
    "ChiTietLuyenTap",
]
