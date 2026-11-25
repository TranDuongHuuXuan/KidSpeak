from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, HTTPException, Path, Query, Request, UploadFile, status
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User
from app.core.security import normalize_role_name, require_roles
from app.schemas.base_schema import DataResponse, PaginationInfo
from app.schemas.expert_upgrade_schema import (
    AdminExpertUpgradeResponse,
    ExpertUpgradeInput,
    ExpertUpgradeResponse,
    ExpertUpgradeReviewInput,
)
from app.schemas.user_schema import UserSchema
from app.service.expert_upgrade_service import ExpertUpgradeError, expert_upgrade_service
from app.service.media_storage_service import (
    MediaNotFoundError,
    MediaStorageError,
    MediaTooLargeError,
    MediaValidationError,
    media_storage_service,
)

upgrade_router = APIRouter(prefix="/expert-upgrade-requests", tags=["Expert upgrade"])


def _fail(error: Exception):
    if isinstance(error, ExpertUpgradeError):
        raise HTTPException(status_code=error.status_code, detail=str(error))
    if isinstance(error, MediaTooLargeError):
        raise HTTPException(status_code=413, detail=str(error))
    if isinstance(error, MediaValidationError):
        raise HTTPException(status_code=400, detail=str(error))
    if isinstance(error, MediaNotFoundError):
        raise HTTPException(status_code=404, detail=str(error))
    if isinstance(error, MediaStorageError):
        raise HTTPException(status_code=502, detail=str(error))
    raise error


def _admin_response(request):
    applicant = UserSchema.model_validate(request.user).model_copy(
        update={
            "role_name": normalize_role_name(request.user.role.name if request.user.role else None)
        }
    )
    avatar_url = None
    avatar_key = request.user.avatar
    if avatar_key and avatar_key.startswith(f"users/avatars/{request.user_id}/"):
        try:
            avatar_url = media_storage_service.get_file_url(avatar_key)
        except (MediaNotFoundError, MediaStorageError):
            avatar_url = None
    return {
        **ExpertUpgradeResponse.model_validate(request).model_dump(),
        "applicant_name": request.user.full_name,
        "applicant_email": request.user.email,
        "applicant": applicant,
        "reviewer_name": request.reviewer.full_name if request.reviewer else None,
        "applicant_avatar_url": avatar_url,
    }


@upgrade_router.post("", response_model=DataResponse[ExpertUpgradeResponse], status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_roles("STUDENT"))])
async def submit_upgrade(
    request: Request,
    reason: Annotated[str, Form(...)],
    specialty: Annotated[str, Form()] = "",
    experience: Annotated[str, Form()] = "",
    introduction: Annotated[str, Form()] = "",
    files: Annotated[list[UploadFile] | None, File()] = None,
    previous_request_id: Annotated[int | None, Form()] = None,
    keep_document_keys: Annotated[list[str] | None, Form()] = None,
    db: Session = Depends(get_db),
):
    try:
        data = ExpertUpgradeInput(specialty=specialty, experience=experience, reason=reason, introduction=introduction)
        result = await expert_upgrade_service.submit(
            db, request.state.user, data, files or [], previous_request_id, keep_document_keys or []
        )
        return DataResponse(data=result, code="201", message="Đã gửi hồ sơ nâng cấp.")
    except Exception as error:
        if isinstance(error, ValidationError):
            raise HTTPException(status_code=422, detail=error.errors()) from error
        _fail(error)


@upgrade_router.get("/mine", response_model=DataResponse[list[ExpertUpgradeResponse]], dependencies=[Depends(require_roles("STUDENT"))])
def list_my_upgrades(request: Request, db: Session = Depends(get_db)):
    return DataResponse(data=expert_upgrade_service.list_own(db, request.state.user.id))


@upgrade_router.get("", response_model=DataResponse[list[AdminExpertUpgradeResponse]], dependencies=[Depends(require_roles("ADMIN"))])
def list_upgrades(
    status_filter: str | None = Query(None, alias="status", pattern="^(pending|approved|rejected|activated)$"),
    search: str | None = Query(None, max_length=120),
    email: str | None = Query(None, max_length=255),
    reason: str | None = Query(None, max_length=2000),
    experience: str | None = Query(None, max_length=4000),
    page: int = Query(1, ge=1), limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    items, total = expert_upgrade_service.list_admin(
        db, status_filter, search, email, reason, experience, (page - 1) * limit, limit
    )
    pages = (total + limit - 1) // limit
    return DataResponse(data=[_admin_response(item) for item in items], pagination=PaginationInfo(skip=(page - 1) * limit, limit=limit, total=total, current_page=page, total_pages=pages, has_next=page < pages, has_prev=page > 1))


@upgrade_router.get("/{request_id}", response_model=DataResponse[ExpertUpgradeResponse | AdminExpertUpgradeResponse], dependencies=[Depends(require_roles("STUDENT", "ADMIN"))])
def get_upgrade(request: Request, request_id: int = Path(ge=1), db: Session = Depends(get_db)):
    try:
        is_admin = request.state.user.role.name.upper() == "ADMIN"
        result = expert_upgrade_service.get_authorized(db, request_id, request.state.user, is_admin)
        return DataResponse(data=_admin_response(result) if is_admin else result)
    except Exception as error:
        _fail(error)


@upgrade_router.post("/{request_id}/review", response_model=DataResponse[AdminExpertUpgradeResponse], dependencies=[Depends(require_roles("ADMIN"))])
def review_upgrade(request: Request, data: ExpertUpgradeReviewInput, request_id: int = Path(ge=1), db: Session = Depends(get_db)):
    try:
        result = expert_upgrade_service.review(db, request_id, request.state.user, data.status, data.review_note)
        return DataResponse(data=_admin_response(result), message="Đã cập nhật kết quả xét duyệt.")
    except Exception as error:
        _fail(error)


@upgrade_router.get("/{request_id}/documents/{document_index}/url", dependencies=[Depends(require_roles("STUDENT", "ADMIN"))])
def get_document_url(request: Request, request_id: int = Path(ge=1), document_index: int = Path(ge=0), download: bool = Query(False), db: Session = Depends(get_db)):
    try:
        is_admin = request.state.user.role.name.upper() == "ADMIN"
        document = expert_upgrade_service.document_for_user(db, request_id, document_index, request.state.user, is_admin)
        url = media_storage_service.get_file_url(document["file_key"], document["file_name"], download)
        return DataResponse(data={"url": url, **document})
    except Exception as error:
        _fail(error)


@upgrade_router.post("/activate", response_model=DataResponse[dict], dependencies=[Depends(require_roles("STUDENT"))])
def activate_upgrade(request: Request, db: Session = Depends(get_db)):
    try:
        activated = expert_upgrade_service.activate(db, request.state.user)
        role_id = db.query(User.role_id).filter(User.id == activated.user_id).scalar()
        return DataResponse(data={"role": "EXPERT", "role_id": role_id, "verification_status": activated.status}, message="Your account has been successfully upgraded to Teacher.")
    except Exception as error:
        _fail(error)
