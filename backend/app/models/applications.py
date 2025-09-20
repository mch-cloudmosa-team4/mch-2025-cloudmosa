"""
Application model for database storage - Job applications
"""

from datetime import datetime
from typing import Optional
import uuid
import enum
from sqlalchemy import Column, Text, DateTime, ForeignKey, Enum, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class ApplicationStatus(enum.Enum):
    """
    Application status enumeration
    """
    APPLIED = 0      # 已申請
    REVIEWING = 1    # 審核中
    ACCEPTED = 2     # 已接受
    REJECTED = 3     # 已拒絕
    WITHDRAWN = 4    # 已撤回


class Application(Base):
    """
    Application model for storing job applications
    """
    __tablename__ = "applications"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    applicant_user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    job_id = Column(UUID(as_uuid=True), ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False, index=True)
    message = Column(Text, nullable=True)  # Optional application message/cover letter
    status = Column(Enum(ApplicationStatus), default=ApplicationStatus.APPLIED, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    applicant = relationship("User", back_populates="applications")
    job = relationship("Job", back_populates="applications")
    
    # Constraints
    __table_args__ = (
        UniqueConstraint('job_id', 'applicant_user_id', name='unique_job_applicant'),
    )

    def __repr__(self):
        return f"<Application(id='{self.id}', job_id='{self.job_id}', applicant_user_id='{self.applicant_user_id}', status={self.status.value})>"