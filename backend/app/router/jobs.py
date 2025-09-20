"""
Jobs API router with database integration
"""

from typing import List
from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.crud import jobs
from app.schemas import JobCreate, JobUpdate, JobResponse
from app.models import BaseResponse


router = APIRouter(
    prefix="/jobs",
    tags=["jobs"],
    responses={
        404: {"description": "Not found"},
        422: {"description": "Validation error"}
    }
)

@router.get("/", response_model=List[JobResponse], summary="List all jobs")
async def list_jobs(
    skip: int = Query(0, ge=0, description="Number of jobs to skip"),
    limit: int = Query(10, ge=1, le=100, description="Number of jobs to return"),
    db: Session = Depends(get_db)
) -> List[JobResponse]:
    jobs_list = jobs.get_multi(db, skip=skip, limit=limit)
    return [JobResponse.model_validate(job) for job in jobs_list]


@router.get("/{job_id}", response_model=JobResponse, summary="Get job by ID")
async def get_job(
    job_id: int,
    db: Session = Depends(get_db)
) -> JobResponse:
    job = jobs.get(db, job_id=job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return JobResponse.model_validate(job)


@router.post("/", response_model=JobResponse, status_code=201, summary="Create new job")
async def create_job(
    job_data: JobCreate,
    db: Session = Depends(get_db)
) -> JobResponse:
    if job_data.pictures:
        # pictures = obj_in.pictures
        del job_data["pictures"]

    created_job = jobs.create(db=db, obj_in=job_data)
    return JobResponse.model_validate(created_job)


@router.put("/{job_id}", response_model=JobResponse, summary="Update job")
async def update_job(
    job_id: int,
    job_update: JobUpdate,
    db: Session = Depends(get_db)
) -> JobResponse:
    if job_update.pictures:
        # pictures = obj_in.pictures
        del job_update["pictures"]

    job_obj = jobs.get(db, job_id=job_id)
    if not job_obj:
        raise HTTPException(status_code=404, detail="Job not found")

    updated_job = jobs.update(db=db, db_obj=job_obj, obj_in=job_update)
    return JobResponse.model_validate(updated_job)


@router.delete("/{job_id}", response_model=BaseResponse, summary="Delete job")
async def delete_job(
    job_id: int,
    db: Session = Depends(get_db)
) -> BaseResponse:
    job_obj = jobs.delete(db=db, job_id=job_id)
    if not job_obj:
        raise HTTPException(status_code=404, detail="Job not found")

    return BaseResponse(message=f"Job {job_id} deleted successfully")