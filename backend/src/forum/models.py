# from datetime import datetime
# from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
# from sqlalchemy.orm import relationship
# from sqlalchemy.ext.declarative import declarative_base

# Base = declarative_base()


# class Announcement(Base):
#     __tablename__ = "announcements"
#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String, nullable=False)
#     content = Column(Text, nullable=False)
#     creator_id = Column(Integer, ForeignKey("users.id"), nullable=False)
#     group_id = Column(Integer, ForeignKey("groups.id"), nullable=True)
#     subgroup_id = Column(Integer, ForeignKey("subgroups.id"), nullable=True)
#     created_at = Column(DateTime, default=datetime.utcnow)

#     creator = relationship("User", back_populates="announcements")
#     group = relationship("Group", back_populates="announcements")
#     subgroup = relationship("Subgroup", back_populates="announcements")
