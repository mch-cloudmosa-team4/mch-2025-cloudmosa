"""
User Skills related request/response schemas
"""

from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, Field, field_validator, ConfigDict
from datetime import datetime

from app.schemas.skills import SkillResponse


class UserSkillBase(BaseModel):
    """Base user skill schema"""
    level: int = Field(ge=1, le=5, description="Skill proficiency level (1-5)")


class UserSkillCreate(UserSkillBase):
    """Schema for creating user skill"""
    skill_id: UUID = Field(description="Skill ID")


class UserSkillUpdate(UserSkillBase):
    """Schema for updating user skill"""
    skill_id: UUID = Field(description="Skill ID")


class UserSkillResponse(UserSkillBase):
    """Schema for user skill response"""
    user_id: UUID = Field(description="User ID")
    skill_id: UUID = Field(description="Skill ID")
    created_at: datetime = Field(description="Creation timestamp")
    
    # Optional related objects
    skill: Optional[SkillResponse] = Field(None, description="Skill details")
    
    model_config = ConfigDict(from_attributes=True)


class UserSkillsRequest(BaseModel):
    """Schema for batch user skills update"""
    skills: List[UserSkillUpdate] = Field(description="List of skills to update")
    
    @field_validator("skills")
    @classmethod
    def validate_skills(cls, v):
        if not v:
            raise ValueError("At least one skill is required")
        
        # Check for duplicate skill_ids
        skill_ids = [skill.skill_id for skill in v]
        if len(skill_ids) != len(set(skill_ids)):
            raise ValueError("Duplicate skill IDs are not allowed")
        
        return v


class SkillSummary(BaseModel):
    """Simple skill summary for user skills response"""
    id: UUID = Field(description="Skill ID")
    name: str = Field(description="Skill name")


class UserSkillSummary(BaseModel):
    """User skill summary with skill details"""
    id: UUID = Field(description="Skill ID")
    name: str = Field(description="Skill name")
    level: int = Field(description="Proficiency level")


class UserSkillsResponse(BaseModel):
    """Schema for user skills response"""
    user_id: str = Field(description="User ID")  # Change to str to match API requirement
    skills: List[UserSkillSummary] = Field(description="User's skills")


class MultipleUserSkillsResponse(BaseModel):
    """Schema for multiple users' skills response"""
    users: List[UserSkillsResponse] = Field(description="List of users with their skills")


class UserSkillsStats(BaseModel):
    """Schema for user skills statistics"""
    total_skills: int = Field(description="Total number of skills")
    skill_levels: dict = Field(description="Distribution of skill levels")
    average_level: float = Field(description="Average skill level")


class SkillUsersResponse(BaseModel):
    """Schema for users who have a specific skill"""
    skill: SkillResponse = Field(description="Skill details")
    users: List[UserSkillResponse] = Field(description="Users with this skill")
    total_users: int = Field(description="Total number of users with this skill")