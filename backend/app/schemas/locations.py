"""
Location-related request/response schemas
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator
from uuid import UUID
import re


class LocationResponse(BaseModel):
    """Schema for location response"""
    id: str = Field(description="Location ID")
    country: str = Field(description="Country name")
    country_code: str = Field(description="Country code (ISO 3166-1 alpha-2)")
    city: str = Field(description="City name")
    created_at: datetime = Field(description="Location creation timestamp")

    class Config:
        from_attributes = True


class LocationCreateRequest(BaseModel):
    """Schema for location creation request"""
    country: str = Field(description="Country name", min_length=1, max_length=255)
    country_code: str = Field(description="Country code (ISO 3166-1 alpha-2)", min_length=2, max_length=2)
    city: str = Field(description="City name", min_length=1, max_length=255)
    
    @field_validator("country_code")
    @classmethod
    def validate_country_code(cls, v):
        if not re.match(r'^[A-Z]{2}$', v.upper()):
            raise ValueError("Country code must be 2 uppercase letters (ISO 3166-1 alpha-2)")
        return v.upper()


class LocationUpdateRequest(BaseModel):
    """Schema for location update request"""
    country: Optional[str] = Field(None, description="Country name", min_length=1, max_length=255)
    country_code: Optional[str] = Field(None, description="Country code (ISO 3166-1 alpha-2)", min_length=2, max_length=2)
    city: Optional[str] = Field(None, description="City name", min_length=1, max_length=255)
    
    @field_validator("country_code")
    @classmethod
    def validate_country_code(cls, v):
        if v and not re.match(r'^[A-Z]{2}$', v.upper()):
            raise ValueError("Country code must be 2 uppercase letters (ISO 3166-1 alpha-2)")
        return v.upper() if v else v


class LocationSearchRequest(BaseModel):
    """Schema for location search request"""
    search_term: str = Field(description="Search term for country or city", min_length=1)
    skip: int = Field(0, description="Number of records to skip", ge=0)
    limit: int = Field(50, description="Maximum number of records to return", ge=1, le=100)


class LocationListResponse(BaseModel):
    """Schema for location list response"""
    locations: List[LocationResponse] = Field(description="List of locations")
    total: int = Field(description="Total number of locations")


class CountryResponse(BaseModel):
    """Schema for country response"""
    country: str = Field(description="Country name")
    country_code: str = Field(description="Country code (ISO 3166-1 alpha-2)")


class CountryListResponse(BaseModel):
    """Schema for country list response"""
    countries: List[CountryResponse] = Field(description="List of countries")


class CityListResponse(BaseModel):
    """Schema for city list response"""
    cities: List[str] = Field(description="List of city names")
    country: str = Field(description="Country name")


class PopularLocationResponse(BaseModel):
    """Schema for popular location response"""
    id: str = Field(description="Location ID")
    country: str = Field(description="Country name")
    country_code: str = Field(description="Country code")
    city: str = Field(description="City name")


class PopularLocationListResponse(BaseModel):
    """Schema for popular location list response"""
    locations: List[PopularLocationResponse] = Field(description="List of popular locations")


class LocationStatsResponse(BaseModel):
    """Schema for location statistics response"""
    total_locations: int = Field(description="Total number of locations")
    total_countries: int = Field(description="Total number of unique countries")