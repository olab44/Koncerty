from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from typing import List

from src.database import get_session
from users.service import decode_app_token
from .schemas import AnnouncementCreate, AnnouncementInfo
from .service import create_announcement, get_announcements
from users.models import User, Member


router = APIRouter()


@router.post("/createAnnouncement", status_code=201, response_model=AnnouncementInfo)
def post_announcement(
    request: AnnouncementCreate,
    db: Session = Depends(get_session),
    token: str = Header(..., alias="Authorization"),
):
    # try:
    user_data = decode_app_token(token)
    email = user_data.get("email")
    existing_user = db.query(User).filter(User.email == email).first()
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    existing_member = db.query(Member).filter(Member.user_id == existing_user.id, Member.group_id == request.group_id).first()
    if not existing_member:
        raise HTTPException(status_code=404, detail="User is not a member of the group")

    if existing_member.role != "Kapelmistrz":
        raise HTTPException(status_code=403, detail="User must have Kapelmistrz role")
    
    # if user_data.get("role") not in ["Kapelmistrz", "Koordynator"]:
    #     raise HTTPException(status_code=403, detail="Access denied")
    return create_announcement(db, existing_user.id, request)
    # except HTTPException as e:
    #     raise e
    # except Exception:
    #     raise HTTPException(status_code=401, detail="Invalid or expired token")


@router.get("/announcements", response_model=List[AnnouncementInfo])
def fetch_announcements(
    group_id: int = None,
    db: Session = Depends(get_session),
    token: str = Header(..., alias="Authorization"),
):
    try:
        user_data = decode_app_token(token)
        return get_announcements(db, group_id)
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
