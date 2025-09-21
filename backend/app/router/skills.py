"""
Skills API router with database integration
"""

from typing import List
from fastapi import APIRouter, HTTPException, Query, Depends, status, Request
from fastapi.exceptions import RequestValidationError
from sqlalchemy.orm import Session
from pydantic import ValidationError

from app.database import get_db
from app.crud import skills, user_skills
from app.schemas import (
    SkillResponse,
    SkillSearchResponse, 
    SkillListResponse,
    SkillCreate,
    SkillStatisticsResponse,
    PopularSkillResponse
)
from app.models import BaseResponse


router = APIRouter(
    prefix="/skills",
    tags=["skills"],
    responses={
        404: {"description": "Not found"},
        422: {"description": "Validation error"}
    }
)


@router.get("/search", response_model=SkillSearchResponse, summary="Search skills by keyword")
async def search_skills(
    keyword: str = Query(..., min_length=1, max_length=100, description="Search keyword"),
    skip: int = Query(0, ge=0, description="Number of skills to skip"),
    limit: int = Query(20, ge=1, le=100, description="Number of skills to return"),
    db: Session = Depends(get_db)
) -> SkillSearchResponse:
    """
    Search skills by keyword (case-insensitive partial matching).
    
    - **keyword**: The keyword to search for in skill names
    - **skip**: Number of results to skip (for pagination)
    - **limit**: Maximum number of results to return
    """
    skill_list = skills.search_by_name(db, name_pattern=keyword, skip=skip, limit=limit)
    
    skill_responses = [SkillResponse.model_validate(skill) for skill in skill_list]
    
    return SkillSearchResponse(
        keyword=keyword,
        skills=skill_responses
    )


@router.get("/", response_model=List[SkillResponse], summary="Get skills by IDs")
async def get_skills(
    skill_ids: List[str] = Query(..., description="List of skill IDs (UUIDs) to retrieve"),
    db: Session = Depends(get_db)
) -> List[SkillResponse]:
    """
    Get multiple skills by their IDs.
    
    - **skill_ids**: List of UUIDs of the skills to retrieve
    
    Returns only the skills that exist. Non-existent skill IDs are silently ignored.
    """
    if not skill_ids:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one skill_id is required"
        )
    
    skill_list = skills.get_multi(db, skill_ids=skill_ids)
    
    return [SkillResponse.model_validate(skill) for skill in skill_list]


@router.get("/all", response_model=SkillListResponse, summary="List all skills")
async def list_skills(
    skip: int = Query(0, ge=0, description="Number of skills to skip"),
    limit: int = Query(50, ge=1, le=200, description="Number of skills to return"),
    db: Session = Depends(get_db)
) -> SkillListResponse:
    """
    Get all skills with pagination support.
    
    - **skip**: Number of skills to skip (for pagination)
    - **limit**: Maximum number of skills to return
    """
    skill_list = skills.get_multi(db, skip=skip, limit=limit)
    total_count = skills.count(db)
    
    skill_responses = [SkillResponse.model_validate(skill) for skill in skill_list]
    
    return SkillListResponse(
        skills=skill_responses,
        total=total_count,
        skip=skip,
        limit=limit
    )


@router.post("/", response_model=SkillResponse, status_code=status.HTTP_201_CREATED, summary="Create a new skill")
async def create_skill(
    skill_data: SkillCreate,
    db: Session = Depends(get_db)
) -> SkillResponse:
    """
    Create a new skill. If the skill already exists, return the existing one.
    
    - **name**: Name of the skill to create
    
    Validation rules:
    - Name must be between 1-100 characters
    - Name cannot be only whitespace
    - Leading/trailing whitespace will be automatically trimmed
    """
    try:
        # Check if skill already exists (name is already validated by Pydantic)
        existing_skill = skills.get_by_name(db, name=skill_data.name)
        if existing_skill:
            return SkillResponse.model_validate(existing_skill)
        
        # Create new skill
        new_skill = skills.create(db, name=skill_data.name)
        return SkillResponse.model_validate(new_skill)
        
    except Exception as e:
        # Handle database or other unexpected errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create skill: {str(e)}"
        )


@router.get("/statistics", response_model=SkillStatisticsResponse, summary="Get skill statistics")
async def get_skill_statistics(
    skill_id: str = Query(..., description="Skill ID (UUID) to get statistics for"),
    db: Session = Depends(get_db)
) -> SkillStatisticsResponse:
    """
    Get statistics for a specific skill including user count and level distribution.
    
    - **skill_id**: The UUID of the skill to get statistics for
    """
    skill = skills.get(db, skill_id=skill_id)
    if not skill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Skill with ID {skill_id} not found"
        )
    
    stats = user_skills.get_skill_statistics(db, skill_id=skill_id)
    
    return SkillStatisticsResponse(
        skill=SkillResponse.model_validate(skill),
        total_users=stats['total_users'],
        average_level=stats['average_level'],
        level_distribution=stats['level_distribution']
    )


@router.get("/popular", response_model=List[PopularSkillResponse], summary="Get most popular skills")
async def get_popular_skills(
    limit: int = Query(10, ge=1, le=50, description="Number of popular skills to return"),
    db: Session = Depends(get_db)
) -> List[PopularSkillResponse]:
    """
    Get the most popular skills based on the number of users who have them.
    
    - **limit**: Maximum number of popular skills to return
    """
    popular_skills_data = user_skills.get_top_skills_by_user_count(db, limit=limit)
    
    result = []
    for skill_id, skill_name, user_count in popular_skills_data:
        # Get the full skill object for created_at timestamp
        skill = skills.get(db, skill_id=str(skill_id))
        if skill:
            result.append(PopularSkillResponse(
                skill=SkillResponse.model_validate(skill),
                user_count=user_count
            ))
    
    return result


@router.delete("/delete", response_model=BaseResponse, summary="Delete a skill")
async def delete_skill(
    skill_id: str = Query(..., description="Skill ID (UUID) to delete"),
    db: Session = Depends(get_db)
) -> BaseResponse:
    """
    Delete a skill by its ID. This will also remove all associated user skills and job requirements.
    
    - **skill_id**: The UUID of the skill to delete
    """
    success = skills.delete(db, skill_id=skill_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Skill with ID {skill_id} not found"
        )
    
    return BaseResponse(
        success=True,
        message=f"Skill with ID {skill_id} has been successfully deleted"
    )
