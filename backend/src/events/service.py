import os
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException
from dotenv import load_dotenv
from typing import List

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from .schemas import EventInfo, CreateEventRequest, GetEventInfo, Participant, CompositionInfo
from users.models import User, Member
from users.models import Event, Participation, Composition

def get_calendar_service(token: str):
    try:
        load_dotenv()
        GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
        GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
        credentials = Credentials(token)
        service = build('calendar', 'v3', credentials=credentials)

        return service
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Google Calendar service error: {str(e)}")

def get_setlist_info(db: Session, setlists: List[int]):
    setlist_infos = []
    for setlist in setlists:
        composition = db.query(Composition).filter(Composition.id == setlist.id).first()
        setlist_infos.append(
            CompositionInfo(id=composition.id, name=composition.name, author=composition.author)
        )
    return setlist_infos

def get_participants_info(db: Session, participants: List[int]):
    user_infos = []
    for participant in participants:
        user = db.query(User).filter(User.id == participant.id).first()
        user_infos.append(
            Participant(id=user.id, username=user.username, email=user.email)
        )
    return user_infos

def get_user_events(db: Session, email: str, request: GetEventInfo):
    existing_user = db.query(User).filter(User.email == email).first()
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    group_events = (
        db.query(Event)
        .join(Participation, Participation.event_id == Event.id)
        .filter(
            Participation.user_id == existing_user.id, 
            Event.parent_group == request.group_id  
        )
        .all()
    )
    event_infos = []
    for event in group_events:
        event_infos.append(EventInfo(
            event_id = event.id,
            name = event.name,
            date_start = event.date_end,
            date_end = event.date_end,
            location = event.location,
            extra_info = event.extra_info,
            set_list = get_setlist_info(db, event.set_lists),
            parent_group = event.parent_group,
            type = event.type,
            participants = get_participants_info(db, event.participations))
        )

    return event_infos

def create_event(db: Session, email: str, request: CreateEventRequest):
    
    existing_user = db.query(User).filter(User.email == email).first()
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")

    new_event = Event(
        id=request.id,
        name = request.name,
        date_start = request.date_start,
        date_end = request.date_end,
        location = request.location,
        extra_info = request.extra_info,
        parent_group = request.parent_group,
        type = request.type
    )

    db.add(new_event)
    db.commit()
    db.refresh(new_event)

    new_participation = Participation(
        user_id=existing_user.id,
        event_id=new_event.id,
    )
    db.add(new_participation)

    unique_user_ids = set(request.user_ids)

    for user_email in request.user_emails:
        user = db.query(User).filter(User.email == user_email).first()
        unique_user_ids.add(user.id)

    for group_id in request.group_ids:
        members = db.query(Member).filter(Member.group_id == group_id).all()
        for member in members:
            unique_user_ids.add(member.user_id)

    for user_id in unique_user_ids:
        existing_participation = db.query(Participation).filter(
            Participation.event_id == new_event.id,
            Participation.user_id == user_id
        ).first()

        if not existing_participation:
            new_participation = Participation(
                user_id=user_id,
                event_id=new_event.id
            )
            db.add(new_participation)

    db.commit()

    
    return new_event