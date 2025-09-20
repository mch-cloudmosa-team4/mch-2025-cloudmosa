"""
User Skills API router with database integration
"""

from typing import List
from fastapi import APIRouter, HTTPException, Query, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.crud import user_skills, skills
from app.models.users import User
from app.models import BaseResponse
from app.schemas.user_skills import (
    UserSkillsResponse,
    MultipleUserSkillsResponse,
    UserSkillsRequest,
    UserSkillSummary
)


router = APIRouter(
    prefix="/user_skills",
    tags=["user_skills"],
    responses={
        401: {"description": "Unauthorized"},
        404: {"description": "Not found"},
        422: {"description": "Validation error"}
    }
)


@router.get("/", response_model=MultipleUserSkillsResponse, summary="Get skills for specific users")
async def get_users_skills(
    user_ids: List[str] = Query(..., description="List of user IDs (UUIDs) to get skills for"),
    db: Session = Depends(get_db)
) -> MultipleUserSkillsResponse:
    """
    Get skills for one or more specific users.
    
    - **user_ids**: List of UUIDs of the users to get skills for
    
    Returns skills grouped by user. Users without skills will still be included with empty skills array.
    """
    if not user_ids:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one user_id is required"
        )
    
    result_users = []
    
    for user_id in user_ids:
        try:
            # Get user skills with skill details
            user_skill_list = user_skills.get_by_user(
                db, 
                user_id=user_id, 
                include_skill_details=True
            )
            print(user_id)
            print(user_skill_list)
            
            # Convert to response format
            skills_summary = []
            for user_skill in user_skill_list:
                if user_skill.skill:  # Ensure skill details are loaded
                    skills_summary.append(UserSkillSummary(
                        id=user_skill.skill.id,  # Use skill.id instead of skill_id
                        name=user_skill.skill.name,
                        level=getattr(user_skill, "level")
                    ))
            
            result_users.append(UserSkillsResponse(
                user_id=user_id,  # Keep as string, will be converted by Pydantic
                skills=skills_summary
            ))
            
        except ValueError:
            # Invalid UUID format - skip this user
            continue
    
    return MultipleUserSkillsResponse(users=result_users)


@router.get("/me", response_model=UserSkillsResponse, summary="Get my skills")
async def get_my_skills(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> UserSkillsResponse:
    """
    Get skills for the currently authenticated user.
    
    Requires valid JWT token in Authorization header.
    """
    # Get user skills with skill details
    user_skill_list = user_skills.get_by_user(
        db, 
        user_id=str(current_user.id), 
        include_skill_details=True
    )
    
    # Convert to response format
    skills_summary = []
    for user_skill in user_skill_list:
        if user_skill.skill:  # Ensure skill details are loaded
            skills_summary.append(UserSkillSummary(
                id=user_skill.skill.id,  # Use skill.id instead of skill_id
                name=user_skill.skill.name,
                level=getattr(user_skill, "level")
            ))
    
    return UserSkillsResponse(
        user_id=str(current_user.id),  # Convert to string
        skills=skills_summary
    )


@router.post("/me", response_model=UserSkillsResponse, summary="Add skills to my profile")
async def add_my_skill(
    skills_data: UserSkillsRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> UserSkillsResponse:
    """
    Add skills to the currently authenticated user's profile.
    
    - **skills**: Array of skills with skill IDs and proficiency levels (1-5)
    
    Only new skills will be added. If a skill already exists in the user's profile,
    it will be skipped and reported in the response.
    
    Requires valid JWT token in Authorization header.
    """
    user_id = str(current_user.id)
    
    try:
        # Get current user skills to check for conflicts
        current_user_skills = user_skills.get_by_user(db, user_id=user_id)
        current_skill_ids = {str(us.skill_id) for us in current_user_skills}
        
        skills_added = []
        skills_skipped = []
        skills_not_found = []
        
        # Process each skill in the request
        for skill_data in skills_data.skills:
            skill_id_str = str(skill_data.skill_id)
            
            # Validate that skill exists in database
            skill = skills.get(db, skill_id=skill_id_str)
            if not skill:
                skills_not_found.append(skill_id_str)
                continue
            
            # Check if user already has this skill
            if skill_id_str in current_skill_ids:
                skills_skipped.append({
                    "skill_id": skill_id_str,
                    "name": skill.name,
                    "reason": "Already exists in profile"
                })
                continue
            
            # Create new user skill
            new_skill = user_skills.create(
                db,
                user_id=user_id,
                skill_id=skill_id_str,
                level=skill_data.level
            )
            
            if new_skill:
                skills_added.append({
                    "skill_id": skill_id_str,
                    "name": skill.name,
                    "level": skill_data.level
                })
                current_skill_ids.add(skill_id_str)  # Update our tracking set
        
        # Handle errors
        if skills_not_found:
            print("Some skills were not found in the database.")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Skills not found: {', '.join(skills_not_found)}"
            )
        
        if not skills_added and skills_skipped:
            # All skills were skipped
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="All specified skills already exist in your profile"
            )
        
        # Get updated skills with details for response
        updated_user_skills = user_skills.get_by_user(
            db,
            user_id=user_id,
            include_skill_details=True
        )
        
        # Convert to response format - return only the newly added skills
        skills_summary = []
        for added_skill in skills_added:
            # Find the corresponding user skill with details
            for user_skill in updated_user_skills:
                if str(user_skill.skill_id) == added_skill["skill_id"] and user_skill.skill:
                    skills_summary.append(UserSkillSummary(
                        id=user_skill.skill.id,
                        name=user_skill.skill.name,
                        level=getattr(user_skill, "level")
                    ))
                    break
        
        return UserSkillsResponse(
            user_id=str(current_user.id),
            skills=skills_summary
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Handle other unexpected errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to add skills: {str(e)}"
        )


