from sqlalchemy.orm import Session
from fastapi import HTTPException
from users.models import User, Group, Member
from .schemas import CreateGroupRequest

import string
import secrets

def generate_invitation_code(length=20):
    return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(length))


def register_group(db: Session, user: User, group: CreateGroupRequest):
    existing_user = db.query(User).filter(User.email == user.email).first()
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
