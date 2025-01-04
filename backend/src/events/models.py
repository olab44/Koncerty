from sqlalchemy import Column, BigInteger, String, DateTime
from database import Base

class Event(Base):
    __tablename__ = 'events'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(30), nullable=False)
    date_start = Column(DateTime, nullable=False)
    date_end = Column(DateTime, nullable=False)
    description = Column(String(100), nullable=True)
    location = Column(String(50), nullable=False)