from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from app.models.comment import Comment
from app.models.lesson import Lesson
from app.models.lesson_category import LessonCategory
from app.models.practice_suggestion import PracticeSuggestion
from app.models.review import Review
from app.models.vocabulary import Vocabulary


class LessonRepository:
    @staticmethod
    def list_categories(db: Session, skip: int, limit: int):
        query = db.query(LessonCategory)
        total = query.count()
        items = (
            query.order_by(LessonCategory.order.asc(), LessonCategory.id.asc())
            .offset(skip)
            .limit(limit)
            .all()
        )
        return items, total

    @staticmethod
    def get_category(db: Session, category_id: int):
        return db.query(LessonCategory).filter(LessonCategory.id == category_id).first()

    @staticmethod
    def count_category_lessons(db: Session, category_id: int) -> int:
        return (
            db.query(func.count(Lesson.id))
            .filter(Lesson.category_id == category_id)
            .scalar()
            or 0
        )

    @staticmethod
    def list_lessons(
        db: Session,
        *,
        skip: int,
        limit: int,
        category_id: int | None,
        level: str | None,
        is_published: bool | None,
        search: str | None,
    ):
        query = db.query(Lesson).options(
            joinedload(Lesson.category),
            joinedload(Lesson.creator),
        )
        if category_id is not None:
            query = query.filter(Lesson.category_id == category_id)
        if level is not None:
            query = query.filter(Lesson.level == level)
        if is_published is not None:
            query = query.filter(Lesson.is_published.is_(is_published))
        if search:
            query = query.filter(Lesson.title.ilike(f"%{search.strip()}%"))

        total = query.count()
        items = (
            query.order_by(Lesson.order.asc(), Lesson.id.asc())
            .offset(skip)
            .limit(limit)
            .all()
        )
        return items, total

    @staticmethod
    def get_lesson(db: Session, lesson_id: int):
        return (
            db.query(Lesson)
            .options(joinedload(Lesson.category), joinedload(Lesson.creator))
            .filter(Lesson.id == lesson_id)
            .first()
        )

    @staticmethod
    def category_name_exists(db: Session, name: str, exclude_id: int | None = None) -> bool:
        query = db.query(LessonCategory.id).filter(
            func.lower(LessonCategory.name) == name.strip().lower()
        )
        if exclude_id is not None:
            query = query.filter(LessonCategory.id != exclude_id)
        return query.first() is not None

    @staticmethod
    def has_lesson_references(db: Session, lesson_id: int) -> bool:
        reference_queries = (
            db.query(Vocabulary.id).filter(Vocabulary.lesson_id == lesson_id),
            db.query(PracticeSuggestion.id).filter(PracticeSuggestion.lesson_id == lesson_id),
            db.query(Comment.id).filter(Comment.lesson_id == lesson_id),
            db.query(Review.id).filter(Review.lesson_id == lesson_id),
        )
        return any(query.first() is not None for query in reference_queries)

    @staticmethod
    def create_category(db: Session, category: LessonCategory) -> LessonCategory:
        db.add(category)
        db.commit()
        db.refresh(category)
        return category

    @staticmethod
    def save_category(db: Session, category: LessonCategory) -> LessonCategory:
        db.add(category)
        db.commit()
        db.refresh(category)
        return category

    @staticmethod
    def delete_category(db: Session, category: LessonCategory) -> None:
        db.delete(category)
        db.commit()

    @staticmethod
    def create_lesson(db: Session, lesson: Lesson) -> Lesson:
        db.add(lesson)
        db.commit()
        db.refresh(lesson)
        return lesson

    @staticmethod
    def save_lesson(db: Session, lesson: Lesson) -> Lesson:
        db.add(lesson)
        db.commit()
        db.refresh(lesson)
        return lesson

    @staticmethod
    def delete_lesson(db: Session, lesson: Lesson) -> None:
        db.delete(lesson)
        db.commit()
