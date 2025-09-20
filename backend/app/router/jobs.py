"""
Jobs API router with database integration
"""

from typing import List
from fastapi import APIRouter, HTTPException, Query, status, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.crud import jobs, job_requirements, job_pictures
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
    for i, job in enumerate(jobs_list):
        skills = job_requirements.get(db, job_id=job.id)
        skills = [skill.skill_id for skill in skills]
        jobs_list[i]["skills"] = skills
        pictures = job_pictures.get(db, job_id=job.id)
        pictures = [picture.job_id for picture in pictures]
        jobs_list[i]["pictures"] = pictures
    return [JobResponse.model_validate(job) for job in jobs_list]


@router.get("/{job_id}", response_model=JobResponse, summary="Get job by ID")
async def get_job(
    job_id: str,
    db: Session = Depends(get_db)
) -> JobResponse:
    job = jobs.get(db, job_id=job_id)
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")

    skills = job_requirements.get(db, job_id=job.id)
    skills = [skill.skill_id for skill in skills]
    job["skills"] = skills
    pictures = job_pictures.get(db, job_id=job.id)
    pictures = [picture.job_id for picture in pictures]
    job["pictures"] = pictures
    return JobResponse.model_validate(job)


@router.post("/", response_model=JobResponse, status_code=status.HTTP_201_CREATED, summary="Create new job")
async def create_job(
    job_data: JobCreate,
    db: Session = Depends(get_db)
) -> JobResponse:
    if job_data.pictures:
        pictures = job_data["pictures"]
        del job_data["pictures"]

    if job_data.skills:
        skill_ids = job_data["skills"]
        del job_data["skills"]

    created_job = jobs.create(db=db, obj_in=job_data)
    for picture_id in pictures:
        job_pictures.create(db, job_id=created_job.id, picture_id=picture_id)
    for skill_id in skill_ids:
        job_requirements.create(db, job_id=created_job.id, skill_id=skill_id)
    return JobResponse.model_validate(created_job)


@router.put("/{job_id}", response_model=JobResponse, summary="Update job")
async def update_job(
    job_id: str,
    job_update: JobUpdate,
    db: Session = Depends(get_db)
) -> JobResponse:
    if job_update.pictures:
        pictures = job_update["pictures"]
        del job_update["pictures"]

    if job_update.skills:
        skill_ids = job_update["skills"]
        del job_update["skills"]

    job_obj = jobs.get(db, job_id=job_id)
    if not job_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")

    updated_job = jobs.update(db=db, db_obj=job_obj, obj_in=job_update)
    job_pictures.delete(db, job_id=updated_job.id)
    job_requirements.delete(db, job_id=updated_job.id)
    for picture_id in pictures:
        job_pictures.create(db, job_id=updated_job.id, picture_id=picture_id)
    for skill_id in skill_ids:
        job_requirements.create(db, job_id=updated_job.id, skill_id=skill_id)
    return JobResponse.model_validate(updated_job)


@router.delete("/{job_id}", response_model=BaseResponse, summary="Delete job")
async def delete_job(
    job_id: str,
    db: Session = Depends(get_db)
) -> BaseResponse:
    job_obj = jobs.delete(db=db, job_id=job_id)
    if not job_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")

    job_pictures.delete(db, job_id=job_id)
    job_requirements.delete(db, job_id=job_id)
    return BaseResponse(message=f"Job {job_id} deleted successfully")