from fastapi import APIRouter
from fastapi import Depends, HTTPException, Header
from sqlalchemy.orm import Session
from typing import List

from database import get_session
from users.models import User
from .service import get_user_events, create_event
from .schemas import EventInfo, CreateEventRequest
from users.service import decode_app_token

router = APIRouter()

@router.get("/findEvents", response_model=List[EventInfo])
def get_events_structure(group_id: int, db: Session = Depends(get_session), token: str = Header(..., alias="Authorization")):
    user_data = decode_app_token(token)

    result = get_user_events(db, user_data.get("email"), group_id)
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return result

@router.post("/createEvent", status_code=201)
def create_group(request: CreateEventRequest, db: Session = Depends(get_session), token: str = Header(..., alias="Authorization")):
    user_data = decode_app_token(token)
    
    new_event = create_event(db, user_data.get("email"), request)
    return {"created": new_event}
