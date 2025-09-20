"""
Application API router with database integration
"""

from typing import List
from fastapi import APIRouter, HTTPException, Query, status, Depends
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.crud import applications
from app.schemas import ApplicationCreate, ApplicationUpdate, ApplicationResponse
from app.models import BaseResponse
from app.dependencies import get_current_user
from app.models import User, ApplicationStatus


router = APIRouter(
    prefix="/applications",
    tags=["applications"],
    responses={
        404: {"description": "Not found"},
        422: {"description": "Validation error"}
    }
)


@router.get("/", response_model=List[ApplicationResponse], summary="List all applications")
async def list_applications(
    skip: int = Query(0, ge=0, description="Number of applications to skip"),
    limit: int = Query(10, ge=1, le=100, description="Number of applications to return"),
    status: Optional[ApplicationStatus] = Query(None, description="Filter application status"),
    db: Session = Depends(get_db)
) -> List[ApplicationResponse]:
    if status:
        applications_list = applications.get_multi(db, skip=skip, limit=limit, status=status)
    else:
        applications_list = applications.get_multi(db, skip=skip, limit=limit)
    return [ApplicationResponse.model_validate(application) for application in applications_list]


@router.get("/me", response_model=List[ApplicationResponse], summary="My applications")
async def my_applications(
    skip: int = Query(0, ge=0, description="Number of applications to skip"),
    limit: int = Query(10, ge=1, le=100, description="Number of applications to return"),
    status: Optional[ApplicationStatus] = Query(None, description="Filter application status"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> List[ApplicationResponse]:
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )

    if status:
        applications_list = applications.get_by_userid(db, user_id=current_user.id, skip=skip, limit=limit, status=status)
    else:
        applications_list = applications.get_by_userid(db, user_id=current_user.id, skip=skip, limit=limit)
    return [ApplicationResponse.model_validate(application) for application in applications_list]


@router.get("/{application_id}", response_model=ApplicationResponse, summary="Get application by ID")
async def get_application(
    application_id: int,
    db: Session = Depends(get_db)
) -> ApplicationResponse:
    application = applications.get(db, application_id=application_id)
    if not application:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")
    return ApplicationResponse.model_validate(application)


@router.post("/", response_model=ApplicationResponse, status_code=201, summary="Create new application")
async def create_application(
    application_data: ApplicationCreate,
    db: Session = Depends(get_db)
) -> ApplicationResponse:
    created_application = applications.create(db=db, obj_in=application_data)
    return ApplicationResponse.model_validate(created_application)


@router.put("/{application_id}", response_model=ApplicationResponse, summary="Update application")
async def update_application(
    application_id: int,
    application_update: ApplicationUpdate,
    db: Session = Depends(get_db)
) -> ApplicationResponse:
    application_obj = applications.get(db, application_id=application_id)
    if not application_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")

    updated_application = applications.update(db=db, db_obj=application_obj, obj_in=application_update)
    return ApplicationResponse.model_validate(updated_application)


@router.delete("/{application_id}", response_model=BaseResponse, summary="Delete application")
async def delete_application(
    application_id: int,
    db: Session = Depends(get_db)
) -> BaseResponse:
    application_obj = applications.delete(db=db, application_id=application_id)
    if not application_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")

    return BaseResponse(message=f"Application {application_id} deleted successfully")