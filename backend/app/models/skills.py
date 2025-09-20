"""
Skill model for database storage
"""

from datetime import datetime
import uuid
from sqlalchemy import Column, DateTime
from sqlalchemy.dialects.postgresql import UUID, CITEXT
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database import Base


class Skill(Base):
    """
    Skill model for database storage
    """
    __tablename__ = "skills"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(CITEXT, unique=True, nullable=False, index=True)  # case-insensitive text
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user_skills = relationship("UserSkill", back_populates="skill", cascade="all, delete-orphan")
    job_requirements = relationship("JobRequirement", back_populates="skill", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Skill(id='{self.id}', name='{self.name}')>"