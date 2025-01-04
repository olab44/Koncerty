import os
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException
from dotenv import load_dotenv

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from .schemas import EventInfo, CreateEventRequest
from users.models import User

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

def get_user_events(db: Session, email: str):
    event = EventInfo(event_id = 1, name = 'Code Review',
        description ='Review latest PRs',
        date_start = datetime(2025, 1, 11, 14, 0, 0),
        date_end = datetime(2025, 1, 11, 15, 30, 0),
        set_list = [],
        participants = [])
    return [event]

def create_event(db: Session, user: User, group: CreateEventRequest):
    return