"""
Files API request/response schemas
"""

from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict, HttpUrl


class FileCreate(BaseModel):
    """Base file schema"""
    mime_type: str = Field(description="MIME type")
    size_bytes: int = Field(ge=0, description="File size in bytes")


class FileUpdate(BaseModel):
    """Payload for updating a File record (partial)"""
    mime_type: Optional[str] = Field(default=None, description="MIME type")
    size_bytes: Optional[int] = Field(default=None, ge=0, description="File size in bytes")


class FileUploadResponse(BaseModel):
    """Schema for returning File ORM objects (matches DB fields)"""
    id: UUID = Field(description="File ID (also used as MinIO object key)")
    mime_type: str = Field(description="MIME type")
    size_bytes: int = Field(ge=0, description="File size in bytes")
    created_at: datetime = Field(description="Creation timestamp")

    model_config = ConfigDict(from_attributes=True)


class FilePresignResponse(BaseModel):
    """Response containing a presigned URL for downloading an object"""
    url: HttpUrl = Field(description="Time-limited presigned URL for the object")