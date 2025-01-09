from fastapi import APIRouter
from fastapi import Depends, HTTPException, Header
from sqlalchemy.orm import Session
from typing import List

from database import get_session
from users.models import User
from .service import get_user_events, create_event
from .schemas import EventInfo, CreateEventRequest
from users.service import get_user_data

router = APIRouter()

@router.get("/findEvents", response_model=List[EventInfo])
def get_events_structure(group_id: int, db: Session = Depends(get_session), token: str = Header(..., alias="Authorization")):
    user_data = get_user_data(token)

    result = get_user_events(db, user_data.get("email"), group_id)
    return result

@router.post("/createEvent", status_code=201)
def create_group(request: CreateEventRequest, db: Session = Depends(get_session), token: str = Header(..., alias="Authorization")):
    user_data = get_user_data(token)

    new_event = create_event(db, user_data.get("email"), request)
    return {"created": new_event}
