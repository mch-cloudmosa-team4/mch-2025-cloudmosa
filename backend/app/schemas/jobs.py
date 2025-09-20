"""
Job API request/response schemas
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, model_validator

from app.models import WorkType, JobStatus


class JobBase(BaseModel):
    employer_id: str = Field(None)
    title: str = Field(None)
    description: str = Field(None)
    reward: str = Field(None)
    work_type: WorkType = Field(None)
    required_people: int = Field(min_length=1, max_length=100)
    start_date: datetime = Field(None)
    status: JobStatus = Field(None)
    location_id: Optional[str] = Field(None)
    address: Optional[str] = Field(None)
    end_date: Optional[datetime] = Field(None)
    pictures: Optional[list[str]] = Field(None)

    @model_validator(mode="after")
    @classmethod
    def validate_end_date(cls, v):
        return v["end_date"] >= v["start_date"]


class JobCreate(JobBase):
    pass


class JobUpdate(JobBase):
    employer_id: Optional[str] = Field(None)
    title: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    reward: Optional[str] = Field(None)
    work_type: Optional[WorkType] = Field(None)
    required_people: Optional[int] = Field(min_length=1, max_length=100)
    start_date: Optional[datetime] = Field(None)
    status: Optional[JobStatus] = Field(None)


class JobResponse(JobBase):
    id: str = Field
    created_at: datetime
    updated_at: datetime

    @model_validator(mode="after")
    @classmethod
    def validate_update_at(cls, v):
        return v["update_at"] >= v["created_at"]