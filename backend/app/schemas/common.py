"""
Common request/response schemas
"""

from datetime import datetime
from typing import List, Optional, Any, Dict
from pydantic import BaseModel, Field


class PaginationMeta(BaseModel):
    """Pagination metadata"""
    page: int = Field(ge=1, description="Current page number")
    size: int = Field(ge=1, le=100, description="Page size")
    total: int = Field(ge=0, description="Total number of items")
    pages: int = Field(ge=0, description="Total number of pages")
    has_next: bool = Field(description="Whether there is a next page")
    has_prev: bool = Field(description="Whether there is a previous page")


class PaginatedResponse(BaseModel):
    """Generic paginated response"""
    data: List[Any] = Field(description="List of items")
    meta: PaginationMeta = Field(description="Pagination metadata")


class ApiError(BaseModel):
    """Standard API error response"""
    error: str = Field(description="Error type")
    message: str = Field(description="Human-readable error message")
    details: Optional[Dict[str, Any]] = Field(default=None, description="Additional error details")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ValidationError(BaseModel):
    """Validation error details"""
    field: str = Field(description="Field name that failed validation")
    message: str = Field(description="Validation error message")
    value: Optional[Any] = Field(default=None, description="Invalid value")


class ValidationErrorResponse(BaseModel):
    """Response for validation errors"""
    error: str = Field(default="validation_error", description="Error type")
    message: str = Field(default="Validation failed", description="Error message")
    errors: List[ValidationError] = Field(description="List of validation errors")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
