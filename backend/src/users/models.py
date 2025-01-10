from sqlalchemy import Column, BigInteger, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(50), nullable=False)

    members = relationship("Member", back_populates="user")
    file_ownerships = relationship("FileOwnership", back_populates="user")


class Group(Base):
    __tablename__ = "groups"

    id = Column(BigInteger, primary_key=True, index=True)
    parent_group = Column(BigInteger, nullable=True)
    name = Column(String(30), nullable=False)
    extra_info = Column(String(100))
    invitation_code = Column(String(20), nullable=False)

    members = relationship("Member", back_populates="group")
    events = relationship(
        "Event",
        back_populates="group",
        primaryjoin="Group.id == Event.parent_group" )


class Member(Base):
    __tablename__ = "members"

    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    group_id = Column(BigInteger, ForeignKey("groups.id"), nullable=False)
    role = Column(String(15))

    user = relationship("User", back_populates="members")
    group = relationship("Group", back_populates="members")
    recipients = relationship("Recipient", back_populates="member")


class Event(Base):
    __tablename__ = 'events'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    date_start = Column(DateTime, nullable=False)
    date_end = Column(DateTime, nullable=False)
    location = Column(String(100), nullable=False)
    extra_info = Column(String(100), nullable=True)
    parent_group = Column(BigInteger, ForeignKey('groups.id'), nullable=False)
    type = Column(String(8), nullable=False)

    participations = relationship("Participation", back_populates="event")
    set_lists = relationship("SetList", back_populates="event")

    group = relationship("Group", back_populates="events")


class Participation(Base):
    __tablename__ = 'participations'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    event_id = Column(BigInteger, ForeignKey('events.id'), nullable=False)
    user_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)

    event = relationship("Event", back_populates="participations")


class SetList(Base):
    __tablename__ = 'set_lists'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    event_id = Column(BigInteger, ForeignKey('events.id'), nullable=False)
    composition_id = Column(BigInteger, ForeignKey('compositions.id'), nullable=False)

    event = relationship("Event", back_populates="set_lists")
    composition = relationship("Composition", back_populates="set_lists")


class Composition(Base):
    __tablename__ = 'compositions'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    author = Column(String(40), nullable=True)

    set_lists = relationship("SetList", back_populates="composition")
    files = relationship("File", back_populates="composition")


class File(Base):
    __tablename__ = "files"

    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    google_drive_id = Column(String(50), nullable=True)
    composition_id = Column(BigInteger, ForeignKey("compositions.id"), nullable=True)

    composition = relationship("Composition", back_populates="files", lazy="joined")
    ownerships = relationship("FileOwnership", back_populates="file")


class FileOwnership(Base):
    __tablename__ = "file_ownerships"

    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    file_id = Column(BigInteger, ForeignKey("files.id"), nullable=False)

    user = relationship("User", back_populates="file_ownerships")
    file = relationship("File", back_populates="ownerships")


class Alert(Base):
    __tablename__ = "alerts"
    id = Column(BigInteger, primary_key=True, index=True)
    title = Column(String(150), nullable=False)
    content = Column(String(400), nullable=False)
    date_sent = Column(DateTime, default=datetime.utcnow)

    recipients = relationship("Recipient", back_populates="alert")


class Recipient(Base):
    __tablename__ = "recipients"
    id = Column(BigInteger, primary_key=True, index=True)
    alert_id = Column(BigInteger, ForeignKey("alerts.id"), nullable=False)
    member_id = Column(BigInteger, ForeignKey("members.id"), nullable=False)

    alert = relationship("Alert", back_populates="recipients")
    member = relationship("Member", back_populates="recipients")
