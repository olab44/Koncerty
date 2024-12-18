from sqlalchemy.orm import Session
from .models import User, Group, Member


def get_user_group_structure(db: Session, username: str):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return None

    group_structure = []

    for member in user.members:
        group = member.group
        if group.parent_group is None:
            # Pobierz tylko podgrupy, w których użytkownik jest członkiem
            subgroups = (
                db.query(Group, Member.role)
                .join(Member, Group.id == Member.group_id)
                .filter(Group.parent_group == group.id, Member.user_id == user.id)
                .all()
            )

            group_structure.append({
                "group_id": group.id,
                "group_name": group.name,
                "role": member.role,
                "subgroups": [
                    {
                        "subgroup_id": subgroup[0].id,
                        "subgroup_name": subgroup[0].name,
                        "role": subgroup[1]
                    }
                    for subgroup in subgroups
                ]
            })

    return {
        "username": user.username,
        "group_structure": group_structure
    }
