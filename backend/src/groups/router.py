from fastapi import APIRouter
from fastapi import Depends, Header
from sqlalchemy.orm import Session
from typing import List

from database import get_session
from .service import (get_user_group_structure, register_group, user_to_group, register_subgroup,
                       edit_group, get_subgroups, remove_subgroup
)
from .schemas import (UserGroupStructureSchema, CreateGroupRequest, JoinGroupRequest, CreateSubgroupRequest,
                       EditGroupRequest, GroupInfo, RemoveGroupRequest, DeleteGroupResponse
)
from users.service import get_user_data

router = APIRouter()

@router.get("/findGroups", response_model=UserGroupStructureSchema)
def get_group_structure(db: Session = Depends(get_session), token: str = Header(..., alias="Authorization")):
    user_data = get_user_data(token)
    result = get_user_group_structure(db, user_data.get("email"))
    return result

@router.post("/createGroup", status_code=201)
def create_group(request: CreateGroupRequest, db: Session = Depends(get_session), token: str = Header(..., alias="Authorization")):
    user_data = get_user_data(token)
    new_group = register_group(db, user_data.get("email"), request)
    return {
        "id": new_group.id,
        "parent": new_group.parent_group,
        "name": new_group.name,
        "extra_info": new_group.extra_info,
        "invitation_code": new_group.invitation_code
    }

@router.post("/joinGroup", status_code=200)
def join_group(request: JoinGroupRequest, db: Session = Depends(get_session), token: str = Header(..., alias="Authorization")):
    user_data = get_user_data(token)

    joined_group = user_to_group(db, user_data.get("email"), request)
    return {
        "id": joined_group.id,
        "parent": joined_group.parent_group,
        "name": joined_group.name,
        "extra_info": joined_group.extra_info,
        "invitation_code": joined_group.invitation_code
    }

@router.post("/createSubgroup", status_code=201)
def create_subgroup(request: CreateSubgroupRequest, db: Session = Depends(get_session), token: str = Header(..., alias="Authorization")):
    user_data = get_user_data(token)
    new_group = register_subgroup(db, user_data.get("email"), request)
    return {
        "id": new_group.id,
        "parent": new_group.parent_group,
        "name": new_group.name,
        "extra_info": new_group.extra_info,
        "invitation_code": new_group.invitation_code
    }

@router.post("/editGroup", status_code=201)
def change_group(request: EditGroupRequest, db: Session = Depends(get_session), token: str = Header(..., alias="Authorization")):
    user_data = get_user_data(token)
    edited_group = edit_group(db, user_data.get("email"), request)
    return edited_group

@router.get("/findSubgroups", response_model=List[GroupInfo])
def get_subs(group_id: int, db: Session = Depends(get_session), token: str = Header(..., alias="Authorization")):
    user_data = get_user_data(token)
    result = get_subgroups(db, user_data.get("email"), group_id)
    return result

@router.post("/deleteSubgroup", status_code=200, response_model=DeleteGroupResponse)
def delete_subgroup(request: RemoveGroupRequest, db: Session = Depends(get_session), token: str = Header(..., alias="Authorization")):
    user_data = get_user_data(token)
    removed_group = remove_subgroup(db, user_data.get("email"), request)
    return removed_group
