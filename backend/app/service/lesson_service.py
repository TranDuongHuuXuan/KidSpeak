import logging
from math import ceil

from fastapi import UploadFile
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.lesson import Lesson
from app.models.lesson_category import LessonCategory
from app.models.user import User
from app.repository.lesson_repository import LessonRepository
from app.schemas.lesson_schema import LessonCategoryInput, LessonInput
from app.service.media_storage_service import (
    MediaStorageError,
    MediaValidationError,
    media_storage_service,
)

logger = logging.getLogger(__name__)


class LessonNotFoundError(Exception):
    pass


class LessonConflictError(Exception):
    pass


class LessonCategoryNotFoundError(Exception):
    pass


class LessonService:
    def __init__(self, repository=LessonRepository, media=media_storage_service):
        self.repository = repository
        self.media = media

    @staticmethod
    def pagination(skip: int, limit: int, total: int) -> dict:
        page = skip // limit + 1
        pages = ceil(total / limit) if total else 0
        return {
            "skip": skip,
            "limit": limit,
            "total": total,
            "current_page": page,
            "total_pages": pages,
            "has_next": page < pages,
            "has_prev": page > 1,
        }

    def _image_url(self, object_key: str | None) -> str | None:
        if not object_key:
            return None
        return self.media.get_file_url(object_key)

    def _category_data(self, category: LessonCategory) -> dict:
        return {
            "id": category.id,
            "name": category.name,
            "description": category.description,
            "image": self._image_url(category.image),
            "order": category.order or 0,
            "created_at": category.created_at,
            "updated_at": category.updated_at,
        }

    def _lesson_data(self, lesson: Lesson) -> dict:
        return {
            "id": lesson.id,
            "category_id": lesson.category_id,
            "category_name": lesson.category.name if lesson.category else None,
            "created_by": lesson.creator_id,
            "creator_name": lesson.creator.full_name if lesson.creator else None,
            "title": lesson.title,
            "description": lesson.description,
            "level": lesson.level,
            "order": lesson.order or 0,
            "image": self._image_url(lesson.image),
            "is_published": lesson.is_published,
            "created_at": lesson.created_at,
            "updated_at": lesson.updated_at,
        }

    @staticmethod
    def _safe_delete_image(media, object_key: str | None, allowed_prefix: str) -> None:
        if not object_key or not object_key.startswith(allowed_prefix):
            return
        try:
            media.delete_file(object_key)
        except Exception:
            logger.exception("Could not remove an unreferenced lesson image.")

    @staticmethod
    def _cleanup_uploaded_image(media, object_key: str | None) -> None:
        if not object_key:
            return
        try:
            media.delete_file(object_key)
        except Exception:
            logger.exception("Could not clean up an unreferenced uploaded lesson image.")

    async def _upload_image(self, image: UploadFile | None, folder: str) -> str | None:
        if image is None:
            return None
        uploaded = await self.media.upload_file(image, folder=folder, media_type="image")
        return uploaded["object_key"]

    def list_categories(self, db: Session, skip: int, limit: int):
        categories, total = self.repository.list_categories(db, skip, limit)
        return [self._category_data(item) for item in categories], self.pagination(
            skip, limit, total
        )

    def get_category(self, db: Session, category_id: int) -> dict:
        category = self.repository.get_category(db, category_id)
        if not category:
            raise LessonNotFoundError("Không tìm thấy danh mục bài học.")
        return self._category_data(category)

    async def create_category(
        self,
        db: Session,
        data: LessonCategoryInput,
        image: UploadFile | None,
    ) -> dict:
        name = data.name.strip()
        if not name:
            raise ValueError("Tên danh mục không được để trống.")
        if self.repository.category_name_exists(db, name):
            raise LessonConflictError("Tên danh mục đã tồn tại.")

        object_key = await self._upload_image(image, "lesson-categories")
        category = LessonCategory(
            name=name,
            description=data.description.strip() if data.description else None,
            order=data.order,
            image=object_key,
        )
        try:
            category = self.repository.create_category(db, category)
        except IntegrityError as error:
            db.rollback()
            self._cleanup_uploaded_image(self.media, object_key)
            raise LessonConflictError("Tên danh mục đã tồn tại.") from error
        except Exception:
            db.rollback()
            self._cleanup_uploaded_image(self.media, object_key)
            raise
        return self._category_data(category)

    async def update_category(
        self,
        db: Session,
        category_id: int,
        data: LessonCategoryInput,
        image: UploadFile | None,
    ) -> dict:
        category = self.repository.get_category(db, category_id)
        if not category:
            raise LessonNotFoundError("Không tìm thấy danh mục bài học.")
        name = data.name.strip()
        if not name:
            raise ValueError("Tên danh mục không được để trống.")
        if self.repository.category_name_exists(db, name, exclude_id=category_id):
            raise LessonConflictError("Tên danh mục đã tồn tại.")

        old_image = category.image
        new_image = await self._upload_image(image, f"lesson-categories/{category_id}")
        category.name = name
        category.description = data.description.strip() if data.description else None
        category.order = data.order
        if new_image:
            category.image = new_image
        try:
            category = self.repository.save_category(db, category)
        except IntegrityError as error:
            db.rollback()
            self._cleanup_uploaded_image(self.media, new_image)
            raise LessonConflictError("Tên danh mục đã tồn tại.") from error
        except Exception:
            db.rollback()
            self._cleanup_uploaded_image(self.media, new_image)
            raise
        if new_image and old_image != new_image:
            self._safe_delete_image(self.media, old_image, "lesson-categories/")
        return self._category_data(category)

    def delete_category(self, db: Session, category_id: int) -> None:
        category = self.repository.get_category(db, category_id)
        if not category:
            raise LessonNotFoundError("Không tìm thấy danh mục bài học.")
        if self.repository.count_category_lessons(db, category_id):
            raise LessonConflictError(
                "Không thể xóa danh mục đang có bài học. Hãy chuyển hoặc xóa các bài học trước."
            )
        image = category.image
        self.repository.delete_category(db, category)
        self._safe_delete_image(self.media, image, "lesson-categories/")

    async def list_lessons(
        self,
        db: Session,
        *,
        skip: int,
        limit: int,
        category_id: int | None,
        level: str | None,
        is_published: bool | None,
        search: str | None,
    ):
        lessons, total = self.repository.list_lessons(
            db,
            skip=skip,
            limit=limit,
            category_id=category_id,
            level=level,
            is_published=is_published,
            search=search,
        )
        return [self._lesson_data(item) for item in lessons], self.pagination(
            skip, limit, total
        )

    def get_lesson(self, db: Session, lesson_id: int) -> dict:
        lesson = self.repository.get_lesson(db, lesson_id)
        if not lesson:
            raise LessonNotFoundError("Không tìm thấy bài học.")
        return self._lesson_data(lesson)

    async def create_lesson(
        self,
        db: Session,
        data: LessonInput,
        current_user: User,
        image: UploadFile | None,
    ) -> dict:
        if not self.repository.get_category(db, data.category_id):
            raise LessonCategoryNotFoundError("Danh mục bài học không tồn tại.")
        title = data.title.strip()
        if not title:
            raise ValueError("Tên chủ đề không được để trống.")

        object_key = await self._upload_image(image, "lessons")
        lesson = Lesson(
            category_id=data.category_id,
            creator_id=current_user.id,
            title=title,
            description=data.description.strip() if data.description else None,
            level=data.level,
            order=data.order,
            image=object_key,
            is_published=data.is_published,
        )
        try:
            lesson = self.repository.create_lesson(db, lesson)
        except Exception:
            db.rollback()
            self._cleanup_uploaded_image(self.media, object_key)
            raise
        return self._lesson_data(lesson)

    async def update_lesson(
        self,
        db: Session,
        lesson_id: int,
        data: LessonInput,
        image: UploadFile | None,
    ) -> dict:
        lesson = self.repository.get_lesson(db, lesson_id)
        if not lesson:
            raise LessonNotFoundError("Không tìm thấy bài học.")
        if not self.repository.get_category(db, data.category_id):
            raise LessonCategoryNotFoundError("Danh mục bài học không tồn tại.")
        title = data.title.strip()
        if not title:
            raise ValueError("Tên chủ đề không được để trống.")

        old_image = lesson.image
        new_image = await self._upload_image(image, f"lessons/{lesson_id}")
        lesson.category_id = data.category_id
        lesson.title = title
        lesson.description = data.description.strip() if data.description else None
        lesson.level = data.level
        lesson.order = data.order
        lesson.is_published = data.is_published
        if new_image:
            lesson.image = new_image
        try:
            lesson = self.repository.save_lesson(db, lesson)
        except Exception:
            db.rollback()
            self._cleanup_uploaded_image(self.media, new_image)
            raise
        if new_image and old_image != new_image:
            self._safe_delete_image(self.media, old_image, "lessons/")
        return self._lesson_data(lesson)

    def delete_lesson(self, db: Session, lesson_id: int) -> None:
        lesson = self.repository.get_lesson(db, lesson_id)
        if not lesson:
            raise LessonNotFoundError("Không tìm thấy bài học.")
        if self.repository.has_lesson_references(db, lesson_id):
            raise LessonConflictError(
                "Không thể xóa bài học đang có từ vựng, bình luận, đánh giá hoặc gợi ý luyện tập."
            )
        image = lesson.image
        self.repository.delete_lesson(db, lesson)
        self._safe_delete_image(self.media, image, "lessons/")


lesson_service = LessonService()
