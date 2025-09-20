"""
Job model for database storage - Job postings and opportunities
"""

from datetime import datetime, date
from typing import Optional
import uuid
import enum
from sqlalchemy import Column, String, Text, Integer, Date, DateTime, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from pgvector.sqlalchemy import Vector
from pydantic import model_validator

from app.database import Base
from app.config import settings
from app.utils import embed_encode


class WorkType(enum.Enum):
    """
    Work type enumeration
    """
    SHORT = "short"      # 短期工作
    LONG = "long"        # 長期工作
    ONE_TIME = "one_time"  # 一次性工作


class JobStatus(enum.Enum):
    """
    Job status enumeration
    """
    DRAFT = "draft"           # 草稿
    PUBLISHED = "published"   # 已發布
    PAUSED = "paused"        # 暫停
    COMPLETED = "completed"   # 已完成
    CANCELLED = "cancelled"   # 已取消


class Job(Base):
    """
    Job model for storing job postings and opportunities
    """
    __tablename__ = "jobs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    employer_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    reward = Column(Text, nullable=False)  # Can be monetary amount, points, or other rewards
    location_id = Column(UUID(as_uuid=True), ForeignKey("locations.id", ondelete="SET NULL"), nullable=True, index=True)
    address = Column(Text, nullable=True)  # Specific address details
    work_type = Column(Enum(WorkType), nullable=False)
    required_people = Column(Integer, nullable=False)  # Number of people needed
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)  # Optional for one-time jobs
    status = Column(Enum(JobStatus), default=JobStatus.DRAFT, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    embedding = Column(Vector(settings.embedding_model_dimension), nullable=False)
    
    # Relationships
    employer = relationship("User", back_populates="employer_jobs")
    location = relationship("Location", back_populates="jobs")
    applications = relationship("Application", back_populates="job", cascade="all, delete-orphan")
    job_requirements = relationship("JobRequirement", back_populates="job", cascade="all, delete-orphan")
    job_pictures = relationship("JobPicture", back_populates="job", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Job(id='{self.id}', title='{self.title}', employer_id='{self.employer_id}', status='{self.status.value}')>"

    @model_validator(mode="after")
    def calculate_embedding(cls, values):
        values["embedding"] = embed_encode(values["title"] + " " + values["description"])
        return values