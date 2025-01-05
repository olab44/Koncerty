from sqlalchemy import Column, BigInteger, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(50), nullable=False)
    members = relationship("Member", back_populates="user")


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

