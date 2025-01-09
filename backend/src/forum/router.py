from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from typing import List

from src.database import get_session
from users.service import decode_app_token
from .schemas import *
from .service import create_alert, get_alerts
from users.models import User, Member, Alert


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
    request: GetAlertsRequest,
    db: Session = Depends(get_session),
    token: str = Header(..., alias="Authorization"),
):
    user_data = decode_app_token(token)
    alerts = get_alerts(db, user_data.get("email"), request)
    alerts_model = [AlertModel.from_orm(alert) for alert in alerts]

    return {
        "alerts": alerts_model
    }
