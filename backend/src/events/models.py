from sqlalchemy import Column, BigInteger, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Event(Base):
    __tablename__ = 'events'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(30), nullable=False)
    date_start = Column(DateTime, nullable=False)
    date_end = Column(DateTime, nullable=False)
    description = Column(String(100))
    location = Column(String(50), nullable=False)

    participations = relationship("Participation", back_populates="event")
    set_lists = relationship("SetList", back_populates="event")

class Participation(Base):
    __tablename__ = 'participations'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    event_id = Column(BigInteger, ForeignKey('public.events.id'), nullable=False)
    group_id = Column(BigInteger, nullable=False)

    event = relationship("Event", back_populates="participations")

class SetList(Base):
    __tablename__ = 'set_lists'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    event_id = Column(BigInteger, ForeignKey('public.events.id'), nullable=False)
    composition_id = Column(BigInteger, nullable=False)

    event = relationship("Event", back_populates="set_lists")
