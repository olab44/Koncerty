# router.py
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_session
from .service import get_user_group_structure, manage_loging
from .schemas import UserGroupStructureSchema, GoogleSignInRequest
from dotenv import load_dotenv
import os



router = APIRouter()


@router.post("/test")
def test():
    return {"message": "Test working"}

@router.get("/groups/{username}", response_model=UserGroupStructureSchema)
def get_group_structure(username: str, db: Session = Depends(get_session)):
    result = get_user_group_structure(db, username)
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return result

@router.post("/google-sign-in")
def login(request: GoogleSignInRequest):
    load_dotenv()
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    APP_SECRET = os.getenv("APP_SECRET")

    try:
        app_token = manage_loging(request.token, GOOGLE_CLIENT_ID, APP_SECRET)
        return {"message": "User signed up successfully", "token": app_token}
    except ValueError as e:
        raise HTTPException(status_code=400, detail="Invalid Google token")
