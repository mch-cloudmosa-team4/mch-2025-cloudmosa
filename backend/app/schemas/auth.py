"""
Authentication-related request/response schemas
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator
import re

from app.models.profiles import Gender
from app.utils import logger


class LoginRequest(BaseModel):
    """Schema for user login request - only requires phone and password"""
    phone: str = Field(description="Phone number with country code (e.g., +2348012345678)")
    passwd_hash: str = Field(description="User password hash")
    
    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v):
        # Basic phone number validation - starts with + followed by digits
        if not re.match(r'^\+\d+$', v):
            raise ValueError("Phone number must start with +")
        return v


class RegisterRequest(BaseModel):
    """Schema for user registration request - requires basic user information"""
    phone: str = Field(description="Phone number with country code (e.g., +2348012345678)")
    email: Optional[str] = Field(None, description="User email (optional)")
    passwd_hash: str = Field(description="User password hash")

    # Profile fields
    display_name: str = Field(description="User display name", min_length=1, max_length=100)
    avatar_file_id: Optional[str] = Field(None, description="Avatar file ID (optional)")
    birthday: Optional[datetime] = Field(None, description="User birthday (optional)")
    gender: str = Field(default="other", description="User gender (optional), default is others")
    location_id: Optional[str] = Field(None, description="Location ID (optional)")
    primary_language_code: str = Field(default="en", description="User's primary language code")
    
    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v):
        # Basic phone number validation - starts with + followed by digits
        if not re.match(r'^\+\d+$', v):
            raise ValueError("Phone number must start with +")
        return v
    
    @field_validator("email")
    @classmethod
    def validate_email(cls, v):
        if v and not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', v):
            raise ValueError("Invalid email format")
        return v

    @field_validator("gender")
    @classmethod
    def validate_gender(cls, v):
        if v not in ["male", "female", "other", "prefer_not_to_say"]:
            raise ValueError("Invalid gender value")
        return v


class PhoneLoginRequest(BaseModel):
    """Schema for phone login/register request - DEPRECATED, use LoginRequest or RegisterRequest"""
    phone: str = Field(description="Phone number with country code (e.g., +2348012345678)")
    passwd_hash: str = Field(description="Password for authentication")
    
    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v):
        # Basic phone number validation - starts with + followed by digits
        if not re.match(r'^\+\d+$', v):
            raise ValueError("Phone number must start with + and contain digits")
        return v


class TokenResponse(BaseModel):
    """Schema for token response"""
    access_token: str = Field(description="JWT access token")
    refresh_token: str = Field(description="JWT refresh token")
    token_type: str = Field(default="bearer", description="Token type")
    user: "UserInfo" = Field(description="User information")


class RefreshTokenRequest(BaseModel):
    """Schema for refresh token request"""
    refresh_token: str = Field(description="Refresh token to exchange for new access token")


class LogoutRequest(BaseModel):
    """Schema for logout request"""
    refresh_token: str = Field(description="Refresh token to revoke")


class UserInfo(BaseModel):
    """Basic user information"""
    user_id: str = Field(description="User ID")
    phone: str = Field(description="User's phone number")
    email: Optional[str] = Field(None, description="User's email (optional)")
    display_name: str = Field(description="User's display name")
    is_active: bool = Field(description="Whether user account is active")
    created_at: datetime = Field(description="Account creation timestamp")
    last_login_at: Optional[datetime] = Field(None, description="Last login timestamp")