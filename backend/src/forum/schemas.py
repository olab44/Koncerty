from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


class AlertModel(BaseModel):
    id: int
    title: str
    content: str
    date_sent: datetime

    class Config:
        from_attributes = True


class RecipientModel(BaseModel):
    id: int
    alert_id: int
    member_id: int

    class Config:
        from_attributes = True


class CreateAlertRequest(BaseModel):
    title: str
    content: str
    parent_group: int
    user_id: Optional[int] = None
    group_id: Optional[int] = None


class CreateAlertResponse(BaseModel):
    alert: AlertModel
    recipients: List[RecipientModel]

    class Config:
        orm_mode = True


class GetAlertsRequest(BaseModel):
    parent_group: int
    user_id: int


class GetAlertsResponse(BaseModel):
    alerts: List[AlertModel]

    class Config:
        orm_mode = True
