import uuid
from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    notes = relationship("Note", back_populates="owner")

class Note(Base):
    __tablename__ = "notes"

    id = Column(String, primary_key=True)
    title = Column(String(255))
    content = Column(Text)
    updated_at = Column(DateTime, default=datetime.now())
    user_id = Column(String, ForeignKey("users.id"))

    owner = relationship("User", back_populates="notes")