@router.put("/me", response_model=UserSkillsResponse, summary="Update my skills")
async def update_my_skills(
    skills_data: UserSkillsRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> UserSkillsResponse:
    """
    Update skills for the currently authenticated user.
    
    This intelligently updates user skills by:
    - Adding new skills that don't exist
    - Updating existing skills if level has changed  
    - Removing skills that are no longer in the list
    
    This approach is more efficient than deleting all and re-creating,
    and preserves creation timestamps for unchanged skills.
    
    - **skills**: Array of skills with skill IDs and proficiency levels (1-5)
    
    Requires valid JWT token in Authorization header.
    """
    user_id = str(current_user.id)
    
    try:
        # Validate that all skill IDs exist
        for skill_data in skills_data.skills:
            skill = skills.get(db, skill_id=str(skill_data.skill_id))
            if not skill:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Skill with ID {skill_data.skill_id} not found"
                )
        
        # Get current user skills
        current_user_skills = user_skills.get_by_user(db, user_id=user_id)
        current_skill_map = {str(us.skill_id): getattr(us, 'level', 0) for us in current_user_skills}
        
        # Create maps for easier comparison
        new_skill_map = {str(skill_data.skill_id): skill_data.level for skill_data in skills_data.skills}
        
        # Find skills to add, update, and remove
        skills_to_add = []
        skills_to_update = []
        skills_to_remove = []
        
        # Check what needs to be added or updated
        for skill_id_str, new_level in new_skill_map.items():
            if skill_id_str in current_skill_map:
                # Skill exists, check if level needs update
                current_level = current_skill_map[skill_id_str]
                if current_level != new_level:
                    skills_to_update.append((skill_id_str, new_level))
            else:
                # New skill to add
                skills_to_add.append((skill_id_str, new_level))
        
        # Check what needs to be removed
        for skill_id_str in current_skill_map:
            if skill_id_str not in new_skill_map:
                skills_to_remove.append(skill_id_str)
        
        # Perform updates
        for skill_id_str, new_level in skills_to_update:
            user_skills.update(db, user_id=user_id, skill_id=skill_id_str, level=new_level)
        
        # Add new skills
        for skill_id_str, level in skills_to_add:
            user_skills.create(db, user_id=user_id, skill_id=skill_id_str, level=level)
        
        # Remove skills that are no longer needed
        for skill_id_str in skills_to_remove:
            user_skills.delete(db, user_id=user_id, skill_id=skill_id_str)
        
        # Get updated skills with details for response
        updated_user_skills = user_skills.get_by_user(
            db,
            user_id=user_id,
            include_skill_details=True
        )
        
        # Convert to response format
        skills_summary = []
        for user_skill in updated_user_skills:
            if user_skill.skill:  # Ensure skill details are loaded
                skills_summary.append(UserSkillSummary(
                    id=user_skill.skill.id,  # Use skill.id instead of skill_id
                    name=user_skill.skill.name,
                    level=getattr(user_skill, "level")
                ))
        
        return UserSkillsResponse(
            user_id=str(current_user.id),  # Convert to string
            skills=skills_summary
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Handle other unexpected errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update user skills: {str(e)}"
        )
    

