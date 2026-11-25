from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.notification import Notification
from app.schemas.base_schema import DataResponse

notification_router = APIRouter(prefix="/notifications", tags=["Notifications"])


@notification_router.get("", dependencies=[Depends(get_current_user)])
def list_notifications(request: Request, db: Session = Depends(get_db)):
    rows = db.query(Notification).filter(Notification.user_id == request.state.user.id).order_by(Notification.created_at.desc()).limit(100).all()
    return DataResponse(data=[{"id": row.id, "title": row.title, "message": row.content, "type": row.type, "url": row.url, "is_read": row.is_read, "created_at": row.created_at} for row in rows])


@notification_router.patch("/{notification_id}/read", dependencies=[Depends(get_current_user)])
def mark_read(notification_id: int, request: Request, db: Session = Depends(get_db)):
    row = db.query(Notification).filter(Notification.id == notification_id, Notification.user_id == request.state.user.id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Notification not found.")
    row.is_read = True
    db.commit()
    return DataResponse(data={"id": row.id, "is_read": row.is_read})
