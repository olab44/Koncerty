from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class AlertBase(BaseModel):
    title: str
    content: str
    group_id: Optional[int] = None


class AlertCreate(AlertBase):
    pass


class AlertInfo(AlertBase):
    id: int
    creator_id: int
    created_at: datetime

    class Config:
        orm_mode = True
