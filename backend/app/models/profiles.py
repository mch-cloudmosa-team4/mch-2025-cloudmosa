"""
User Profile model for database storage
"""

from datetime import datetime, date
from typing import Optional
import uuid
from sqlalchemy import Column, String, Text, Date, DateTime, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.database import Base


class Gender(enum.Enum):
    """
    Gender enumeration
    """
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
    PREFER_NOT_TO_SAY = "prefer_not_to_say"


class Profile(Base):
    """
    User Profile model for database storage
    """
    __tablename__ = "profiles"
    
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), primary_key=True, index=True)
    display_name = Column(Text, nullable=False)
    avatar_file_id = Column(UUID(as_uuid=True), ForeignKey('files.id', ondelete='SET NULL'), nullable=True, index=True)
    birthday = Column(Date, nullable=True)
    gender = Column(Enum(Gender), nullable=False)
    location_id = Column(UUID(as_uuid=True), ForeignKey('locations.id', ondelete='SET NULL'), nullable=True, index=True)
    bio = Column(Text, nullable=True)
    primary_language_code = Column(String(10), nullable=False)  # ISO 639-1 language codes (e.g., 'en', 'zh-TW')
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="profile")
    avatar_file = relationship("File", foreign_keys=[avatar_file_id], back_populates="avatar_profiles")
    location = relationship("Location", back_populates="profiles")

    def __repr__(self):
        return f"<Profile(user_id='{self.user_id}', display_name='{self.display_name}')>"
