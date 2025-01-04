from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional

class Participant(BaseModel):
    username: str
    email: str

class EventInfo(BaseModel):
    event_id: int
    name: str
    date_start: datetime
    date_end: datetime
    description: Optional[str]
    set_list: List[int]
    participants: List[Participant]

class CreateEventRequest(BaseModel):
    name: str
    date_start: datetime
    date_end: datetime
    description: Optional[str]
