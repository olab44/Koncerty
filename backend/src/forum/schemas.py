from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class AnnouncementBase(BaseModel):
    title: str
    content: str


class AnnouncementCreate(AnnouncementBase):
    group_id: Optional[int] = None
    user_id: Optional[int] = None


class Announcement(AnnouncementBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
