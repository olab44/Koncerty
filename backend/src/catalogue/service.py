from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import List

from users.models import Member, Composition, File, FileOwnership
from .schemas import CompositionInfo, FileInfo


def get_composition_files_info(db: Session, composition_id: int) -> List[FileInfo]:
    """ Get basic info (id, name) about the composition's files """
    files = db.query()
    return files


def get_compositions(db: Session, user_id: int, group_id: int) -> List[CompositionInfo]:
    """ Get all the compositions for the group's music catalogue """
    member = db.query(Member).filter(Member.user_id == user_id, Member.group_id == group_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Requesting member not found.")

    compositions = db.query()

    catalogue = []
    for composition in compositions:
        files = get_composition_files_info(composition.id)
        catalogue.append(CompositionInfo(composition.id, composition.name, composition.author, files))

    return catalogue


def add_composition(db: Session, user_id: int, group_id: int, name, author, files):
    """ Add the composition to the group's music catalogue """
    member = db.query(Member).filter(Member.user_id == user_id, Member.group_id == group_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Requesting member not found.")

    return