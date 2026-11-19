from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, HTTPException, Query, Request, UploadFile, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import require_roles
from app.schemas.base_schema import DataResponse, PaginationInfo
from app.schemas.lesson_schema import (
    LessonCategoryInput,
    LessonCategoryResponse,
    LessonInput,
    LessonLevel,
    LessonResponse,
)
from app.service.lesson_service import (
    LessonCategoryNotFoundError,
    LessonConflictError,
    LessonNotFoundError,
    lesson_service,
)
from app.service.media_storage_service import (
    MediaStorageError,
    MediaTooLargeError,
    MediaValidationError,
)

lesson_router = APIRouter(
    tags=["Expert lesson management"],
    dependencies=[Depends(require_roles("EXPERT", "ADMIN"))],
)


def _handle_service_error(error: Exception) -> HTTPException:
    if isinstance(error, LessonNotFoundError):
        return HTTPException(status_code=404, detail=str(error))
    if isinstance(error, LessonCategoryNotFoundError):
        return HTTPException(status_code=404, detail=str(error))
    if isinstance(error, LessonConflictError):
        return HTTPException(status_code=409, detail=str(error))
    if isinstance(error, (MediaTooLargeError, MediaValidationError, ValueError)):
        return HTTPException(status_code=400, detail=str(error))
    if isinstance(error, MediaStorageError):
        return HTTPException(status_code=502, detail=str(error))
    raise error


def _category_input(name: str, description: str | None, order: int) -> LessonCategoryInput:
    try:
        return LessonCategoryInput(name=name, description=description, order=order)
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error


def _lesson_input(
    category_id: int,
    title: str,
    description: str | None,
    level: LessonLevel,
    order: int,
    is_published: bool,
) -> LessonInput:
    try:
        return LessonInput(
            category_id=category_id,
            title=title,
            description=description,
            level=level,
            order=order,
            is_published=is_published,
        )
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error


@lesson_router.get(
    "/lesson-categories",
    response_model=DataResponse[list[LessonCategoryResponse]],
)
def list_categories(
    request: Request,
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
):
    try:
        data, pagination = lesson_service.list_categories(db, skip, limit)
        return DataResponse(data=data, pagination=PaginationInfo(**pagination))
    except Exception as error:
        raise _handle_service_error(error)


@lesson_router.get(
    "/lesson-categories/{category_id}",
    response_model=DataResponse[LessonCategoryResponse],
)
def get_category(category_id: int, request: Request, db: Session = Depends(get_db)):
    try:
        return DataResponse(data=lesson_service.get_category(db, category_id))
    except Exception as error:
        raise _handle_service_error(error)


@lesson_router.post(
    "/lesson-categories",
    response_model=DataResponse[LessonCategoryResponse],
    status_code=status.HTTP_201_CREATED,
)
async def create_category(
    request: Request,
    name: Annotated[str, Form(min_length=1, max_length=200)],
    description: Annotated[str | None, Form()] = None,
    order: Annotated[int, Form(ge=0)] = 0,
    image: UploadFile | None = File(default=None),
    db: Session = Depends(get_db),
):
    data = _category_input(name, description, order)
    try:
        result = await lesson_service.create_category(db, data, image)
        return DataResponse(data=result, code="201", message="Đã tạo danh mục bài học.")
    except Exception as error:
        raise _handle_service_error(error)


@lesson_router.put(
    "/lesson-categories/{category_id}",
    response_model=DataResponse[LessonCategoryResponse],
)
async def update_category(
    category_id: int,
    request: Request,
    name: Annotated[str, Form(min_length=1, max_length=200)],
    description: Annotated[str | None, Form()] = None,
    order: Annotated[int, Form(ge=0)] = 0,
    image: UploadFile | None = File(default=None),
    db: Session = Depends(get_db),
):
    data = _category_input(name, description, order)
    try:
        result = await lesson_service.update_category(db, category_id, data, image)
        return DataResponse(data=result, message="Đã cập nhật danh mục bài học.")
    except Exception as error:
        raise _handle_service_error(error)


@lesson_router.delete(
    "/lesson-categories/{category_id}",
    response_model=DataResponse[None],
)
def delete_category(category_id: int, request: Request, db: Session = Depends(get_db)):
    try:
        lesson_service.delete_category(db, category_id)
        return DataResponse(data=None, message="Đã xóa danh mục bài học.")
    except Exception as error:
        raise _handle_service_error(error)


@lesson_router.get("/lessons", response_model=DataResponse[list[LessonResponse]])
async def list_lessons(
    request: Request,
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    category_id: int | None = Query(None, ge=1),
    level: LessonLevel | None = None,
    is_published: bool | None = None,
    search: str | None = Query(None, max_length=300),
):
    try:
        data, pagination = await lesson_service.list_lessons(
            db,
            skip=skip,
            limit=limit,
            category_id=category_id,
            level=level,
            is_published=is_published,
            search=search,
        )
        return DataResponse(data=data, pagination=PaginationInfo(**pagination))
    except Exception as error:
        raise _handle_service_error(error)


@lesson_router.get("/lessons/{lesson_id}", response_model=DataResponse[LessonResponse])
def get_lesson(lesson_id: int, request: Request, db: Session = Depends(get_db)):
    try:
        return DataResponse(data=lesson_service.get_lesson(db, lesson_id))
    except Exception as error:
        raise _handle_service_error(error)


@lesson_router.post(
    "/lessons",
    response_model=DataResponse[LessonResponse],
    status_code=status.HTTP_201_CREATED,
)
async def create_lesson(
    request: Request,
    category_id: Annotated[int, Form(ge=1)],
    title: Annotated[str, Form(min_length=1, max_length=300)],
    level: Annotated[LessonLevel, Form()],
    order: Annotated[int, Form(ge=0)] = 0,
    description: Annotated[str | None, Form()] = None,
    is_published: Annotated[bool, Form()] = True,
    image: UploadFile | None = File(default=None),
    db: Session = Depends(get_db),
):
    current_user = request.state.user
    data = _lesson_input(category_id, title, description, level, order, is_published)
    try:
        result = await lesson_service.create_lesson(db, data, current_user, image)
        return DataResponse(data=result, code="201", message="Đã tạo bài học.")
    except Exception as error:
        raise _handle_service_error(error)


@lesson_router.put("/lessons/{lesson_id}", response_model=DataResponse[LessonResponse])
async def update_lesson(
    lesson_id: int,
    request: Request,
    category_id: Annotated[int, Form(ge=1)],
    title: Annotated[str, Form(min_length=1, max_length=300)],
    level: Annotated[LessonLevel, Form()],
    order: Annotated[int, Form(ge=0)] = 0,
    description: Annotated[str | None, Form()] = None,
    is_published: Annotated[bool, Form()] = True,
    image: UploadFile | None = File(default=None),
    db: Session = Depends(get_db),
):
    data = _lesson_input(category_id, title, description, level, order, is_published)
    try:
        result = await lesson_service.update_lesson(db, lesson_id, data, image)
        return DataResponse(data=result, message="Đã cập nhật bài học.")
    except Exception as error:
        raise _handle_service_error(error)


@lesson_router.delete("/lessons/{lesson_id}", response_model=DataResponse[None])
def delete_lesson(lesson_id: int, request: Request, db: Session = Depends(get_db)):
    try:
        lesson_service.delete_lesson(db, lesson_id)
        return DataResponse(data=None, message="Đã xóa bài học.")
    except Exception as error:
        raise _handle_service_error(error)
