from fastapi import APIRouter, File, UploadFile, Form
from fastapi import Depends, HTTPException, Header
from sqlalchemy.orm import Session

from typing import List

from database import get_session
from .service import get_compositions, add_composition
from .schemas import *
from users.service import decode_app_token

router = APIRouter()

@router.get("/findCompositions", response_model=List[CompositionInfo])
def find_compositions(group_id: int, db: Session = Depends(get_session), token: str = Header(..., alias="Authorization")):
    """ Handle frontend request for the group's music catalogue """
    user_data = decode_app_token(token)
    return get_compositions(db, user_data.get("user_id"), group_id)


@router.post("/addComposition", response_model=List[CompositionInfo])
def add_composition(group_id: int = Form(...), name: str = Form(...), author: str = Form(...), files: List[UploadFile] = File(...),
    db: Session = Depends(get_session), token: str = Header(..., alias="Authorization")):
    """ Handle request to add a new composition to the group's music catalogue """
    user_data = decode_app_token(token)
    return add_composition(db, user_data.get("user_id"), group_id, name, author, files)