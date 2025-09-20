"""
JobPicture model for database storage - Pictures associated with jobs
"""

from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class JobPicture(Base):
    """
    JobPicture model - Association table between jobs and picture files
    """
    __tablename__ = "job_pictures"
    
    # Composite primary key
    job_id = Column(UUID(as_uuid=True), ForeignKey("jobs.id", ondelete="CASCADE"), primary_key=True)
    file_id = Column(UUID(as_uuid=True), ForeignKey("files.id", ondelete="CASCADE"), primary_key=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    job = relationship("Job", back_populates="job_pictures")
    file = relationship("File", back_populates="job_pictures")

    def __repr__(self):
        return f"<JobPicture(job_id='{self.job_id}', file_id='{self.file_id}')>"