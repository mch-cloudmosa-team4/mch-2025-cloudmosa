"""
Job API request/response schemas
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, model_validator

from app.models import WorkType, JobStatus


class JobBase(BaseModel):
    employer_id: str = Field()
    title: str = Field()
    description: str = Field()
    reward: str = Field()
    work_type: WorkType = Field()
    required_people: int = Field()
    start_date: datetime = Field()
    status: JobStatus = Field()
    location_id: Optional[str] = Field(None)
    address: Optional[str] = Field(None)
    end_date: Optional[datetime] = Field(None)
    pictures: Optional[list[str]] = Field(None)
    skills: Optional[list[str]] = Field(None)


class JobCreate(JobBase):
    pass


class JobUpdate(JobBase):
    id: str = Field()
    employer_id: Optional[str] = Field(None)
    title: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    reward: Optional[str] = Field(None)
    work_type: Optional[WorkType] = Field(None)
    required_people: Optional[int] = Field(None)
    start_date: Optional[datetime] = Field(None)
    status: Optional[JobStatus] = Field(None)


class JobResponse(JobBase):
    id: str = Field()
    created_at: datetime = Field()
    updated_at: datetime = Field()
