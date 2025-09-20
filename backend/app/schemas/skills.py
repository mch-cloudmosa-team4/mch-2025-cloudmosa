"""
Skill-related request/response schemas
"""

from datetime import datetime
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict, field_validator


class SkillBase(BaseModel):
    """Base skill schema"""
    name: str = Field(min_length=1, max_length=100, description="Skill name")
    
    @field_validator("name")
    @classmethod
    def validate_name(cls, v):
        if not v or not v.strip():
            raise ValueError("Skill name cannot be empty or contain only whitespace")
        return v.strip()


class SkillCreate(SkillBase):
    """Schema for skill creation"""
    pass


class SkillUpdate(BaseModel):
    """Schema for skill update"""
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="Skill name")
    
    @field_validator("name")
    @classmethod
    def validate_name(cls, v):
        if v is not None:
            return v.strip()
        return v


class SkillResponse(SkillBase):
    """Schema for skill response"""
    id: UUID = Field(description="Skill ID (UUID)")
    created_at: datetime = Field(description="Creation timestamp")
    
    model_config = ConfigDict(from_attributes=True)


class SkillSearchRequest(BaseModel):
    """Schema for skill search request"""
    keyword: str = Field(min_length=1, max_length=100, description="Search keyword")


class SkillSearchResponse(BaseModel):
    """Schema for skill search response"""
    keyword: str = Field(description="Search keyword used")
    skills: List[SkillResponse] = Field(description="List of matching skills")


class SkillListResponse(BaseModel):
    """Schema for skill list response"""
    skills: List[SkillResponse] = Field(description="List of skills")
    total: int = Field(description="Total number of skills")
    skip: int = Field(description="Number of skills skipped")
    limit: int = Field(description="Number of skills returned")


class SkillStatisticsResponse(BaseModel):
    """Schema for skill statistics response"""
    skill: SkillResponse = Field(description="Skill information")
    total_users: int = Field(description="Total number of users with this skill")
    average_level: float = Field(description="Average skill level among users")
    level_distribution: dict = Field(description="Distribution of skill levels")


class PopularSkillResponse(BaseModel):
    """Schema for popular skills response"""
    skill: SkillResponse = Field(description="Skill information")
    user_count: int = Field(description="Number of users with this skill")