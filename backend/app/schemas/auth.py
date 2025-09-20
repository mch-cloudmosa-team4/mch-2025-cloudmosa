"""
Authentication-related request/response schemas
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator
import re

from app.utils import logger



class PhoneLoginRequest(BaseModel):
    """Schema for phone login/register request"""
    phone: str = Field(description="Phone number with country code (e.g., +2348012345678)")
    
    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v):
        # Basic phone number validation - starts with + followed by digits
        if not re.match(r'^\+\d{10,15}$', v):
            raise ValueError("Phone number must start with + and contain 10-15 digits")
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