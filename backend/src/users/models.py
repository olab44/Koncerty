from sqlalchemy import Column, BigInteger, String, ForeignKey
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


class Member(Base):
    __tablename__ = "members"

    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    group_id = Column(BigInteger, ForeignKey("groups.id"), nullable=False)
    role = Column(String(15))

    user = relationship("User", back_populates="members")
    group = relationship("Group", back_populates="members")
