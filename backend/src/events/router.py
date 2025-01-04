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
def get_events_structure(db: Session = Depends(get_session), token: str = Header(..., alias="Authorization")):
    user_data = decode_app_token(token)


    result = get_user_events(db, user_data.get("email"))
    print(result)
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return result

@router.post("/createEvent", status_code=201)
def create_group(request: CreateEventRequest, db: Session = Depends(get_session), token: str = Header(..., alias="Authorization")):
    user_data = decode_app_token(token)
    user = db.query(User).filter(User.email == user_data.get("email")).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User not found {user_data}")

    new_event = create_event(db, request)
    return {
        "event_id": new_event.event_id,
        "name": new_event.name,
        "description": new_event.description,
    }
