from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional

class Participant(BaseModel):
    id: int
    username: str
    email: str

class CompositionInfo(BaseModel):
    id: int
    name: str
    author: str

class EventInfo(BaseModel):
    event_id: int
    name: str
    date_start: datetime
    date_end: datetime
    location: str
    extra_info: Optional[str]
    set_list: List[CompositionInfo]
    parent_group: int
    type: str
    participants: List[Participant]

class CreateEventRequest(BaseModel):
    name: str
    date_start: datetime
    date_end: datetime
    location: str
    extra_info: Optional[str]
    parent_group: int
    type: str
    user_emails: List[str]
    group_ids: List[int]
    composition_ids: List[int]

class EditEventRequest(BaseModel):
    event_id: int
    name: str
    date_start: datetime
    date_end: datetime
    location: str
    extra_info: Optional[str]
    parent_group: int
    type: str
    removed_participants: List[str]
    added_participants: List[str]
    removed_compositions: List[int]
    added_compositions: List[int]
