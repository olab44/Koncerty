# router.py
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_session
from .service import get_user_group_structure
from .schemas import UserGroupStructureSchema


router = APIRouter()


@router.post("/test")
def test():
    return None

@router.get("/groups/{username}", response_model=UserGroupStructureSchema)
def get_group_structure(username: str, db: Session = Depends(get_session)):
    result = get_user_group_structure(db, username)
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return result
