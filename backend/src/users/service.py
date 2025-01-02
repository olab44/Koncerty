from sqlalchemy.orm import Session
from fastapi import HTTPException
from .models import User, Group, Member
from google.oauth2 import id_token
from google.auth.transport import requests
import jwt
import datetime

def get_user_group_structure(db: Session, username: str):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return None

    group_structure = []

    for member in user.members:
        group = member.group
        if group.parent_group is None:
            # Pobierz tylko podgrupy, w których użytkownik jest członkiem
            subgroups = (
                db.query(Group, Member.role)
                .join(Member, Group.id == Member.group_id)
                .filter(Group.parent_group == group.id, Member.user_id == user.id)
                .all()
            )

            group_structure.append({
                "group_id": group.id,
                "group_name": group.name,
                "role": member.role,
                "subgroups": [
                    {
                        "subgroup_id": subgroup[0].id,
                        "subgroup_name": subgroup[0].name,
                        "role": subgroup[1]
                    }
                    for subgroup in subgroups
                ]
            })

    return {
        "username": user.username,
        "group_structure": group_structure
    }

def manage_loging(db: Session, token: str, GOOGLE_CLIENT_ID: str, APP_SECRET: str):
    try:
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
            app_token = (app_token, True)
        else:
            app_token = (app_token, False)
        return app_token

    except ValueError as e:
        raise HTTPException(status_code=400, detail="Invalid Google token")
    
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