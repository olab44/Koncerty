from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class AnnouncementBase(BaseModel):
    title: str
    content: str
    group_id: Optional[int] = None
    subgroup_id: Optional[int] = None


class AnnouncementCreate(AnnouncementBase):
    pass


class AnnouncementInfo(AnnouncementBase):
    id: int
    creator_id: int
    created_at: datetime

    class Config:
        orm_mode = True
