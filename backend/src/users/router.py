# router.py
from fastapi import APIRouter
from fastapi import Depends, HTTPException, Header
from sqlalchemy.orm import Session
from database import get_session
from .service import manage_loging, register_user, get_user_from_group
from .schemas import GoogleSignInRequest, UserCreate, UsersInfoStructure, GroupsUserRequest
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

@router.get("/findUsers", response_model=UsersInfoStructure)
def get_groups_users(group_id: GroupsUserRequest, db: Session = Depends(get_session), token: str = Header(..., alias="Authorization")):
    user_data = decode_app_token(token)
    result = get_user_from_group(db, user_data.get("email"), group_id.group_id)
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return result
