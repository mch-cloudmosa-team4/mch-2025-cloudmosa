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
    jobs_list = jobs.search(db, search_str=search_str, skip=skip, limit=limit)
    return [JobResponse.model_validate(job) for job in jobs_list]