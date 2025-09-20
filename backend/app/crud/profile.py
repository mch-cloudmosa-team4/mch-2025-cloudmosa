"""
CRUD operations for Profile model
"""

from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_
import uuid

from app.models.profiles import Profile, Gender
from app.models.users import User
from app.schemas.profile import ProfileUpdateRequest


class ProfileCRUD:
    """
    CRUD operations for Profile model
    """
    
    def get(self, db: Session, user_id: str) -> Optional[Profile]:
        """
        Get profile by user ID
        
        Args:
            db: Database session
            user_id: User ID (UUID string)
            
        Returns:
            Profile or None if not found
        """
        try:
            user_uuid = uuid.UUID(user_id) if isinstance(user_id, str) else user_id
            return db.query(Profile).filter(Profile.user_id == user_uuid).first()
        except ValueError:
            return None
    
    def get_with_user(self, db: Session, user_id: str) -> Optional[Profile]:
        """
        Get profile with associated user data
        
        Args:
            db: Database session
            user_id: User ID (UUID string)
            
        Returns:
            Profile with loaded user relationship or None if not found
        """
        try:
            user_uuid = uuid.UUID(user_id) if isinstance(user_id, str) else user_id
            return db.query(Profile).options(joinedload(Profile.user)).filter(
                Profile.user_id == user_uuid
            ).first()
        except ValueError:
            return None
    
    def get_multi_by_user_ids(
        self, 
        db: Session, 
        user_ids: List[str]
    ) -> List[Profile]:
        """
        Get multiple profiles by user IDs
        
        Args:
            db: Database session
            user_ids: List of user IDs (UUID strings)
            
        Returns:
            List of profiles with user data
        """
        if not user_ids:
            return []
            
        try:
            user_uuids = [uuid.UUID(uid) for uid in user_ids]
            return db.query(Profile).options(joinedload(Profile.user)).filter(
                Profile.user_id.in_(user_uuids)
            ).all()
        except ValueError:
            return []
    
    def get_multi(
        self, 
        db: Session, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[Profile]:
        """
        Get multiple profiles with pagination
        
        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of profiles with user data
        """
        return db.query(Profile).options(joinedload(Profile.user)).offset(skip).limit(limit).all()
    
    def update(
        self, 
        db: Session, 
        profile: Profile, 
        update_data: ProfileUpdateRequest
    ) -> Profile:
        """
        Update profile
        
        Args:
            db: Database session
            profile: Existing profile instance
            update_data: Profile update data
            
        Returns:
            Updated profile
        """
        update_dict = update_data.model_dump(exclude_unset=True, exclude={'user_id'})
        
        # Handle gender conversion
        if 'gender' in update_dict:
            gender_value = update_dict['gender']
            if gender_value == 0:
                setattr(profile, 'gender', Gender.PREFER_NOT_TO_SAY)
            elif gender_value == 1:
                setattr(profile, 'gender', Gender.MALE)
            elif gender_value == 2:
                setattr(profile, 'gender', Gender.FEMALE)
            del update_dict['gender']
        
        # Update other fields
        for field, value in update_dict.items():
            if hasattr(profile, field) and value is not None:
                setattr(profile, field, value)
        
        # Also update user fields if provided
        if hasattr(update_data, 'phone') and update_data.phone:
            setattr(profile.user, 'phone', update_data.phone)
        if hasattr(update_data, 'email') and update_data.email is not None:
            setattr(profile.user, 'email', update_data.email)
        
        db.commit()
        db.refresh(profile)
        return profile
    
    def to_response_dict(self, profile: Profile) -> Dict[str, Any]:
        """
        Convert profile to response dictionary format
        
        Args:
            profile: Profile instance with loaded user relationship
            
        Returns:
            Dictionary suitable for API response
        """
        # Convert gender enum to int
        gender_int = 0  # Default NULL
        gender_value = getattr(profile, 'gender', None)
        if gender_value == Gender.MALE:
            gender_int = 1
        elif gender_value == Gender.FEMALE:
            gender_int = 2
        elif gender_value == Gender.PREFER_NOT_TO_SAY:
            gender_int = 0
            
        return {
            "user_id": str(profile.user_id),
            "phone": getattr(profile.user, 'phone', ''),
            "email": getattr(profile.user, 'email', None),
            "display_name": getattr(profile, 'display_name', ''),
            "avatar_file_id": getattr(profile, 'avatar_file_id', None),
            "birthday": getattr(profile, 'birthday', None),
            "gender": gender_int,
            "location_id": getattr(profile, 'location_id', None),
            "bio": getattr(profile, 'bio', None),
            "primary_language_code": getattr(profile, 'primary_language_code', ''),
            "created_at": getattr(profile, 'created_at', None),
            "updated_at": getattr(profile, 'updated_at', None)
        }
    
    def exists(self, db: Session, user_id: str) -> bool:
        """
        Check if profile exists for user
        
        Args:
            db: Database session
            user_id: User ID (UUID string)
            
        Returns:
            True if profile exists, False otherwise
        """
        try:
            user_uuid = uuid.UUID(user_id) if isinstance(user_id, str) else user_id
            return db.query(Profile).filter(Profile.user_id == user_uuid).first() is not None
        except ValueError:
            return False


# Create instance
profile = ProfileCRUD()