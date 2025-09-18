"""
Item-related request/response schemas
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict, field_validator


class ItemBase(BaseModel):
    """Base item schema"""
    name: str = Field(min_length=1, max_length=100, description="Item name")
    description: Optional[str] = Field(None, max_length=500, description="Item description")
    price: float = Field(gt=0, description="Item price")
    is_active: bool = Field(True, description="Whether the item is active")


class ItemCreate(ItemBase):
    """Schema for item creation"""
    
    @field_validator("price")
    @classmethod
    def validate_price(cls, v):
        return round(v, 2)


class ItemUpdate(BaseModel):
    """Schema for item update"""
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="Item name")
    description: Optional[str] = Field(None, max_length=500, description="Item description")  
    price: Optional[float] = Field(None, gt=0, description="Item price")
    is_active: Optional[bool] = Field(None, description="Whether the item is active")
    
    @field_validator("price")
    @classmethod
    def validate_price(cls, v):
        if v is not None:
            return round(v, 2)
        return v


class ItemResponse(ItemBase):
    """Schema for item response"""
    id: int = Field(description="Item ID")
    created_at: datetime = Field(description="Creation timestamp")
    updated_at: datetime = Field(description="Last update timestamp")
    
    model_config = ConfigDict(from_attributes=True)
