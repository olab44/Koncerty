from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from . import models, schemas
from src.database import get_db
from users import models as user_models
from service import send_email_notification
from datetime import datetime

router = APIRouter()


@router.post("/announcements/", response_model=schemas.Announcement)
def create_announcement(
    announcement: schemas.AnnouncementCreate, db: Session = Depends(get_db)
):
    db_announcement = models.Alert(
        content=announcement.content,
        date_sent=datetime.utcnow()
    )
    db.add(db_announcement)
    db.commit()
    db.refresh(db_announcement)

    if announcement.group_id:
        group_members = db.query(user_models.Member).filter(
            user_models.Member.group_id == announcement.group_id
        ).all()

        for member in group_members:
            user = db.query(user_models.User).filter(user_models.User.id == member.user_id).first()
            if user:
                send_email_notification(user.email, db_announcement)
                db.add(models.Recipient(member_id=member.id, alert_id=db_announcement.id))
                db.commit()

    if announcement.user_id:
        user = db.query(user_models.User).filter(user_models.User.id == announcement.user_id).first()
        if user:
            send_email_notification(user.email, db_announcement)
            db.add(models.Recipient(member_id=announcement.user_id, alert_id=db_announcement.id))
            db.commit()

    return db_announcement
