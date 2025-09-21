"""
CRUD operations for Profile model
"""

from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_
import uuid
from datetime import datetime, timezone

from app.models.profiles import Profile, Gender
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
        
    def get_all(self, db: Session) -> List[Profile]:
        """
        Get all profiles
        
        Args:
            db: Database session
            
        Returns:
            List of all profiles
        """
        return db.query(Profile).all()
    
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
    
    def create(
        self,
        db: Session,
        user_id: str,
        display_name: str,
        gender: Gender = Gender.OTHER,
        primary_language_code: str = "en",
        avatar_file_id: Optional[str] = None,
        birthday: Optional[datetime] = None,
        location_id: Optional[str] = None,
        bio: Optional[str] = None
    ) -> Profile:
        profile = Profile(
            user_id=user_id,
            display_name=display_name,
            avatar_file_id=avatar_file_id,
            birthday=birthday,
            gender=gender,
            location_id=location_id,
            bio=bio,
            primary_language_code=primary_language_code,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )

        db.add(profile)
        db.commit()
        db.refresh(profile)
        return profile

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
        
        # Update other fields
        for field, value in update_dict.items():
            if hasattr(profile, field) and value is not None:
                if field == "gender":
                    value = Gender(value)
                setattr(profile, field, value)
        
        # Also update user fields if provided
        if hasattr(update_data, 'email') and update_data.email is not None:
            setattr(profile.user, 'email', update_data.email)
        
        db.commit()
        db.refresh(profile)
        return profile
    
    def delete(self, db: Session, user_id: str) -> bool:
        """
        Delete profile by user ID
        
        Args:
            db: Database session
            user_id: User ID (UUID string)
            
        Returns:
            True if deleted, False if not found
        """
        profile = self.get(db, user_id)
        if not profile:
            return False
        
        db.delete(profile)
        db.commit()
        return True
    
    def to_response_dict(self, profile: Profile) -> Dict[str, Any]:
        """
        Convert profile to response dictionary format
        
        Args:
            profile: Profile instance with loaded user relationship
            
        Returns:
            Dictionary suitable for API response
        """ 
        return {
            "user_id": str(profile.user_id),
            "phone": getattr(profile.user, 'phone', ''),
            "email": getattr(profile.user, 'email', None),
            "display_name": getattr(profile, 'display_name', ''),
            "avatar_file_id": getattr(profile, 'avatar_file_id', None),
            "birthday": getattr(profile, 'birthday', None),
            "gender": getattr(profile, 'gender', None),
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