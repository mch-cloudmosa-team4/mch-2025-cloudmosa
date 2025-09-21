"""
Profile API router
"""

from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends, status, Query
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.users import User
from app.crud.profile import profile
from app.schemas.profile import (
    ProfileResponse,
    ProfileUpdateRequest,
    ProfileListResponse,
    ProfileUpdateResponse
)

bearer_scheme = HTTPBearer()


router = APIRouter(
    prefix="/profile",
    tags=["profile"],
    responses={
        401: {"description": "Unauthorized"},
        404: {"description": "Not found"},
        422: {"description": "Validation error"}
    }
)


@router.get("", response_model=List[ProfileResponse], summary="Get user profiles")
async def get_profiles(
    user_ids: List[str] = Query(description="List of user IDs to get profiles for"),
    db: Session = Depends(get_db)
) -> List[ProfileResponse]:
    """
    Get user profiles by user IDs
    
    Args:
        user_ids: List of user IDs
        db: Database session
        
    Returns:
        List[ProfileResponse]: User profiles
        
    Raises:
        HTTPException: If validation fails
    """
    if not user_ids:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one user_id must be provided"
        )
    
    # Get profiles with user data
    profiles = profile.get_multi_by_user_ids(db, user_ids)
    
    # Convert to response format
    response_data = []
    for p in profiles:
        response_data.append(ProfileResponse(**profile.to_response_dict(p)))
    
    return response_data


@router.get("/all", response_model=ProfileListResponse, summary="List all profiles")
async def list_all_profiles(
    db: Session = Depends(get_db)
) -> ProfileListResponse:
    """
    List all user profiles with pagination
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        db: Database session
        
    Returns:
        ProfileListResponse: Paginated list of user profiles
    """
    profiles = profile.get_all(db)
    
    # Convert to response format
    profile_list = [ProfileResponse(**profile.to_response_dict(p)) for p in profiles]
    
    return ProfileListResponse(
        profiles=profile_list,
    )


@router.get("/me", response_model=ProfileResponse, summary="Get my profile", dependencies=[Depends(bearer_scheme)])
async def get_my_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> ProfileResponse:
    """
    Get current user's profile
    
    Args:
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        ProfileResponse: Current user's profile
        
    Raises:
        HTTPException: If user not authorized or profile not found
    """
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    
    # Get current profile
    current_profile = profile.get(db, str(current_user.id))
    if not current_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    
    # Convert to response format
    profile_data = profile.to_response_dict(current_profile)
    
    return ProfileResponse(**profile_data)


@router.put("/me", response_model=ProfileUpdateResponse, summary="Update my profile", dependencies=[Depends(bearer_scheme)])
async def update_my_profile(
    update_request: ProfileUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> ProfileUpdateResponse:
    """
    Update current user's profile
    
    Args:
        update_request: Profile update data
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        ProfileUpdateResponse: Updated profile data
        
    Raises:
        HTTPException: If user not authorized or profile not found
    """
    # Get current profile
    current_profile = profile.get(db, str(current_user.id))
    if not current_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    
    # Update profile
    updated_profile = profile.update(db, current_profile, update_request)
    
    # Convert to response format
    profile_data = profile.to_response_dict(updated_profile)
    
    return ProfileUpdateResponse(
        success=True,
        message="Profile updated successfully",
        profile=ProfileResponse(**profile_data)
    )