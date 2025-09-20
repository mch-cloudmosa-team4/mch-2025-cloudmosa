"""
JobRequirement model for database storage - Skills required for jobs
"""

from datetime import datetime
from typing import Optional
from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy import ForeignKey

from app.database import Base


class JobRequirement(Base):
    """
    JobRequirement model - Association table between jobs and skills with minimum level requirements
    """
    __tablename__ = "job_requirements"
    
    # Composite primary key
    job_id = Column(UUID(as_uuid=True), ForeignKey("jobs.id", ondelete="CASCADE"), primary_key=True)
    skill_id = Column(UUID(as_uuid=True), ForeignKey("skills.id", ondelete="CASCADE"), primary_key=True)
    
    # Minimum skill level required (1-5, nullable)
    min_level = Column(Integer, nullable=True)  # If null, no specific level required
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    job = relationship("Job", back_populates="job_requirements")
    skill = relationship("Skill", back_populates="job_requirements")

    def __repr__(self):
        return f"<JobRequirement(job_id='{self.job_id}', skill_id='{self.skill_id}', min_level={self.min_level})>"