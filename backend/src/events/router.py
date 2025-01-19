from fastapi import APIRouter
from fastapi import Depends, HTTPException, Header
from sqlalchemy.orm import Session
from typing import List

from database import get_session
from users.models import User
from .service import get_user_events, create_event, edit_event, remove_event
from .schemas import EventInfo, CreateEventRequest, EditEventRequest, RemoveEventRequest
from users.service import get_user_data

router = APIRouter()

@router.get("/findEvents", response_model=List[EventInfo])
def get_events_structure(group_id: int, db: Session = Depends(get_session), token: str = Header(..., alias="Authorization")):
    user_data = get_user_data(token)

    result = get_user_events(db, user_data.get("email"), group_id)
    return result

@router.post("/createEvent", status_code=201)
def create_ev(request: CreateEventRequest, db: Session = Depends(get_session), token: str = Header(..., alias="Authorization")):
    user_data = get_user_data(token)

    new_event = create_event(db, user_data.get("email"), request)
    return {"created": new_event}


@router.post("/editEvent", status_code=201)
def edit_ev(request: EditEventRequest, db: Session = Depends(get_session), token: str = Header(..., alias="Authorization")):
    user_data = get_user_data(token)

    new_event = edit_event(db, user_data.get("email"), request)
    return {"edited": new_event}

@router.post("/removeEvent", status_code=201)
def rm_event(request: RemoveEventRequest, db: Session = Depends(get_session), token: str = Header(..., alias="Authorization")):
    user_data = get_user_data(token)

    deleted_event = remove_event(db, user_data.get("email"), request)
    return {"removed": deleted_event}

