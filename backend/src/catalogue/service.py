from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import List

from users.models import Member, Composition, File, FileOwnership, User
from .schemas import CompositionInfo, FileInfo, CreateCompositionRequest, CreateCompositionResponse, FileInfoExtra
from files.service import assign_file_to_composition
from files.schemas import FileToCompositionRequest

def get_composition_files_info(db: Session, composition_id: int) -> List[FileInfo]:
    """ Get basic info (id, name) about the composition's files """
    files = db.query()  
    return files


def get_compositions(db: Session, email: str, group_id: int) -> List[CompositionInfo]:
    """ Get all the compositions for the group's music catalogue """
    users = db.query(User).join(Member, User.id == Member.user_id).filter(Member.group_id == group_id)
    
    if not users:
        raise HTTPException(status_code=404, detail="No users in the group")

    composition_list = []
    composition_ids = set()
    for user in users:
        compositions = (db.query(Composition)
                    .join(File, File.composition_id == Composition.id)
                    .join(FileOwnership, FileOwnership.file_id == File.id)
                    .filter(FileOwnership.user_id == user.id).all())
        if compositions:
            for composition in compositions:
                if composition.id not in composition_ids:
                    composition_ids.add(composition.id)
                    composition_list.append(composition)


    return composition_list


def create_composition(db: Session, user_email: str, request: CreateCompositionRequest):
    """ Add the composition to the group's music catalogue """
    reqesting_user = db.query(User).filter(User.email == user_email).first()

    if not reqesting_user:
        raise HTTPException(status_code=404, detail="Requesting user not found.")

    member = db.query(Member).filter(Member.user_id == reqesting_user.id, Member.group_id == request.parent_group).first()
    if not member:
        raise HTTPException(status_code=404, detail="Requesting member not found.")
    if member.role != "Kapelmistrz":
        raise HTTPException(status_code=404, detail="Requesting member does not have permision.")
    
    new_composition = Composition(
        name = request.name,
        author = request.author
    )
    
    db.add(new_composition)
    db.commit()
    db.refresh(new_composition)
    
    comp_info = CompositionInfo(
        id=new_composition.id,
        name=new_composition.name,
        author=new_composition.author,
        files=[]
    )

    for file in request.files:
        new_request = FileToCompositionRequest(
            file_id=file,
            composition_id=new_composition.id,
            parent_group=request.parent_group
        )
        file = assign_file_to_composition(db, reqesting_user.email, new_request)
        file_info = FileInfo(id=file.id, name=file.name)
        comp_info.files.append(file_info)

    return [comp_info]

def get_compositions_extra(db: Session, user_email: str, group_id: int):
    """ Get all the compositions for the group's music catalogue """
    requesting_user = db.query(User).filter(User.email == user_email).first()
    if not requesting_user:
        raise HTTPException(status_code=404, detail="Requesting user not found")
    users = db.query(User).join(Member, User.id == Member.user_id).filter(Member.group_id == group_id)
    
    if not users:
        raise HTTPException(status_code=404, detail="No users in the group")

    composition_list = []
    composition_ids = set()
    for user in users:
        compositions = (db.query(Composition)
                    .join(File, File.composition_id == Composition.id)
                    .join(FileOwnership, FileOwnership.file_id == File.id)
                    .filter(FileOwnership.user_id == user.id).all())
        if compositions:
            for composition in compositions:
                if composition.id not in composition_ids:
                    composition_ids.add(composition.id)
                    found = CreateCompositionResponse(
                        name=composition.name,
                        author=composition.author,
                        files=[]
                    )
                    for file in composition.files:
                        file_info = FileInfoExtra(
                            id=file.id,
                            name=file.name,
                            access=db.query(FileOwnership).filter(FileOwnership.user_id == requesting_user.id, FileOwnership.file_id==file.id).first() is not None
                        )
                        found.files.append(file_info)
                    composition_list.append(found)
                    


    return composition_list
