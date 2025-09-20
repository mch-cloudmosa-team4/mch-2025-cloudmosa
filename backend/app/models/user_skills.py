"""
UserSkill model for database storage - Association table between users and skills
"""

from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class UserSkill(Base):
    """
    UserSkill model - Association table between users and skills with proficiency level
    """
    __tablename__ = "user_skills"
    
    # Composite primary key
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    skill_id = Column(UUID(as_uuid=True), ForeignKey("skills.id", ondelete="CASCADE"), primary_key=True)
    
    # Proficiency level from 1 to 5
    level = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="user_skills")
    skill = relationship("Skill", back_populates="user_skills")
    
    # Constraints
    __table_args__ = (
        CheckConstraint('level >= 1 AND level <= 5', name='check_level_range'),
    )

    def __repr__(self):
        return f"<UserSkill(user_id='{self.user_id}', skill_id='{self.skill_id}', level={self.level})>"