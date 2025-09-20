"""
CRUD operations for Skill model
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
import uuid
from datetime import datetime, timezone

from app.models.skills import Skill
from app.models.user_skills import UserSkill


class SkillCRUD:
    """
    CRUD operations for Skill model
    """
    
    def get(self, db: Session, skill_id: str) -> Optional[Skill]:
        """
        Get skill by ID
        
        Args:
            db: Database session
            skill_id: Skill ID (UUID string)
            
        Returns:
            Skill or None if not found
        """
        try:
            skill_uuid = uuid.UUID(skill_id) if isinstance(skill_id, str) else skill_id
            return db.query(Skill).filter(Skill.id == skill_uuid).first()
        except ValueError:
            return None
    
    def get_by_name(self, db: Session, name: str) -> Optional[Skill]:
        """
        Get skill by name (case-insensitive)
        
        Args:
            db: Database session
            name: Skill name
            
        Returns:
            Skill or None if not found
        """
        return db.query(Skill).filter(Skill.name == name.strip()).first()
    
    def get_multi(
        self, 
        db: Session, 
        skill_ids: Optional[List[str]] = None,
        skip: int = 0, 
        limit: int = 100
    ) -> List[Skill]:
        """
        Get multiple skills
        
        Args:
            db: Database session
            skill_ids: Optional list of skill IDs to filter by
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of skills
        """
        query = db.query(Skill)
        
        if skill_ids:
            try:
                skill_uuids = [uuid.UUID(sid) for sid in skill_ids]
                query = query.filter(Skill.id.in_(skill_uuids))
            except ValueError:
                return []
                
        return query.offset(skip).limit(limit).all()

    def search_by_name(
        self, 
        db: Session, 
        name_pattern: str, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[Skill]:
        """
        Search skills by name pattern (case-insensitive)
        
        Args:
            db: Database session
            name_pattern: Pattern to search for in skill names
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of matching skills
        """
        pattern = f"%{name_pattern.strip().lower()}%"
        return (
            db.query(Skill)
            .filter(Skill.name.ilike(pattern))
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def create(
        self, 
        db: Session, 
        name: str
    ) -> Skill:
        """
        Create a new skill
        
        Args:
            db: Database session
            name: Skill name
            
        Returns:
            Newly created skill
        """
        new_skill = Skill(
            id=uuid.uuid4(),
            name=name.strip(),
            created_at=datetime.now(timezone.utc)
        )
        
        db.add(new_skill)
        db.commit()
        db.refresh(new_skill)
        
        return new_skill
    
    def update(self, db: Session, skill_id: str, **kwargs) -> Optional[Skill]:
        """
        Update skill details
        
        Args:
            db: Database session
            skill_id: Skill ID
            kwargs: Fields to update (e.g., name)
            
        Returns:
            Updated skill or None if not found
        """
        skill = self.get(db, skill_id)
        if not skill:
            return None
        
        for key, value in kwargs.items():
            if hasattr(skill, key) and value is not None:
                if key == 'name':
                    value = value.strip()
                setattr(skill, key, value)
        
        db.commit()
        db.refresh(skill)
        return skill
    
    def delete(self, db: Session, skill_id: str) -> bool:
        """
        Permanently delete skill
        Note: This will also delete associated UserSkill and JobRequirement records
        due to CASCADE delete
        
        Args:
            db: Database session
            skill_id: Skill ID
            
        Returns:
            True if deleted, False if not found
        """
        skill = self.get(db, skill_id)
        if skill:
            db.delete(skill)
            db.commit()
            return True
        return False

    def count(self, db: Session) -> int:
        """
        Count total skills
        
        Args:
            db: Database session
            
        Returns:
            Total count
        """
        return db.query(Skill).count()


# Create instance
skills = SkillCRUD()
