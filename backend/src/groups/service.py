from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import List
from users.models import User, Group, Member
from .schemas import SubgroupSchema, CreateGroupRequest, JoinGroupRequest, CreateSubgroupRequest, EditGroupRequest

import string
import secrets

def generate_invitation_code(length=20):
    return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(length))


def register_group(db: Session, user_email: User, group: CreateGroupRequest):
    existing_user = db.query(User).filter(User.email == user_email).first()
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")

    invitation_code = generate_invitation_code()

    new_group = Group(
        parent_group=group.parent_group,
        name=group.name,
        extra_info=group.extra_info,
        invitation_code=invitation_code
    )
    db.add(new_group)
    db.commit()
    db.refresh(new_group)

    new_member = Member(
        user_id=existing_user.id,
        group_id=new_group.id,
        role="Kapelmistrz"
    )
    db.add(new_member)
    db.commit()

    return new_group


def get_subgroups_recursive(
    db: Session, parent_group_id: int, visited_groups: set
) -> List[SubgroupSchema]:
    """
    Pobierz wszystkie podgrupy dla grupy nadrzędnej, rekurencyjnie przetwarzając podgrupy,
    unikając duplikowania grup.
    """
    subgroups = (
        db.query(Group, Member.role)
        .join(Member, Group.id == Member.group_id, isouter=True)
        .filter(Group.parent_group == parent_group_id)
        .all()
    )

    result = []
    for subgroup in subgroups:
        group_id = subgroup[0].id

        if group_id in visited_groups:
            continue

        visited_groups.add(group_id)
        result.append(
            SubgroupSchema(
                subgroup_id=group_id,
                subgroup_name=subgroup[0].name,
                extra_info=subgroup[0].extra_info,
                role=subgroup[1],
                inv_code=subgroup[0].invitation_code if subgroup[1] == 'Kapelmistrz' else None,
                subgroups=get_subgroups_recursive(db, group_id, visited_groups)
            )
        )

    return result


def get_user_group_structure(db: Session, email: str):
    """
    Pobierz strukturę grup dla użytkownika, uwzględniając zagnieżdżone podgrupy,
    unikając duplikowania grup.
    """
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None

    group_structure = []
    visited_groups = set()

    for member in user.members:
        group = member.group

        if group.id in visited_groups:
            continue

        visited_groups.add(group.id)

        subgroups = get_subgroups_recursive(db, group.id, visited_groups)

        group_structure.append({
            "group_id": group.id,
            "group_name": group.name,
            "role": member.role,
            "extra_info": group.extra_info,
            "inv_code": group.invitation_code if member.role == 'Kapelmistrz' else None,
            "subgroups": subgroups
        })

    return {
        "username": user.username,
        "group_structure": group_structure
    }


def user_to_group(db: Session, user_email: User, group: JoinGroupRequest):
    existing_user = db.query(User).filter(User.email == user_email).first()
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")

    joined_group = db.query(Group).filter(Group.invitation_code == group.inv_code).first()

    new_member = Member(
        user_id=existing_user.id,
        group_id=joined_group.id,
        role="Muzyk"
    )
    db.add(new_member)
    db.commit()

    return joined_group

def register_subgroup(db: Session, user_email: User, request: CreateSubgroupRequest):
    existing_user = db.query(User).filter(User.email == user_email).first()
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    existing_member = db.query(Member).filter(Member.user_id == existing_user.id, Member.group_id == request.parent_group).first()

    if not existing_member:
        raise HTTPException(status_code=404, detail="User is not a member of the group")

    if existing_member.role != "Kapelmistrz":
        raise HTTPException(status_code=403, detail="User must have Kapelmistrz role")

    new_group = Group(
        parent_group=request.parent_group,
        name=request.name,
        extra_info=request.extra_info,
        invitation_code=None
    )
    db.add(new_group)
    db.commit()
    db.refresh(new_group)

    db.add(Member(user_id=existing_user.id, group_id=new_group.id, role=None))
    
    for id in request.members:
        duplicated = db.query(Member).filter(Member.user_id == id, Member.group_id == new_group.id).first()
        if not duplicated:
            db.add(Member(user_id=id, group_id=new_group.id, role=None))
    
    db.commit() 
    return new_group


def edit_group(db: Session, user_email: User, request: EditGroupRequest):
    existing_user = db.query(User).filter(User.email == user_email).first()
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")

    existing_member = db.query(Member).filter(Member.user_id == existing_user.id, Member.group_id == request.parent_group).first()

    if not existing_member:
        raise HTTPException(status_code=404, detail="User is not a member of the group")

    if existing_member.role != "Kapelmistrz":
        raise HTTPException(status_code=403, detail="User must have Kapelmistrz role")

    group = db.query(Group).filter(Group.id == request.group_id).first()

    group.name = request.name
    group.extra_info = request.extra_info

    db.commit()
    db.refresh(group)

    return {
        "id": group.id,
        "name": group.name,
        "extra_info": group.extra_info
    }
