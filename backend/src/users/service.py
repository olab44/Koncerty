from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import List
from .models import User, Group, Member
from .schemas import SubgroupSchema
from google.oauth2 import id_token
from google.auth.transport import requests
from dotenv import load_dotenv
import os
import jwt
import datetime

def get_subgroups_recursive(
    db: Session, parent_group_id: int, visited_groups: set
) -> List[SubgroupSchema]:
    """
    Pobierz wszystkie podgrupy dla grupy nadrzędnej, rekurencyjnie przetwarzając podgrupy,
    unikając duplikowania grup.
    """
    subgroups = (
        db.query(Group, Member.role)
        .join(Member, Group.id == Member.group_id, isouter=True)
        .filter(Group.parent_group == parent_group_id)
        .all()
    )

    result = []
    for subgroup in subgroups:
        group_id = subgroup[0].id

        if group_id in visited_groups:
            continue

        visited_groups.add(group_id)
        result.append(
            SubgroupSchema(
                subgroup_id=group_id,
                subgroup_name=subgroup[0].name,
                role=subgroup[1] if subgroup[1] else "Brak roli",
                subgroups=get_subgroups_recursive(db, group_id, visited_groups)
            )
        )

    return result


def get_user_group_structure(db: Session, username: str):
    """
    Pobierz strukturę grup dla użytkownika, uwzględniając zagnieżdżone podgrupy,
    unikając duplikowania grup.
    """
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return None

    group_structure = []
    visited_groups = set()

    for member in user.members:
        group = member.group

        if group.id in visited_groups:
            continue

        visited_groups.add(group.id) 

        subgroups = get_subgroups_recursive(db, group.id, visited_groups)

        group_structure.append({
            "group_id": group.id,
            "group_name": group.name,
            "role": member.role,
            "subgroups": subgroups
        })

    return {
        "username": user.username,
        "group_structure": group_structure
    }



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