from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from typing import List

from src.database import get_session
from users.service import decode_app_token
from .schemas import *
from .service import create_alert, get_alerts
from users.models import User, Member, Alert
from users.service import get_user_data


router = APIRouter()


@router.post("/createAlert", status_code=201, response_model=CreateAlertResponse)
def post_alert(
    request: CreateAlertRequest,
    db: Session = Depends(get_session),
    token: str = Header(..., alias="Authorization"),
):
    user_data = decode_app_token(token)    
    alert, recipients =  create_alert(db, user_data.get("email"), request)
    alert_model = AlertModel.from_orm(alert)
    recipients_model = [RecipientModel.from_orm(rec) for rec in recipients]

    return {
        "alert": alert_model,
        "recipients": recipients_model
    }


@router.get("/getAlerts", response_model=GetAlertsResponse)
def fetch_alerts(
    parent_group: int,
    db: Session = Depends(get_session),
    token: str = Header(..., alias="Authorization"),
):
    user_data = get_user_data(token)
    user_email = user_data.get("email")

    if not user_email:
        raise HTTPException(status_code=400, detail="User email not found in token")

    existing_user = db.query(User).filter(User.email == user_email).first()
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")

    alerts = get_alerts(db, existing_user.id, parent_group)
    alerts_model = [AlertModel.from_orm(alert) for alert in alerts]
    return {"alerts": alerts_model}