@router.patch("/me", response_model=UserSkillsResponse, summary="Partially update my skills")
async def partially_update_my_skills(
    skills_data: UserSkillsRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> UserSkillsResponse:
    """
    Partially update skills for the currently authenticated user.
    
    This ONLY updates existing skills that the user already has.
    It will NOT add new skills or remove existing ones.
    If a skill in the request doesn't exist in user's profile, it will be ignored.
    
    RESPONSE: Returns only the skills that were actually updated, not all user skills.
    
    - **skills**: Array of skills with skill IDs and proficiency levels (1-5)
    
    Requires valid JWT token in Authorization header.
    """
    user_id = str(current_user.id)
    
    try:
        # Validate that all skill IDs exist in database
        for skill_data in skills_data.skills:
            skill = skills.get(db, skill_id=str(skill_data.skill_id))
            if not skill:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Skill with ID {skill_data.skill_id} not found"
                )
        
        # Get current user skills
        current_user_skills = user_skills.get_by_user(db, user_id=user_id)
        current_skill_map = {str(us.skill_id): getattr(us, 'level', 0) for us in current_user_skills}
        
        # Create map for easier comparison
        new_skill_map = {str(skill_data.skill_id): skill_data.level for skill_data in skills_data.skills}
        
        # Find skills to update (ONLY existing skills)
        skills_to_update = []
        skills_ignored = []
        
        for skill_id_str, new_level in new_skill_map.items():
            if skill_id_str in current_skill_map:
                # Skill exists in user's profile, check if level needs update
                current_level = current_skill_map[skill_id_str]
                if current_level != new_level:
                    skills_to_update.append((skill_id_str, new_level))
            else:
                # Skill doesn't exist in user's profile - ignore it
                skills_ignored.append(skill_id_str)
        
        # Perform ONLY updates (no additions, no deletions)
        updated_skills = []
        for skill_id_str, new_level in skills_to_update:
            updated_skill = user_skills.update(db, user_id=user_id, skill_id=skill_id_str, level=new_level)
            if updated_skill:
                updated_skills.append(updated_skill)
        
        # Get skill details for the updated skills only
        skills_summary = []
        for updated_skill in updated_skills:
            # Get skill details
            skill = skills.get(db, skill_id=str(updated_skill.skill_id))
            if skill:
                skills_summary.append(UserSkillSummary(
                    id=getattr(skill, "id"),
                    name=getattr(skill, "name"),
                    level=getattr(updated_skill, "level")
                ))
        
        return UserSkillsResponse(
            user_id=str(current_user.id),
            skills=skills_summary
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Handle other unexpected errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to partially update user skills: {str(e)}"
        )


@router.delete("/me", response_model=UserSkillsResponse, summary="Remove skills from my profile")
async def remove_my_skill(
    skills_data: UserSkillsRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> UserSkillsResponse:
    """
    Remove one or more skills from the currently authenticated user's profile.
    
    - **skills**: Array of skills with skill IDs to remove (level field is ignored)
    
    Only existing skills will be removed. If a skill doesn't exist in the user's profile,
    it will be skipped and reported in the response.
    
    Returns the skills that were successfully removed.
    
    Requires valid JWT token in Authorization header.
    """
    user_id = str(current_user.id)
    
    try:
        # Get current user skills to check what exists
        current_user_skills = user_skills.get_by_user(db, user_id=user_id)
        current_skill_map = {str(us.skill_id): us for us in current_user_skills}
        
        skills_removed = []
        skills_not_found = []
        
        # Process each skill in the request
        for skill_data in skills_data.skills:
            skill_id_str = str(skill_data.skill_id)
            
            # Check if user has this skill
            if skill_id_str not in current_skill_map:
                skills_not_found.append(skill_id_str)
                continue
            
            # Delete the skill
            success = user_skills.delete(db, user_id=user_id, skill_id=skill_id_str)
            if success:
                # Get skill details for the response
                user_skill = current_skill_map[skill_id_str]
                skill = skills.get(db, skill_id=skill_id_str)
                if skill:
                    skills_removed.append({
                        "skill_id": skill_id_str,
                        "name": skill.name,
                        "level": getattr(user_skill, "level", 0)
                    })
        
        # Handle case where no skills were found in user's profile
        if not skills_removed and skills_not_found:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="None of the specified skills exist in your profile"
            )
        
        # Convert to response format - return the removed skills
        skills_summary = []
        for removed_skill in skills_removed:
            skills_summary.append(UserSkillSummary(
                id=removed_skill["skill_id"],  # Use skill_id as id
                name=removed_skill["name"],
                level=removed_skill["level"]
            ))
        
        return UserSkillsResponse(
            user_id=str(current_user.id),
            skills=skills_summary
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Handle other unexpected errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to remove skills: {str(e)}"
        )


