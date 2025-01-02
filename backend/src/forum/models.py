from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, BigInteger
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Announcement(Base):
    __tablename__ = 'announcements'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    group_id = Column(Integer, ForeignKey('groups.id'), nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    group = relationship("Group", back_populates="announcements")
    user = relationship("User", back_populates="announcements")

    def __repr__(self):
        return f"<Announcement(id={self.id}, title={self.title}, created_at={self.created_at})>"


class Recipient(Base):
    __tablename__ = "recipients"

    id = Column(BigInteger, primary_key=True, index=True)
    member_id = Column(BigInteger, ForeignKey("members.id"), nullable=False)
    alert_id = Column(BigInteger, ForeignKey("alerts.id"), nullable=False)

    member = relationship("Member", back_populates="recipients")
    alert = relationship("Alert", back_populates="recipients")
