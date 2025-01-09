from sqlalchemy.orm import Session
from typing import List
import dramatiq
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from smtplib import SMTP
from .config import settings
from users.models import Member, User, Alert, Recipient
from .schemas import AlertCreate, AlertInfo
import os
import base64
from fastapi import HTTPException
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
# from Google import Create_Service
from forum.sendEmail import send_gmail_email


SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

def create_alert(db: Session, email: str, request: AlertCreate) -> Alert:

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
        # get users who become recipients
        recipients = get_recipients(db, request.group_id)
        for recipient in recipients:
            # rec is recipient object
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


def get_alerts(db: Session, group_id: int) -> List[AlertInfo]:
    query = db.query(Alert).filter(Alert.group_id == group_id)
    return query.all()


def create_recipient(db: Session, user_id: int, alert_id: int) -> Recipient:
    new_recipient = Recipient(
        alert_id = alert_id,
        member_id = user_id
    )
    db.add(new_recipient)
    db.commit()
    db.refresh(new_recipient)

    return new_recipient


def get_recipients(db: Session, group_id: int) -> List[User]:
    """
    Fetch id of users in the specified group or subgroup.
    """
    query = db.query(User).join(Member).filter(Member.group_id == group_id)
    return query.all()


# def compose_message(recipient_email: str, subject: str, body: str) -> MIMEText:
#     """
#     Compose an email message.
#     """
#     message = MIMEText(body, "plain")
#     message["Subject"] = subject
#     message["From"] = settings.EMAIL_ADDRESS
#     message["To"] = recipient_email
#     return message


# def send_email(message: MIMEText) -> None:
#     with SMTP(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
#         server.starttls()
#         server.login(settings.EMAIL_ADDRESS, settings.EMAIL_PASSWORD)
#         server.sendmail(settings.EMAIL_ADDRESS, [message["To"]], message.as_string())

# def get_gmail_service():
#     """Authenticate with Gmail API and return the service object."""
#     creds = None
#     # Load credentials from the token file
#     if os.path.exists(settings.TOKEN_FILE):
#         creds = Credentials.from_authorized_user_file(settings.TOKEN_FILE, SCOPES)
#     # If credentials are invalid or not available, reauthenticate
#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             flow = InstalledAppFlow.from_client_secrets_file(settings.GMAIL_CREDENTIALS_FILE, SCOPES)
#             creds = flow.run_local_server(port=0)
#         # Save the credentials for the next run
#         with open(settings.TOKEN_FILE, "w") as token_file:
#             token_file.write(creds.to_json())
#     return build("gmail", "v1", credentials=creds)


# def send_gmail_email(recipient_email: str, subject: str, body: str):
#     """Send an email via Gmail API."""
#     service = get_gmail_service()
#     message = MIMEText(body)
#     message["to"] = recipient_email
#     message["subject"] = subject
#     raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
#     try:
#         send_message = (
#             service.users()
#             .messages()
#             .send(userId="me", body={"raw": raw_message})
#             .execute()
#         )
#         print(f"Message sent: {send_message['id']}")
#     except Exception as error:
#         print(f"An error occurred: {error}")


@dramatiq.actor
def notify_recipient(recipient_email: str, subject: str, body: str) -> None:
    send_gmail_email(recipient_email, subject, body)


# def notify_recipients(recipients: List[str], subject: str, body: str) -> None:
#     for recipient_email in recipients:
#         notify_recipient.send(recipient_email, subject, body)
