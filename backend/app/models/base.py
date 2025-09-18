"""
Common base models for the application
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class BaseResponse(BaseModel):
    """Base response model"""
    success: bool = Field(default=True, description="Operation success status")
    message: str = Field(default="Operation completed successfully", description="Response message")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Response timestamp")


class ErrorResponse(BaseModel):
    """Error response model"""
    success: bool = Field(default=False, description="Operation success status")
    message: str = Field(description="Error message")
    error_code: Optional[str] = Field(default=None, description="Error code")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Response timestamp")


class HealthCheck(BaseModel):
    """Health check response model"""
    status: str = Field(default="healthy", description="Service status")
    version: str = Field(description="Application version")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Health check timestamp")


class PaginatedResponse(BaseModel):
    """Base model for paginated responses"""
    page: int = Field(ge=1, description="Current page number")
    size: int = Field(ge=1, le=100, description="Page size")
    total: int = Field(ge=0, description="Total number of items")
    pages: int = Field(ge=0, description="Total number of pages")
    has_next: bool = Field(description="Whether there is a next page")
    has_prev: bool = Field(description="Whether there is a previous page")


# Re-export commonly used models
__all__ = [
    "BaseResponse",
    "ErrorResponse", 
    "HealthCheck",
    "PaginatedResponse"
]
