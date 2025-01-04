# router.py
from fastapi import APIRouter
from fastapi import Depends, HTTPException, Header
from sqlalchemy.orm import Session
from database import get_session
from .service import manage_loging, register_user
from .schemas import GoogleSignInRequest, UserCreate
from users.service import decode_app_token

router = APIRouter()


@router.post("/test")
def test():
    return {"message": "Test working"}

@router.post("/google-sign-in")
def login(request: GoogleSignInRequest, db: Session = Depends(get_session)):
    try:
        app_token = manage_loging(db, request.token)
        return {"message": "User signed up successfully", "app_token": app_token[0], "new": app_token[1]}
    except ValueError as e:
        raise HTTPException(status_code=400, detail="Invalid Google token")


@router.post("/createUser", status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_session), token: str = Header(..., alias="Authorization")):
    try:
        user_data = decode_app_token(token)
        user_email = user_data.get("email")
        new_user = register_user(db, user_email, user.username)

        return {"id": new_user.id, "username": new_user.username, "email": new_user.email}
    except HTTPException:
        raise HTTPException(status_code=400, detail="Email already registered")
