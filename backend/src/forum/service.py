from sqlalchemy.orm import Session
from typing import List
import dramatiq
from email.mime.text import MIMEText
from smtplib import SMTP
from .config import settings
from users.models import Member, User, Alert
# from .models import Alert
from .schemas import AlertCreate, AlertInfo
import os
import base64
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from .config import settings

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

def create_Alert(db: Session, creator_id: int, data: AlertCreate) -> Alert:
    new_Alert = Alert(
        title=data.title,
        content=data.content,
        creator_id=creator_id,
        group_id=data.group_id
    )
    db.add(new_Alert)
    db.commit()
    db.refresh(new_Alert)

    # Fetch recipients and send notifications
    recipients = get_recipients(db, data.group_id)
    notify_recipients(
        recipients=recipients,
        subject=f"New Alert: {data.title}",
        body=data.content,
    )

    return new_Alert


def get_Alerts(db: Session, group_id: int) -> List[AlertInfo]:
    query = db.query(Alert).filter(Alert.group_id == group_id)
    return query.all()


def get_recipients(db: Session, group_id: int) -> List[str]:
    """
    Fetch email addresses of users in the specified group or subgroup.
    """
    query = db.query(User).join(Member).filter(Member.group_id == group_id)
    return [user.email for user in query.all()]


def compose_message(recipient_email: str, subject: str, body: str) -> MIMEText:
    """
    Compose an email message.
    """
    message = MIMEText(body, "plain")
    message["Subject"] = subject
    message["From"] = settings.EMAIL_ADDRESS
    message["To"] = recipient_email
    return message


# def send_email(message: MIMEText) -> None:
#     with SMTP(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
#         server.starttls()
#         server.login(settings.EMAIL_ADDRESS, settings.EMAIL_PASSWORD)
#         server.sendmail(settings.EMAIL_ADDRESS, [message["To"]], message.as_string())

def get_gmail_service():
    """Authenticate with Gmail API and return the service object."""
    creds = None
    # Load credentials from the token file
    if os.path.exists(settings.TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(settings.TOKEN_FILE, SCOPES)
    # If credentials are invalid or not available, reauthenticate
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(settings.GMAIL_CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(settings.TOKEN_FILE, "w") as token_file:
            token_file.write(creds.to_json())
    return build("gmail", "v1", credentials=creds)


def send_gmail_email(recipient_email: str, subject: str, body: str):
    """Send an email via Gmail API."""
    service = get_gmail_service()
    message = MIMEText(body)
    message["to"] = recipient_email
    message["subject"] = subject
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    try:
        send_message = (
            service.users()
            .messages()
            .send(userId="me", body={"raw": raw_message})
            .execute()
        )
        print(f"Message sent: {send_message['id']}")
    except Exception as error:
        print(f"An error occurred: {error}")


@dramatiq.actor
def notify_recipient(recipient_email: str, subject: str, body: str) -> None:
    send_gmail_email(recipient_email, subject, body)


def notify_recipients(recipients: List[str], subject: str, body: str) -> None:
    for recipient_email in recipients:
        notify_recipient.send(recipient_email, subject, body)
