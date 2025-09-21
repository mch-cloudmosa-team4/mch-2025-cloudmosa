from typing import List
from fastapi import APIRouter, Query, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.crud import jobs
from app.schemas import JobResponse


router = APIRouter(
    tags=["jobs"],
    responses={
        404: {"description": "Not found"},
        422: {"description": "Validation error"}
    }
)


@router.get("/search/jobs", response_model=List[JobResponse], summary="List searched jobs")
async def search_jobs(
    search_str: str = Query("", description="Search string"),
    skip: int = Query(0, ge=0, description="Number of jobs to skip"),
    limit: int = Query(10, ge=1, le=100, description="Number of jobs to return"),
    db: Session = Depends(get_db)
) -> List[JobResponse]:
    print(f"search string: {search_str}")
    jobs_list = jobs.search(db, search_str=search_str, skip=skip, limit=limit)
    return [JobResponse(
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
        pictures=[],
        skills=[]
    ) for job in jobs_list]