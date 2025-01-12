from fastapi import APIRouter, File, UploadFile, Form
from fastapi import Depends, HTTPException, Header
from sqlalchemy.orm import Session

from typing import List

from database import get_session
from .service import get_compositions, create_composition, get_compositions_extra, remove_composition
from .schemas import *
from users.service import get_user_data 

router = APIRouter()

@router.get("/findCompositions", status_code=200)
def find_compositions(group_id: int, db: Session = Depends(get_session), token: str = Header(..., alias="Authorization")):
    """ Handle frontend request for the group's music catalogue """
    user_data = get_user_data(token)
    catalogue = get_compositions(db, user_data.get("user_id"), group_id)
    return {"found": catalogue}


@router.post("/addComposition", status_code=201)
def add_composition(request: CreateCompositionRequest, db: Session = Depends(get_session), token: str = Header(..., alias="Authorization")):
    """ Handle request to add a new composition to the group's music catalogue """
    user_data = get_user_data(token)
    created = create_composition(db, user_data.get("email"), request)
    return {"created": created}

@router.get("/findCompositionsExtra", status_code=200)
def find_compositions_extra(group_id: int, db: Session = Depends(get_session), token: str = Header(..., alias="Authorization")):
    """ Handle frontend request for the group's music catalogue """
    user_data = get_user_data(token)
    catalogue = get_compositions_extra(db, user_data.get("email"), group_id)
    return {"found": catalogue}

@router.post("/removeComposition", status_code=201)
def rm_event(request: RemoveCompositionRequest, db: Session = Depends(get_session), token: str = Header(..., alias="Authorization")):
    user_data = get_user_data(token)

    composition_event = remove_composition(db, user_data.get("email"), request)
    return {"removed": composition_event}
