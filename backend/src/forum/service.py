from sqlalchemy.orm import Session
from typing import List
import dramatiq
from email.mime.text import MIMEText
from smtplib import SMTP
from .config import settings
from users.models import Member, User
from .models import Announcement
from .schemas import AnnouncementCreate, AnnouncementInfo


def create_announcement(db: Session, creator_id: int, data: AnnouncementCreate) -> Announcement:
    new_announcement = Announcement(
        title=data.title,
        content=data.content,
        creator_id=creator_id,
        group_id=data.group_id,
        subgroup_id=data.subgroup_id,
    )
    db.add(new_announcement)
    db.commit()
    db.refresh(new_announcement)

    # Fetch recipients and send notifications
    recipients = get_recipients(db, data.group_id, data.subgroup_id)
    notify_recipients(
        recipients=recipients,
        subject=f"New Announcement: {data.title}",
        body=data.content,
    )

    return new_announcement


def get_announcements(db: Session, group_id: int = None, subgroup_id: int = None) -> List[AnnouncementInfo]:
    query = db.query(Announcement)
    if group_id:
        query = query.filter(Announcement.group_id == group_id)
    if subgroup_id:
        query = query.filter(Announcement.subgroup_id == subgroup_id)
    return query.all()


def get_recipients(db: Session, group_id: int = None, subgroup_id: int = None) -> List[str]:
    """
    Fetch email addresses of users in the specified group or subgroup.
    """
    query = db.query(User).join(Member)
    if group_id:
        query = query.filter(Member.group_id == group_id)
    if subgroup_id:
        query = query.filter(Member.subgroup_id == subgroup_id)
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


def send_email(message: MIMEText) -> None:
    with SMTP(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
        server.starttls()
        server.login(settings.EMAIL_ADDRESS, settings.EMAIL_PASSWORD)
        server.sendmail(settings.EMAIL_ADDRESS, [message["To"]], message.as_string())


@dramatiq.actor
def notify_recipient(recipient_email: str, subject: str, body: str) -> None:
    message = compose_message(recipient_email, subject, body)
    send_email(message)


def notify_recipients(recipients: List[str], subject: str, body: str) -> None:
    for recipient_email in recipients:
        notify_recipient.send(recipient_email, subject, body)
