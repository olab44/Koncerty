from sqlalchemy.orm import Session
from typing import List
import dramatiq
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from smtplib import SMTP
from .config import settings
from users.models import Member, User, Alert, Recipient, Group
from .schemas import CreateAlertRequest, GetAlertsRequest
import os
import base64
from fastapi import HTTPException
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from forum.sendEmail import send_gmail_email

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

def create_alert(db: Session, email: str, request: CreateAlertRequest) -> Alert:
    """
    Creates an alert and sends notifications to recipients.

    Args:
        db (Session): The database session.
        email (str): The email of the user creating the alert.
        request (CreateAlertRequest): Request data for creating the alert.

    Returns:
        tuple: The created Alert object and a list of Recipient objects.

    Raises:
        HTTPException: If the user does not exist, is not a member of the group, 
                       or lacks the required role to create an alert.
    """
    existing_user = db.query(User).filter(User.email == email).first()
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    existing_member = db.query(Member).filter(Member.user_id == existing_user.id, Member.group_id == request.parent_group).first()
    if not existing_member:
        raise HTTPException(status_code=404, detail="User is not a member of the group")

    if existing_member.role not in ["Kapelmistrz", "Koordynator"]:
        raise HTTPException(status_code=403, detail="User must have Kapelmistrz or Koordynator role")
    
    new_alert = Alert(
        title=request.title,
        content=request.content
    )
    db.add(new_alert)
    db.commit()
    db.refresh(new_alert)

    recipients_list = []
    # Fetch recipients and send notifications
    if request.group_id:
        recipients = get_recipients(db, request.group_id)
        for recipient in recipients:
            rec = create_recipient(db, recipient.id, new_alert.id)
            recipients_list.append(rec)
            notify_recipient(recipient.email, new_alert.title, new_alert.content)
    elif request.user_id:
        recipient = db.query(User).filter(User.id == request.user_id).first()
        if not recipient:
            raise HTTPException(status_code=404, detail=f"There is no user with id: {request.user_id}")
        rec = create_recipient(db, request.user_id, new_alert.id)
        recipients_list.append(rec)
        notify_recipient(recipient.email, new_alert.title, new_alert.content)
    else:
        raise HTTPException(status_code=404, detail="You must provide user_id or group_id to address the alert")

    return new_alert, recipients_list


def get_alerts(db: Session, email: str, request: GetAlertsRequest):
    """
    Retrieves alerts for a user based on their group membership.

    Args:
        db (Session): The database session.
        email (str): The email of the user requesting the alerts.
        request (GetAlertsRequest): The request data for fetching alerts.

    Returns:
        list: A list of Alert objects.
    """
    existing_user = db.query(User).filter(User.email == email).first()
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    existing_member = db.query(Member).filter(Member.user_id == existing_user.id, Member.group_id == request.parent_group).first()
    if not existing_member:
        raise HTTPException(status_code=404, detail="User is not a member of the group")
    
    members = db.query(Member.id).join(
        Group, Member.group_id == Group.id
    ).filter(
        Member.user_id == request.user_id,
        Group.parent_group == request.parent_group
    ).subquery()
    
    alerts = db.query(Alert).join(
        Recipient, Recipient.alert_id == Alert.id
    ).filter(
        (Recipient.member_id == existing_member.id) | 
        (Recipient.member_id.in_(members))
    ).all()
    return alerts


def create_recipient(db: Session, user_id: int, alert_id: int) -> Recipient:
    """
    Creates a recipient record for a given alert.
    """
    new_recipient = Recipient(
        alert_id=alert_id,
        member_id=user_id
    )
    db.add(new_recipient)
    db.commit()
    db.refresh(new_recipient)

    return new_recipient


def get_recipients(db: Session, group_id: int) -> List[User]:
    """
    Fetches the users who are members of a specified group.
    """
    query = db.query(User).join(Member).filter(Member.group_id == group_id)
    return query.all()


@dramatiq.actor
def notify_recipient(recipient_email: str, subject: str, body: str) -> None:
    """
    Sends a notification email to a recipient.
    """
    # send_gmail_email(recipient_email, subject, body)
    pass
