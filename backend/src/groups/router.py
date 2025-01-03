from fastapi import APIRouter
from fastapi import Depends, HTTPException
from dotenv import load_dotenv 
import os
from sqlalchemy.orm import Session

from database import get_session
from .service import register_group
from .schemas import CreateGroupRequest
from users.models import User
from users.service import decode_app_token


router = APIRouter()

@router.post("/createGroup", status_code=201)
def create_group(reqest: CreateGroupRequest, db: Session = Depends(get_session)):
    user_data = decode_app_token(reqest.token)
    user = db.query(User).filter(User.email == user_data.get("email")).first()

    if not user:
        raise HTTPException(status_code=404, detail=f"User not found {user_data}")

    new_group = register_group(db, user, reqest)
    return {
        "id": new_group.id,
        "parent": new_group.parent_group,
        "name": new_group.name,
        "extra_info": new_group.extra_info,
        "invitation_code": new_group.invitation_code
    }
