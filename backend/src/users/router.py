# router.py
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_session
from .service import get_user_groups
from .schemas import UserGroupsResponse


router = APIRouter()


@router.post("/test")
def test():
    return None

@router.get("/groups/{user}", response_model=UserGroupsResponse)
def getGroupsByUser(user: str, db: Session = Depends(get_session)):
    user_data = get_user_groups(db, user)
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")
    return user_data

