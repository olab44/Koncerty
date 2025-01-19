from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import List

from .schemas import EventInfo, CreateEventRequest, Participant, EditEventRequest, RemoveEventRequest
from catalogue.schemas import CompositionInfo
from users.models import (User, Member,
     Event, Participation, Composition, SetList
)

def get_setlist_info(db: Session, setlists: List[int]):
    """
    Retrieve setlist information for the given setlist IDs.
    """
    setlist_infos = []
    for setlist in setlists:
        composition = db.query(Composition).filter(Composition.id == setlist.composition_id).first()
        setlist_infos.append(
            CompositionInfo(id=composition.id, name=composition.name, author=composition.author)
        )
    return setlist_infos

def get_participants_info(db: Session, participants: List[int]):
    """
    Retrieve participant information for the given participant IDs.
    """
    user_infos = []
    for participant in participants:
        user = db.query(User).filter(User.id == participant.user_id).first()
        user_infos.append(
            Participant(id=user.id, username=user.username, email=user.email)
        )
    return user_infos

def user_in_parent_group(db: Session, user: User, group_id: int) -> bool:
    """
    Check if a user belongs to a specific parent group.
    """
    member = db.query(Member).filter(
        Member.user_id == user.id,
        Member.group_id == group_id
    ).first()

    return member is not None

def get_user_events(db: Session, email: str, group_id: int):
    """
    Retrieve events for a specific user and group.
    """
    existing_user = db.query(User).filter(User.email == email).first()
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")

    group_events = (
        db.query(Event)
        .join(Participation, Participation.event_id == Event.id)
        .filter(
            Participation.user_id == existing_user.id,
            Event.parent_group == group_id
        )
        .all()
    )
    event_infos = []
    for event in group_events:
        event_infos.append(EventInfo(
            event_id = event.id,
            name = event.name,
            date_start = event.date_start,
            date_end = event.date_end,
            location = event.location,
            extra_info = event.extra_info,
            set_list = get_setlist_info(db, event.set_lists),
            parent_group = event.parent_group,
            type = event.type,
            participants = get_participants_info(db, event.participations))
        )

    return event_infos

def create_event(db: Session, email: str, request: CreateEventRequest):
    """
    Create a new event and associate participants and setlists.
    """

    existing_user = db.query(User).filter(User.email == email).first()
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")

    new_event = Event(
        name = request.name,
        date_start = request.date_start,
        date_end = request.date_end,
        location = request.location,
        extra_info = request.extra_info,
        parent_group = request.parent_group,
        type = request.type
    )

    db.add(new_event)
    db.commit()
    db.refresh(new_event)

    new_participation = Participation(
        user_id=existing_user.id,
        event_id=new_event.id,
    )
    db.add(new_participation)

    unique_user_ids = set()

    for user_email in request.user_emails:
        user = db.query(User).filter(User.email == user_email).first()
        if user and user_in_parent_group(db, user, new_event.parent_group):
            unique_user_ids.add(user.id)

    for group_id in request.group_ids:
        members = db.query(Member).filter(Member.group_id == group_id).all()
        for member in members:
            unique_user_ids.add(member.user_id)

    for user_id in unique_user_ids:
        existing_participation = db.query(Participation).filter(
            Participation.event_id == new_event.id,
            Participation.user_id == user_id
        ).first()

        if not existing_participation:
            new_participation = Participation(
                user_id=user_id,
                event_id=new_event.id
            )
            db.add(new_participation)

    db.commit()

    for composition in request.composition_ids:
        new_setlist = SetList(
            event_id = new_event.id,
            composition_id = composition
        )

        db.add(new_setlist)

    db.commit()

    return new_event


def edit_event(db: Session, email: str, request: EditEventRequest):
    """
    Edit an existing event's details, participants, and setlists.
    """

    existing_user = db.query(User).filter(User.email == email).first()
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")

    parent_member = db.query(Member).filter(Member.user_id == existing_user.id, Member.group_id == request.parent_group).first()

    if not parent_member:
        raise HTTPException(status_code=404, detail="Requesting user not is a member of the group")
    if parent_member.role == "Muzyk":
        raise HTTPException(status_code=404, detail="Requesting user must have Kapelmistrz or Koordynator role")

    existing_event = db.query(Event).filter(Event.id == request.event_id).first()

    existing_event.name = request.name
    existing_event.date_start = request.date_start
    existing_event.date_end = request.date_end
    existing_event.location = request.location
    existing_event.extra_info = request.extra_info
    existing_event.parent_group = request.parent_group
    existing_event.type = request.type

    db.commit()
    db.refresh(existing_event)

    for removed_email in request.removed_participants:
        to_remove = (db.query(Participation)
                        .join(User, User.id == Participation.user_id)
                        .filter(Participation.event_id == request.event_id, User.email == removed_email)
                        .first())
        if to_remove:
            db.delete(to_remove)

    for added_email in request.added_participants:
        user = db.query(User).filter(User.email == added_email).first()
        if user:
            existing_participant = (db.query(Participation)
                                     .filter(Participation.event_id == request.event_id, Participation.user_id == user.id)
                                     .first())
            if not existing_participant:
                new_participant = Participation(
                    event_id=request.event_id,
                    user_id=user.id
                )
                db.add(new_participant)

    for id in request.removed_compositions:
        to_remove = db.query(SetList).filter(SetList.event_id == request.event_id, SetList.composition_id == id).first()
        if to_remove:
            db.delete(to_remove)

    for id in request.added_compositions:
        to_add = db.query(SetList).filter(SetList.event_id == request.event_id, SetList.composition_id == id).first()
        if not to_add:
            new_setlist = SetList(
                event_id = request.event_id,
                composition_id = id
            )
            db.add(new_setlist)

    db.commit()

    return existing_event

def remove_event(db: Session, email: str, request: RemoveEventRequest):

    existing_user = db.query(User).filter(User.email == email).first()
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")

    parent_member = db.query(Member).filter(Member.user_id == existing_user.id, Member.group_id == request.owner_group_id).first()

    if not parent_member:
        raise HTTPException(status_code=404, detail="Requesting user not is a member of the group")
    if parent_member.role == "Muzyk":
        raise HTTPException(status_code=404, detail="Requesting user must have Kapelmistrz or Koordynator role")

    to_delete = db.query(Event).filter(Event.id == request.event_id).first()

    if not to_delete:
        raise HTTPException(status_code=404, detail=f"Event with id {request.event_id} not found")

    db.delete(to_delete)
    db.commit()

    return {"deleted": to_delete.id}