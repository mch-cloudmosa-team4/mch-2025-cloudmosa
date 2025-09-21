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
    res = []
    for job in jobs_list:
        skills = job_requirements.get(db, job_id=job.id)
        skills = [str(skill.skill_id) for skill in skills]
        pictures = job_pictures.get(db, job_id=job.id)
        pictures = [str(picture.job_id) for picture in pictures]
        res.append(
            JobResponse(
                id = str(job.id),
                employer_id = str(job.employer_id),
                title = job.title,
                description = job.description,
                location_id = str(job.location_id),
                reward = job.reward,
                address = job.address,
                work_type = job.work_type,
                required_people = job.required_people,
                start_date = job.start_date,
                end_date = job.end_date,
                status = job.status,
                created_at=job.created_at,
                updated_at=job.updated_at,
                pictures= pictures if pictures else [],
                skills= skills if skills else []
            )
        )
    return res


@router.get("/{job_id}", response_model=JobResponse, summary="Get job by ID")
async def get_job(
    job_id: str,
    db: Session = Depends(get_db)
) -> JobResponse:
    job = jobs.get(db, job_id=job_id)
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")

    skills = job_requirements.get(db, job_id=job.id)
    skills = [str(skill.skill_id) for skill in skills]
    pictures = job_pictures.get(db, job_id=job.id)
    pictures = [str(picture.job_id) for picture in pictures]
    
    return JobResponse(
        id = str(job.id),
        employer_id = str(job.employer_id),
        title = job.title,
        description = job.description,
        location_id = str(job.location_id),
        reward = job.reward,
        address = job.address,
        work_type = job.work_type,
        required_people = job.required_people,
        start_date = job.start_date,
        end_date = job.end_date,
        status = job.status,
        created_at=job.created_at,
        updated_at=job.updated_at,
        pictures= pictures if pictures else [],
        skills= skills if skills else []
    )


@router.post("/", response_model=JobResponse, status_code=status.HTTP_201_CREATED, summary="Create new job")
async def create_job(
    job_data: JobCreate,
    db: Session = Depends(get_db)
) -> JobResponse:
    pictures = job_data.pictures if job_data.pictures else []
    skill_ids = job_data.skills if job_data.skills else []

    created_job = jobs.create(db=db, obj_in=job_data)
    for picture_id in pictures:
        job_pictures.create(db, job_id=created_job.id, picture_id=picture_id)
    for skill_id in skill_ids:
        job_requirements.create(db, job_id=created_job.id, skill_id=skill_id)

    # if skill_ids:
    #     skill_ids = [str(skill.skill_id) for skill in skill_ids]
    # if pictures:
    #     pictures = [str(picture.job_id) for picture in pictures]

    return JobResponse(
        id = str(created_job.id),
        employer_id = str(created_job.employer_id),
        title = created_job.title,
        description = created_job.description,
        location_id = str(created_job.location_id),
        reward = created_job.reward,
        address = created_job.address,
        work_type = created_job.work_type,
        required_people = created_job.required_people,
        start_date = created_job.start_date,
        end_date = created_job.end_date,
        status = created_job.status,
        created_at=created_job.created_at,
        updated_at=created_job.updated_at,
        pictures=pictures,
        skills=skill_ids
    )


@router.put("/", response_model=JobResponse, summary="Update job")
async def update_job(
    job_update: JobUpdate,
    db: Session = Depends(get_db)
) -> JobResponse:
    job_id = job_update.id
    pictures = job_update.pictures if job_update.pictures is not None else job_pictures.get(db, job_id=job_id)
    skill_ids = job_update.skills if job_update.skills is not None else job_requirements.get(db, job_id=job_id)

    job_obj = jobs.get(db, job_id=job_id)
    if not job_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")

    updated_job = jobs.update(db=db, db_obj=job_obj, obj_in=job_update)

    if job_update.pictures is not None:
        job_pictures.delete(db, job_id=updated_job.id)
        for picture_id in pictures:
            job_pictures.create(db, job_id=updated_job.id, picture_id=picture_id)
    else:
        pictures = [str(picture.file_id) for picture in pictures]

    if job_update.skills is not None:
        # Test result: Not deleted
        job_requirements.delete(db, job_id=updated_job.id)
        for skill_id in skill_ids:
            job_requirements.create(db, job_id=updated_job.id, skill_id=skill_id, min_level=1)
    else:
        skill_ids = [str(skill.skill_id) for skill in skill_ids]

    return JobResponse(
        id = str(updated_job.id),
        employer_id = str(updated_job.employer_id),
        title = updated_job.title,
        description = updated_job.description,
        location_id = str(updated_job.location_id),
        reward = updated_job.reward,
        address = updated_job.address,
        work_type = updated_job.work_type,
        required_people = updated_job.required_people,
        start_date = updated_job.start_date,
        end_date = updated_job.end_date,
        status = updated_job.status,
        created_at=updated_job.created_at,
        updated_at=updated_job.updated_at,
        pictures=pictures,
        skills=skill_ids
    )


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