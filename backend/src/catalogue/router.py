from fastapi import APIRouter, File, UploadFile, Form
from fastapi import Depends, HTTPException, Header
from sqlalchemy.orm import Session

from typing import List

from database import get_session
from .service import get_compositions, create_composition
from .schemas import *
from users.service import decode_app_token

router = APIRouter()

@router.get("/findCompositions", status_code=200)
def find_compositions(group_id: int, db: Session = Depends(get_session), token: str = Header(..., alias="Authorization")):
    """ Handle frontend request for the group's music catalogue """
    user_data = decode_app_token(token)
    catalogue = get_compositions(db, user_data.get("user_id"), group_id)
    return {"found": catalogue}


@router.post("/addComposition", status_code=201)
def add_composition(request: CreateCompositionRequest, db: Session = Depends(get_session), token: str = Header(..., alias="Authorization")):
    """ Handle request to add a new composition to the group's music catalogue """
    user_data = decode_app_token(token)
    created = create_composition(db, user_data.get("email"), request)
    return {"created": created}