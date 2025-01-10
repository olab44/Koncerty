from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import List

from users.models import Member, Composition, File, FileOwnership, User
from .schemas import CompositionInfo, FileInfo


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


def create_composition(db: Session, user_id: int, group_id: int, name, author, files):
    """ Add the composition to the group's music catalogue """
    member = db.query(Member).filter(Member.user_id == user_id, Member.group_id == group_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Requesting member not found.")

    return