"""
Profile-related request/response schemas
"""

from datetime import datetime, date
from typing import Optional, List
from pydantic import BaseModel, Field, field_validator
from uuid import UUID
import re


class ProfileResponse(BaseModel):
    """Schema for profile response"""
    user_id: str = Field(description="User ID") 
    phone: str = Field(description="User's phone number")
    email: Optional[str] = Field(None, description="User's email")
    display_name: str = Field(description="User's display name")
    avatar_file_id: Optional[int] = Field(None, description="Avatar file ID")
    birthday: Optional[date] = Field(None, description="User's birthday")
    gender: str = Field(description="Gender")
    location_id: Optional[int] = Field(None, description="Location ID")
    bio: Optional[str] = Field(None, description="User's biography")
    primary_language_code: str = Field(description="Primary language code")
    created_at: datetime = Field(description="Profile creation timestamp")
    updated_at: datetime = Field(description="Profile last update timestamp")


class ProfileUpdateRequest(BaseModel):
    """Schema for profile update request"""
    display_name: Optional[str] = Field(None, description="User's display name")
    email: Optional[str] = Field(None, description="User's email")
    avatar_file_id: Optional[int] = Field(None, description="Avatar file ID")
    birthday: Optional[date] = Field(None, description="User's birthday")
    gender: Optional[str] = Field(None, description="Gender")
    location_id: Optional[int] = Field(None, description="Location ID")
    bio: Optional[str] = Field(None, description="User's biography")
    primary_language_code: Optional[str] = Field(None, description="Primary language code")
    
    @field_validator("gender")
    @classmethod
    def validate_gender(cls, v):
        if v not in ["male", "female", "other", "prefer_not_to_say"]:
            raise ValueError("Invalid gender value")
        return v
    
    @field_validator("email")
    @classmethod
    def validate_email(cls, v):
        if v and not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', v):
            raise ValueError("Invalid email format")
        return v


class ProfileListResponse(BaseModel):
    """Schema for profile list response (for GET /api/v1/profile)"""
    profiles: List[ProfileResponse] = Field(description="List of user profiles")


class ProfileUpdateResponse(BaseModel):
    """Schema for profile update response"""
    success: bool = Field(default=True, description="Update success status")
    message: str = Field(default="Profile updated successfully", description="Response message")
    profile: ProfileResponse = Field(description="Updated profile data")