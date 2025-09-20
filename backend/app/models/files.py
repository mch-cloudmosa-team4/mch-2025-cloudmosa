"""
File model for database storage - File metadata and storage references
"""

from datetime import datetime
import uuid
from sqlalchemy import Column, String, Text, BigInteger, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class File(Base):
    """
    File model for storing file metadata and storage references
    """
    __tablename__ = "files"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    object_key = Column(Text, nullable=False)  # Object key (e.g., images/1234567890.jpg)
    mime_type = Column(Text, nullable=False)  # MIME type (e.g., image/jpeg, application/pdf)
    size_bytes = Column(BigInteger, nullable=False)  # File size in bytes
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    avatar_profiles = relationship("Profile", foreign_keys="Profile.avatar_file_id", back_populates="avatar_file")
    job_pictures = relationship("JobPicture", back_populates="file", cascade="all, delete-orphan")
    messages = relationship("Message", back_populates="file")

    def __repr__(self):
        return f"<File(id='{self.id}', mime_type='{self.mime_type}', size_bytes={self.size_bytes})>"