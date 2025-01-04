from sqlalchemy.orm import Session
from fastapi import HTTPException
from google.oauth2 import id_token
from google.auth.transport import requests
from dotenv import load_dotenv

from .models import User, Member
from .schemas import UserInfo, UsersInfoStructure

import os
import jwt
import datetime


def manage_loging(db: Session, token: str):
    try:
        load_dotenv()
        GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
        APP_SECRET = os.getenv("APP_SECRET")

        idinfo = id_token.verify_oauth2_token(
            token,
            requests.Request(),
            GOOGLE_CLIENT_ID
        )

        user_id = idinfo["sub"]
        email = idinfo.get("email")
        name = idinfo.get("name")

        app_token = jwt.encode(
            {
                "user_id": user_id,
                "email": email,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
            },
            APP_SECRET,
            algorithm="HS256"
        )
        existing_user = db.query(User).filter(User.email == email).first()
        if existing_user:
            app_token = (app_token, False)
        else:
            app_token = (app_token, True)
        return app_token

    except ValueError as e:
        raise HTTPException(status_code=400, detail="Invalid Google token")

def decode_app_token(app_token: str):
    try:
        if app_token.startswith("Bearer "):
            app_token = app_token[len("Bearer "):]

        load_dotenv()
        APP_SECRET = os.getenv("APP_SECRET")
        decoded_data = jwt.decode(app_token, APP_SECRET, algorithms=["HS256"])
        return decoded_data
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def register_user(db: Session, user_email: str, username: str):
    existing_user = db.query(User).filter(User.email == user_email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(username=username, email=user_email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_user_from_group(db: Session, user_email: str, group_id: int):
    user = db.query(User).filter(User.email == user_email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    member = db.query(Member).filter(Member.user_id == user.id, Member.group_id == group_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="User is not a member of the group")

    if member.role == "Muzyk":
        raise HTTPException(status_code=403, detail="User must have Kapelmistrz or Koordynator role")

    members = db.query(Member).filter(Member.group_id == group_id).all()
    
    if not members:
        raise HTTPException(status_code=404, detail="Group not found or has no members")
    
    user_list = []
    for member in members:
        user = db.query(User).filter(User.id == member.user_id).first()
        if user:
            user_info = UserInfo(
                id=user.id,
                username=user.username,
                email=user.email,
                role=member.role
            )
            user_list.append(user_info)

    return UsersInfoStructure(user_list=user_list)