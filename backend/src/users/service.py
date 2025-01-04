from sqlalchemy.orm import Session
from fastapi import HTTPException
from .models import User
from google.oauth2 import id_token
from google.auth.transport import requests
from dotenv import load_dotenv
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
    # Sprawdź, czy użytkownik już istnieje
    existing_user = db.query(User).filter(User.email == user_email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

        # Zapisz użytkownika do bazy danych
    new_user = User(username=username, email=user_email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user