from sqlalchemy.orm import Session
from .models import User


def get_user_groups(db: Session, username: str):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return None

    groups = [member.group for member in user.members]
    return {"username": user.username, "groups": groups}

