"""
Request and response schemas
"""

from typing import Optional, List, Any
from pydantic import BaseModel, Field, validator
from datetime import datetime


class PaginationParams(BaseModel):
    """Pagination parameters schema"""
    page: int = Field(1, ge=1, description="Page number")
    size: int = Field(10, ge=1, le=100, description="Page size")


class PaginatedResponseData(BaseModel):
    """Generic paginated response schema"""
    items: List[Any] = Field(description="List of items")
    page: int = Field(ge=1, description="Current page number")
    size: int = Field(ge=1, description="Page size")
    total: int = Field(ge=0, description="Total number of items")
    pages: int = Field(ge=0, description="Total number of pages")
    has_next: bool = Field(description="Whether there is a next page")
    has_prev: bool = Field(description="Whether there is a previous page")


class CreateItemRequest(BaseModel):
    """Schema for item creation request"""
    name: str = Field(min_length=1, max_length=100, description="Item name")
    description: Optional[str] = Field(None, max_length=500, description="Item description")
    price: float = Field(gt=0, description="Item price")
    is_active: bool = Field(True, description="Whether the item is active")
    
    @validator("price")
    def validate_price(cls, v):
        return round(v, 2)


class UpdateItemRequest(BaseModel):
    """Schema for item update request"""
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="Item name")
    description: Optional[str] = Field(None, max_length=500, description="Item description")
    price: Optional[float] = Field(None, gt=0, description="Item price")
    is_active: Optional[bool] = Field(None, description="Whether the item is active")
    
    @validator("price")
    def validate_price(cls, v):
        if v is not None:
            return round(v, 2)
        return v


class ItemResponse(BaseModel):
    """Schema for item response"""
    id: int = Field(description="Item ID")
    name: str = Field(description="Item name")
    description: Optional[str] = Field(description="Item description")
    price: float = Field(description="Item price")
    is_active: bool = Field(description="Whether the item is active")
    created_at: Optional[datetime] = Field(None, description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")


class ErrorDetail(BaseModel):
    """Error detail schema"""
    field: Optional[str] = Field(None, description="Field that caused the error")
    message: str = Field(description="Error message")
    type: Optional[str] = Field(None, description="Error type")


class ValidationErrorResponse(BaseModel):
    """Validation error response schema"""
    success: bool = Field(False, description="Operation success status")
    message: str = Field("Validation error", description="Error message")
    errors: List[ErrorDetail] = Field(description="List of validation errors")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Error timestamp")