@router.get("/stats/me", response_model=dict, summary="Get my skills statistics")
async def get_my_skills_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> dict:
    """
    Get skills statistics for the currently authenticated user.
    
    Returns statistics like total skills count, skill level distribution, and average level.
    
    Requires valid JWT token in Authorization header.
    """
    user_id = str(current_user.id)
    
    # Get user skills
    user_skill_list = user_skills.get_by_user(db, user_id=user_id)
    
    if not user_skill_list:
        return {
            "total_skills": 0,
            "skill_levels": {},
            "average_level": 0.0
        }
    
    # Calculate statistics
    total_skills = len(user_skill_list)
    levels = [getattr(us, 'level', 0) for us in user_skill_list]
    
    # Level distribution
    level_distribution = {}
    for level in range(1, 6):  # Levels 1-5
        count = levels.count(level)
        if count > 0:
            level_distribution[level] = count
    
    # Average level
    average_level = sum(levels) / len(levels) if levels else 0.0
    
    return {
        "total_skills": total_skills,
        "skill_levels": level_distribution,
        "average_level": round(average_level, 2)
    }


@router.get("/search/{skill_id}", response_model=MultipleUserSkillsResponse, summary="Get users who have a specific skill")
async def get_users_by_skill(
    skill_id: str,
    min_level: int = Query(1, ge=1, le=5, description="Minimum skill level required"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=500, description="Maximum number of records to return"),
    db: Session = Depends(get_db)
) -> MultipleUserSkillsResponse:
    """
    Search users who have a specific skill.
    
    - **skill_id**: UUID of the skill to search for
    - **min_level**: Minimum proficiency level required (1-5)
    - **skip**: Number of records to skip for pagination
    - **limit**: Maximum number of records to return
    
    Returns users who have the specified skill, ordered by skill level (highest first).
    """
    try:
        # Validate skill exists
        skill = skills.get(db, skill_id=skill_id)
        if not skill:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Skill with ID {skill_id} not found"
            )
        
        # Get users who have this skill
        user_skills_list = user_skills.get_by_skill(
            db,
            skill_id=skill_id,
            min_level=min_level,
            include_user_details=True,
            skip=skip,
            limit=limit
        )
        
        # Group by user and convert to response format
        user_skill_map = {}
        for user_skill in user_skills_list:
            if user_skill.user:  # Ensure user details are loaded
                user_id_str = str(user_skill.user_id)
                if user_id_str not in user_skill_map:
                    user_skill_map[user_id_str] = {
                        'user_id': user_id_str,
                        'skills': []
                    }
                
                user_skill_map[user_id_str]['skills'].append(UserSkillSummary(
                    id=getattr(skill, "id"),
                    name=getattr(skill, "name"),
                    level=getattr(user_skill, "level")
                ))
        
        # Convert to response format
        result_users = [
            UserSkillsResponse(
                user_id=user_data['user_id'],
                skills=user_data['skills']
            )
            for user_data in user_skill_map.values()
        ]
        
        return MultipleUserSkillsResponse(users=result_users)
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except ValueError:
        # Invalid UUID format
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid skill ID format"
        )
    except Exception as e:
        # Handle other unexpected errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get users by skill: {str(e)}"
        )
