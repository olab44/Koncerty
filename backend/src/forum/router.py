from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from typing import List

from src.database import get_session
from users.service import decode_app_token
from .schemas import *
from .service import create_alert, get_alerts
from users.models import User, Member


router = APIRouter()


@router.post("/createAlert", status_code=201, response_model=AlertInfo)
def post_alert(
    request: AlertCreate,
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


@router.get("/Alerts", response_model=List[AlertInfo])
def fetch_alerts(
    group_id: int = None,
    db: Session = Depends(get_session),
    token: str = Header(..., alias="Authorization"),
):
    try:
        user_data = decode_app_token(token)
        return get_alerts(db, group_id)
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
