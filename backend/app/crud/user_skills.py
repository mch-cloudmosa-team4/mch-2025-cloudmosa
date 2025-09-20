"""
CRUD operations for UserSkill model
"""

from typing import List, Optional, Dict, Tuple, Any, Sequence
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_, func, desc, asc
import uuid
from datetime import datetime, timezone

from app.models.user_skills import UserSkill
from app.models.users import User
from app.models.skills import Skill


class UserSkillCRUD:
    """
    CRUD operations for UserSkill model (Association table between users and skills)
    """
    
    def get(
        self, 
        db: Session, 
        user_id: str, 
        skill_id: str
    ) -> Optional[UserSkill]:
        """
        Get user skill by composite key (user_id, skill_id)
        
        Args:
            db: Database session
            user_id: User ID (UUID string)
            skill_id: Skill ID (UUID string)
            
        Returns:
            UserSkill or None if not found
        """
        try:
            user_uuid = uuid.UUID(user_id) if isinstance(user_id, str) else user_id
            skill_uuid = uuid.UUID(skill_id) if isinstance(skill_id, str) else skill_id
            
            return db.query(UserSkill).filter(
                and_(
                    UserSkill.user_id == user_uuid,
                    UserSkill.skill_id == skill_uuid
                )
            ).first()
        except ValueError:
            return None
    
    def get_by_user(
        self, 
        db: Session, 
        user_id: str,
        include_skill_details: bool = False
    ) -> List[UserSkill]:
        """
        Get all skills for a specific user
        
        Args:
            db: Database session
            user_id: User ID (UUID string)
            include_skill_details: Whether to include skill details in query
            
        Returns:
            List of UserSkill records
        """
        try:
            print("Getting user skills for user_id:", user_id)
            user_uuid = uuid.UUID(user_id) if isinstance(user_id, str) else user_id
            print("User UUID:", user_uuid)
            query = db.query(UserSkill).filter(UserSkill.user_id == user_uuid)
            print("User skills count:", query.count())

            if include_skill_details:
                query = query.options(joinedload(UserSkill.skill))
            
            return query.order_by(UserSkill.created_at).all()
        except ValueError:
            print(f"Invalid UUID format for user_id: {user_id}")
            return []
    
    def get_by_skill(
        self, 
        db: Session, 
        skill_id: str,
        min_level: Optional[int] = None,
        include_user_details: bool = False,
        skip: int = 0,
        limit: int = 100
    ) -> List[UserSkill]:
        """
        Get all users who have a specific skill
        
        Args:
            db: Database session
            skill_id: Skill ID (UUID string)
            min_level: Minimum skill level required
            include_user_details: Whether to include user details in query
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of UserSkill records
        """
        try:
            skill_uuid = uuid.UUID(skill_id) if isinstance(skill_id, str) else skill_id
            query = db.query(UserSkill).filter(UserSkill.skill_id == skill_uuid)
            
            if min_level is not None and 1 <= min_level <= 5:
                query = query.filter(UserSkill.level >= min_level)
            
            if include_user_details:
                query = query.options(joinedload(UserSkill.user))
            
            return query.order_by(desc(UserSkill.level)).offset(skip).limit(limit).all()
        except ValueError:
            return []

    def get_multi(
        self, 
        db: Session,
        user_ids: Optional[List[str]] = None,
        skill_ids: Optional[List[str]] = None,
        min_level: Optional[int] = None,
        max_level: Optional[int] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[UserSkill]:
        """
        Get multiple user skills with optional filters
        
        Args:
            db: Database session
            user_ids: Optional list of user IDs to filter by
            skill_ids: Optional list of skill IDs to filter by
            min_level: Minimum skill level
            max_level: Maximum skill level
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of UserSkill records
        """
        query = db.query(UserSkill)
        
        try:
            if user_ids:
                user_uuids = [uuid.UUID(uid) for uid in user_ids]
                query = query.filter(UserSkill.user_id.in_(user_uuids))
            
            if skill_ids:
                skill_uuids = [uuid.UUID(sid) for sid in skill_ids]
                query = query.filter(UserSkill.skill_id.in_(skill_uuids))
            
            if min_level is not None and 1 <= min_level <= 5:
                query = query.filter(UserSkill.level >= min_level)
            
            if max_level is not None and 1 <= max_level <= 5:
                query = query.filter(UserSkill.level <= max_level)
            
            return query.offset(skip).limit(limit).all()
        except ValueError:
            return []

    def create(
        self, 
        db: Session, 
        user_id: str, 
        skill_id: str, 
        level: int
    ) -> Optional[UserSkill]:
        """
        Create new user skill association
        
        Args:
            db: Database session
            user_id: User ID (UUID string)
            skill_id: Skill ID (UUID string)
            level: Proficiency level (1-5)
            
        Returns:
            Created UserSkill or None if invalid input
        """
        try:
            user_uuid = uuid.UUID(user_id) if isinstance(user_id, str) else user_id
            skill_uuid = uuid.UUID(skill_id) if isinstance(skill_id, str) else skill_id
            
            if not (1 <= level <= 5):
                return None
            
            # Check if association already exists
            existing = self.get(db, user_id, skill_id)
            if existing:
                return None  # Don't create duplicate
            
            user_skill = UserSkill(
                user_id=user_uuid,
                skill_id=skill_uuid,
                level=level
            )
            
            db.add(user_skill)
            db.commit()
            db.refresh(user_skill)
            
            return user_skill
        except ValueError:
            return None

    def update(
        self, 
        db: Session, 
        user_id: str, 
        skill_id: str, 
        level: int
    ) -> Optional[UserSkill]:
        """
        Update skill level for existing user skill
        
        Args:
            db: Database session
            user_id: User ID (UUID string)
            skill_id: Skill ID (UUID string)
            level: New proficiency level (1-5)
            
        Returns:
            Updated UserSkill or None if not found or invalid level
        """
        if not (1 <= level <= 5):
            return None
        
        user_skill = self.get(db, user_id, skill_id)
        if not user_skill:
            return None
        
        setattr(user_skill, 'level', level)
        db.commit()
        db.refresh(user_skill)
        return user_skill

    def delete(
        self, 
        db: Session, 
        user_id: str, 
        skill_id: str
    ) -> bool:
        """
        Delete user skill association
        
        Args:
            db: Database session
            user_id: User ID (UUID string)
            skill_id: Skill ID (UUID string)
            
        Returns:
            True if deleted, False if not found
        """
        user_skill = self.get(db, user_id, skill_id)
        if user_skill:
            db.delete(user_skill)
            db.commit()
            return True
        return False

    def delete_all_user_skills(
        self, 
        db: Session, 
        user_id: str
    ) -> int:
        """
        Delete all skills for a specific user
        
        Args:
            db: Database session
            user_id: User ID (UUID string)
            
        Returns:
            Number of deleted records
        """
        try:
            user_uuid = uuid.UUID(user_id) if isinstance(user_id, str) else user_id
            deleted_count = db.query(UserSkill).filter(
                UserSkill.user_id == user_uuid
            ).delete()
            db.commit()
            return deleted_count
        except ValueError:
            return 0

    # Statistics and Query Methods
    
    def get_skill_statistics(
        self, 
        db: Session, 
        skill_id: str
    ) -> Dict[str, Any]:
        """
        Get statistics for a specific skill
        
        Args:
            db: Database session
            skill_id: Skill ID (UUID string)
            
        Returns:
            Dictionary with skill statistics
        """
        try:
            skill_uuid = uuid.UUID(skill_id) if isinstance(skill_id, str) else skill_id
            
            # Get total users with this skill
            total_users = db.query(UserSkill).filter(
                UserSkill.skill_id == skill_uuid
            ).count()
            
            # Get level distribution
            level_stats = db.query(
                UserSkill.level, 
                func.count(UserSkill.level).label('count')
            ).filter(
                UserSkill.skill_id == skill_uuid
            ).group_by(UserSkill.level).all()
            
            # Calculate average level
            avg_level = db.query(
                func.avg(UserSkill.level)
            ).filter(
                UserSkill.skill_id == skill_uuid
            ).scalar() or 0
            
            level_distribution = {level: count for level, count in level_stats}
            
            return {
                'total_users': total_users,
                'average_level': round(float(avg_level), 2),
                'level_distribution': level_distribution
            }
        except ValueError:
            return {'total_users': 0, 'average_level': 0, 'level_distribution': {}}

    def get_user_skill_count(
        self, 
        db: Session, 
        user_id: str
    ) -> int:
        """
        Get total number of skills for a user
        
        Args:
            db: Database session
            user_id: User ID (UUID string)
            
        Returns:
            Number of skills user has
        """
        try:
            user_uuid = uuid.UUID(user_id) if isinstance(user_id, str) else user_id
            return db.query(UserSkill).filter(
                UserSkill.user_id == user_uuid
            ).count()
        except ValueError:
            return 0

    def get_top_skills_by_user_count(
        self, 
        db: Session, 
        limit: int = 10
    ) -> List[Any]:
        """
        Get most popular skills by user count
        
        Args:
            db: Database session
            limit: Number of top skills to return
            
        Returns:
            List of tuples (skill_id, skill_name, user_count)
        """
        return (
            db.query(
                UserSkill.skill_id,
                Skill.name,
                func.count(UserSkill.user_id).label('user_count')
            )
            .join(Skill, UserSkill.skill_id == Skill.id)
            .group_by(UserSkill.skill_id, Skill.name)
            .order_by(desc(func.count(UserSkill.user_id)))
            .limit(limit)
            .all()
        )

    def exists(
        self, 
        db: Session, 
        user_id: str, 
        skill_id: str
    ) -> bool:
        """
        Check if user skill association exists
        
        Args:
            db: Database session
            user_id: User ID (UUID string)
            skill_id: Skill ID (UUID string)
            
        Returns:
            True if association exists, False otherwise
        """
        return self.get(db, user_id, skill_id) is not None

    def count_by_level(
        self, 
        db: Session, 
        level: int
    ) -> int:
        """
        Count user skills by specific level
        
        Args:
            db: Database session
            level: Skill level (1-5)
            
        Returns:
            Count of user skills at that level
        """
        if not (1 <= level <= 5):
            return 0
        
        return db.query(UserSkill).filter(UserSkill.level == level).count()


# Create instance
user_skills = UserSkillCRUD()
