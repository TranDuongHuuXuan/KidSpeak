"""Rename Vietnamese database identifiers to English.

Revision ID: 69786eb07024
Revises: 81326314b204
Create Date: 2026-10-29
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "69786eb07024"
down_revision: Union[str, Sequence[str], None] = "81326314b204"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


TABLE_RENAMES = (
    ("DanhMucBaiHoc", "lesson_categories"),
    ("Quyen", "permissions"),
    ("VaiTro", "roles"),
    ("NguoiDung", "users"),
    ("VaiTro_Quyen", "role_permissions"),
    ("BaiHoc", "lessons"),
    ("HocSinh_GiaoVien", "student_teachers"),
    ("PhienLuyenTap", "practice_sessions"),
    ("ThongBao", "notifications"),
    ("GoiY_LuyenTap", "practice_suggestions"),
    ("TuVung", "vocabularies"),
    ("ChiTietLuyenTap", "practice_details"),
)

COLUMN_RENAMES = (
    ("lesson_categories", "ma_danh_muc", "id"),
    ("lesson_categories", "ten_danh_muc", "name"),
    ("lesson_categories", "mo_ta", "description"),
    ("lesson_categories", "thu_tu", "order"),
    ("lesson_categories", "ngay_tao", "created_at"),
    ("permissions", "ma_quyen", "id"),
    ("permissions", "ten_quyen", "name"),
    ("permissions", "mo_ta", "description"),
    ("roles", "ma_vai_tro", "id"),
    ("roles", "ten_vai_tro", "name"),
    ("roles", "mo_ta", "description"),
    ("users", "ma_nguoi_dung", "id"),
    ("users", "ten_dang_nhap", "username"),
    ("users", "mat_khau", "password"),
    ("users", "ma_vai_tro", "role_id"),
    ("users", "ngay_sinh", "date_of_birth"),
    ("users", "anh_dai_dien", "avatar"),
    ("users", "trang_thai", "is_active"),
    ("users", "ngay_tao", "created_at"),
    ("users", "ngay_cap_nhat", "updated_at"),
    ("role_permissions", "ma_vai_tro", "role_id"),
    ("role_permissions", "ma_quyen", "permission_id"),
    ("lessons", "ma_bai_hoc", "id"),
    ("lessons", "ma_danh_muc", "category_id"),
    ("lessons", "ma_nguoi_dung", "creator_id"),
    ("lessons", "tieu_de", "title"),
    ("lessons", "mo_ta", "description"),
    ("lessons", "cap_do", "level"),
    ("lessons", "thu_tu", "order"),
    ("lessons", "trang_thai", "is_published"),
    ("lessons", "ngay_tao", "created_at"),
    ("lessons", "ngay_cap_nhat", "updated_at"),
    ("student_teachers", "ma_quan_he", "id"),
    ("student_teachers", "ma_giao_vien", "teacher_id"),
    ("student_teachers", "ma_hoc_sinh", "student_id"),
    ("student_teachers", "ngay_tao", "created_at"),
    ("practice_sessions", "ma_phien", "id"),
    ("practice_sessions", "ma_nguoi_dung", "user_id"),
    ("practice_sessions", "ngay_bat_dau", "started_at"),
    ("practice_sessions", "ngay_ket_thuc", "ended_at"),
    ("practice_sessions", "tong_so_diem", "total_score"),
    ("notifications", "ma_thong_bao", "id"),
    ("notifications", "ma_nguoi_dung", "user_id"),
    ("notifications", "tieu_de", "title"),
    ("notifications", "noi_dung", "content"),
    ("notifications", "loai_thong_bao", "type"),
    ("notifications", "duong_dan", "url"),
    ("notifications", "da_doc", "is_read"),
    ("notifications", "ngay_tao", "created_at"),
    ("practice_suggestions", "ma_goi_y", "id"),
    ("practice_suggestions", "ma_giao_vien", "teacher_id"),
    ("practice_suggestions", "ma_hoc_sinh", "student_id"),
    ("practice_suggestions", "ma_bai_hoc", "lesson_id"),
    ("practice_suggestions", "noi_dung", "content"),
    ("practice_suggestions", "da_doc", "is_read"),
    ("practice_suggestions", "ngay_tao", "created_at"),
    ("vocabularies", "ma_tu_vung", "id"),
    ("vocabularies", "ma_bai_hoc", "lesson_id"),
    ("vocabularies", "tu_chuan", "word"),
    ("vocabularies", "phien_am", "pronunciation"),
    ("vocabularies", "duong_dan_anh", "image_url"),
    ("vocabularies", "am_thanh_mau", "audio_url"),
    ("vocabularies", "thu_tu", "order"),
    ("vocabularies", "ngay_tao", "created_at"),
    ("practice_details", "ma_chi_tiet", "id"),
    ("practice_details", "ma_phien", "session_id"),
    ("practice_details", "ma_tu_vung", "vocabulary_id"),
    ("practice_details", "duong_dan_file_ghi", "recording_url"),
    ("practice_details", "van_ban_ai_nhan_dien", "ai_transcription"),
    ("practice_details", "am_thanh_dau", "initial_consonant_score"),
    ("practice_details", "am_thanh_cuoi", "final_consonant_score"),
    ("practice_details", "am_thanh_dieu", "tone_score"),
    ("practice_details", "am_thanh_chi_tiet", "overall_score"),
    ("practice_details", "ngay_tao", "created_at"),
)

INDEX_RENAMES = (
    ("ix_DanhMucBaiHoc_ma_danh_muc", "ix_lesson_categories_id"),
    ("ix_Quyen_ma_quyen", "ix_permissions_id"),
    ("ix_VaiTro_ma_vai_tro", "ix_roles_id"),
    ("ix_NguoiDung_email", "ix_users_email"),
    ("ix_NguoiDung_ma_nguoi_dung", "ix_users_id"),
    ("ix_NguoiDung_ma_vai_tro", "ix_users_role_id"),
    ("ix_NguoiDung_ten_dang_nhap", "ix_users_username"),
    ("ix_BaiHoc_ma_bai_hoc", "ix_lessons_id"),
    ("ix_BaiHoc_ma_danh_muc", "ix_lessons_category_id"),
    ("ix_BaiHoc_ma_nguoi_dung", "ix_lessons_creator_id"),
    ("ix_HocSinh_GiaoVien_ma_giao_vien", "ix_student_teachers_teacher_id"),
    ("ix_HocSinh_GiaoVien_ma_hoc_sinh", "ix_student_teachers_student_id"),
    ("ix_HocSinh_GiaoVien_ma_quan_he", "ix_student_teachers_id"),
    ("ix_PhienLuyenTap_ma_nguoi_dung", "ix_practice_sessions_user_id"),
    ("ix_PhienLuyenTap_ma_phien", "ix_practice_sessions_id"),
    ("ix_ThongBao_ma_nguoi_dung", "ix_notifications_user_id"),
    ("ix_ThongBao_ma_thong_bao", "ix_notifications_id"),
    ("ix_GoiY_LuyenTap_ma_bai_hoc", "ix_practice_suggestions_lesson_id"),
    ("ix_GoiY_LuyenTap_ma_giao_vien", "ix_practice_suggestions_teacher_id"),
    ("ix_GoiY_LuyenTap_ma_goi_y", "ix_practice_suggestions_id"),
    ("ix_GoiY_LuyenTap_ma_hoc_sinh", "ix_practice_suggestions_student_id"),
    ("ix_TuVung_ma_bai_hoc", "ix_vocabularies_lesson_id"),
    ("ix_TuVung_ma_tu_vung", "ix_vocabularies_id"),
    ("ix_ChiTietLuyenTap_ma_chi_tiet", "ix_practice_details_id"),
    ("ix_ChiTietLuyenTap_ma_phien", "ix_practice_details_session_id"),
    ("ix_ChiTietLuyenTap_ma_tu_vung", "ix_practice_details_vocabulary_id"),
)

CONSTRAINT_RENAMES = (
    ("lesson_categories", "DanhMucBaiHoc_pkey", "lesson_categories_pkey"),
    (
        "lesson_categories",
        "DanhMucBaiHoc_ten_danh_muc_key",
        "lesson_categories_name_key",
    ),
    ("permissions", "Quyen_pkey", "permissions_pkey"),
    ("permissions", "Quyen_ten_quyen_key", "permissions_name_key"),
    ("roles", "VaiTro_pkey", "roles_pkey"),
    ("roles", "VaiTro_ten_vai_tro_key", "roles_name_key"),
    ("users", "NguoiDung_pkey", "users_pkey"),
    (
        "users",
        "NguoiDung_ma_vai_tro_fkey",
        "users_role_id_fkey",
    ),
    ("role_permissions", "VaiTro_Quyen_pkey", "role_permissions_pkey"),
    (
        "role_permissions",
        "VaiTro_Quyen_ma_vai_tro_fkey",
        "role_permissions_role_id_fkey",
    ),
    (
        "role_permissions",
        "VaiTro_Quyen_ma_quyen_fkey",
        "role_permissions_permission_id_fkey",
    ),
    ("lessons", "BaiHoc_pkey", "lessons_pkey"),
    ("lessons", "BaiHoc_ma_danh_muc_fkey", "lessons_category_id_fkey"),
    ("lessons", "BaiHoc_ma_nguoi_dung_fkey", "lessons_creator_id_fkey"),
    ("student_teachers", "HocSinh_GiaoVien_pkey", "student_teachers_pkey"),
    (
        "student_teachers",
        "HocSinh_GiaoVien_ma_giao_vien_fkey",
        "student_teachers_teacher_id_fkey",
    ),
    (
        "student_teachers",
        "HocSinh_GiaoVien_ma_hoc_sinh_fkey",
        "student_teachers_student_id_fkey",
    ),
    ("practice_sessions", "PhienLuyenTap_pkey", "practice_sessions_pkey"),
    (
        "practice_sessions",
        "PhienLuyenTap_ma_nguoi_dung_fkey",
        "practice_sessions_user_id_fkey",
    ),
    ("notifications", "ThongBao_pkey", "notifications_pkey"),
    (
        "notifications",
        "ThongBao_ma_nguoi_dung_fkey",
        "notifications_user_id_fkey",
    ),
    ("practice_suggestions", "GoiY_LuyenTap_pkey", "practice_suggestions_pkey"),
    (
        "practice_suggestions",
        "GoiY_LuyenTap_ma_bai_hoc_fkey",
        "practice_suggestions_lesson_id_fkey",
    ),
    (
        "practice_suggestions",
        "GoiY_LuyenTap_ma_giao_vien_fkey",
        "practice_suggestions_teacher_id_fkey",
    ),
    (
        "practice_suggestions",
        "GoiY_LuyenTap_ma_hoc_sinh_fkey",
        "practice_suggestions_student_id_fkey",
    ),
    ("vocabularies", "TuVung_pkey", "vocabularies_pkey"),
    (
        "vocabularies",
        "TuVung_ma_bai_hoc_fkey",
        "vocabularies_lesson_id_fkey",
    ),
    ("practice_details", "ChiTietLuyenTap_pkey", "practice_details_pkey"),
    (
        "practice_details",
        "ChiTietLuyenTap_ma_phien_fkey",
        "practice_details_session_id_fkey",
    ),
    (
        "practice_details",
        "ChiTietLuyenTap_ma_tu_vung_fkey",
        "practice_details_vocabulary_id_fkey",
    ),
)

SEQUENCE_RENAMES = (
    ("DanhMucBaiHoc_ma_danh_muc_seq", "lesson_categories_id_seq"),
    ("Quyen_ma_quyen_seq", "permissions_id_seq"),
    ("VaiTro_ma_vai_tro_seq", "roles_id_seq"),
    ("NguoiDung_ma_nguoi_dung_seq", "users_id_seq"),
    ("BaiHoc_ma_bai_hoc_seq", "lessons_id_seq"),
    ("HocSinh_GiaoVien_ma_quan_he_seq", "student_teachers_id_seq"),
    ("PhienLuyenTap_ma_phien_seq", "practice_sessions_id_seq"),
    ("ThongBao_ma_thong_bao_seq", "notifications_id_seq"),
    ("GoiY_LuyenTap_ma_goi_y_seq", "practice_suggestions_id_seq"),
    ("TuVung_ma_tu_vung_seq", "vocabularies_id_seq"),
    ("ChiTietLuyenTap_ma_chi_tiet_seq", "practice_details_id_seq"),
)


def _rename_constraint(table_name: str, old_name: str, new_name: str) -> None:
    op.execute(
        sa.text(
            f'ALTER TABLE "{table_name}" '
            f'RENAME CONSTRAINT "{old_name}" TO "{new_name}"'
        )
    )


def upgrade() -> None:
    for old_name, new_name in TABLE_RENAMES:
        op.rename_table(old_name, new_name)

    for table_name, old_name, new_name in COLUMN_RENAMES:
        op.alter_column(table_name, old_name, new_column_name=new_name)

    for table_name, old_name, new_name in CONSTRAINT_RENAMES:
        _rename_constraint(table_name, old_name, new_name)

    for old_name, new_name in INDEX_RENAMES:
        op.execute(sa.text(f'ALTER INDEX IF EXISTS "{old_name}" RENAME TO "{new_name}"'))

    for old_name, new_name in SEQUENCE_RENAMES:
        op.execute(
            sa.text(
                f'ALTER SEQUENCE IF EXISTS "{old_name}" RENAME TO "{new_name}"'
            )
        )


def downgrade() -> None:
    for table_name, old_name, new_name in reversed(CONSTRAINT_RENAMES):
        _rename_constraint(table_name, new_name, old_name)

    for old_name, new_name in reversed(INDEX_RENAMES):
        op.execute(sa.text(f'ALTER INDEX IF EXISTS "{new_name}" RENAME TO "{old_name}"'))

    for table_name, old_name, new_name in reversed(COLUMN_RENAMES):
        op.alter_column(table_name, new_name, new_column_name=old_name)

    for old_name, new_name in reversed(TABLE_RENAMES):
        op.rename_table(new_name, old_name)

    for old_name, new_name in reversed(SEQUENCE_RENAMES):
        op.execute(
            sa.text(
                f'ALTER SEQUENCE IF EXISTS "{new_name}" RENAME TO "{old_name}"'
            )
        )
