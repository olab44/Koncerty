from fastapi import APIRouter
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_session
from .service import register_group
from .schemas import CreateGroupRequest
from users.models import User


router = APIRouter()

@router.post("/createGroup", status_code=201)
def create_group(reqest: CreateGroupRequest, db: Session = Depends(get_session)):
    user = db.query(User).filter(User.email == reqest.user_email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    new_group = register_group(db, user, reqest)
    return {
        "id": new_group.id,
        "parent": new_group.parent_group,
        "name": new_group.name,
        "extra_info": new_group.extra_info,
        "invitation_code": new_group.invitation_code
    }
