# router.py
from fastapi import APIRouter
from fastapi import Depends, HTTPException, Header
from sqlalchemy.orm import Session
from database import get_session
from typing import List
from .service import manage_loging, register_user, get_user_from_group, change_user_role, remove_member_all_subs
from .schemas import GoogleSignInRequest, UserCreate, UserInfo, GroupsUserRequest, ChangeUserRoleRequest, RemoveMemberRequest
from users.service import get_user_data

router = APIRouter()


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
        user_data = get_user_data(token)
        user_email = user_data.get("email")
        
        new_user = register_user(db, user_email, user.username)

        return {"id": new_user.id, "username": new_user.username, "email": new_user.email}
    except HTTPException:
        raise HTTPException(status_code=400, detail="Email already registered")

@router.get("/findUsers", response_model=List[UserInfo])
def get_groups_users(group_id: int, db: Session = Depends(get_session), token: str = Header(..., alias="Authorization")):
    user_data = get_user_data(token)
    result = get_user_from_group(db, user_data.get("email"), group_id)
    return result

@router.post("/changeRole", status_code=201)
def change_role(request: ChangeUserRoleRequest, db: Session = Depends(get_session), token: str = Header(..., alias="Authorization")):
    user_data = get_user_data(token)
    result = change_user_role(db, user_data.get("email"), request)
    return result

@router.delete("/removeMember", status_code=200)
def rm_member(request: RemoveMemberRequest, db: Session = Depends(get_session), token: str = Header(..., alias="Authorization")):
    user_data = get_user_data(token)
    result = remove_member_all_subs(db, user_data.get("email"), request)
    
    return result
