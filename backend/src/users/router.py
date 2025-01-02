# router.py
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_session
from .service import get_user_group_structure, manage_loging, register_user
from .schemas import UserGroupStructureSchema, GoogleSignInRequest, UserCreate
from .models import User
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
def login(request: GoogleSignInRequest, db: Session = Depends(get_session)):
    load_dotenv()
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    APP_SECRET = os.getenv("APP_SECRET")

    try:
        app_token = manage_loging(db, request.token, GOOGLE_CLIENT_ID, APP_SECRET)
        return {"message": "User signed up successfully", "app_token": app_token[0], "new": app_token[1]}
    except ValueError as e:
        raise HTTPException(status_code=400, detail="Invalid Google token")

@router.post("/createUser", status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_session)):
    try:
        new_user = register_user(db, user.email, user.username)

        return {"id": new_user.id, "username": new_user.username, "email": new_user.email}
    except HTTPException:
            raise HTTPException(status_code=400, detail="Email already registered")
