"""
Application API request/response schemas
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, model_validator

from app.models import ApplicationStatus


class ApplicationBase(BaseModel):
    applicant_user_id: str = Field(None)
    job_id: str = Field(None)
    message: str = Field("")


class ApplicationCreate(ApplicationBase):
    pass


class ApplicationUpdate(ApplicationBase):
    applicant_user_id: Optional[str] = Field(None)
    job_id: Optional[str] = Field(None)
    message: Optional[str] = Field("")
    status: Optional[ApplicationStatus] = Field(None)


class ApplicationResponse(ApplicationBase):
    id: str = Field
    created_at: datetime
    updated_at: datetime
    status: ApplicationStatus = Field(None)

    @model_validator(mode="after")
    @classmethod
    def validate_update_at(cls, v):
        return v["update_at"] >= v["created_at"]