"""
CRUD operations for User model
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
import uuid
from datetime import datetime, timezone

from app.models.users import User, UserRole
from app.models.profiles import Profile, Gender
from app.utils.auth import get_password_hash, verify_password


class UserCRUD:
    """
    CRUD operations for User model
    """
    
    def get(self, db: Session, user_id: str) -> Optional[User]:
        """
        Get user by ID
        
        Args:
            db: Database session
            user_id: User ID (UUID string)
            
        Returns:
            User or None if not found
        """
        try:
            user_uuid = uuid.UUID(user_id) if isinstance(user_id, str) else user_id
            return db.query(User).filter(User.id == user_uuid).first()
        except ValueError:
            return None
    
    def get_by_phone(self, db: Session, phone: str) -> Optional[User]:
        """
        Get user by phone number
        
        Args:
            db: Database session
            phone: Phone number
            
        Returns:
            User or None if not found
        """
        return db.query(User).filter(User.phone == phone).first()
    
    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        """
        Get user by email
        
        Args:
            db: Database session
            email: Email address
            
        Returns:
            User or None if not found
        """
        return db.query(User).filter(User.email == email).first()
    
    def get_multi(
        self, 
        db: Session, 
        user_ids: Optional[List[str]] = None,
        skip: int = 0, 
        limit: int = 100
    ) -> List[User]:
        """
        Get multiple users
        
        Args:
            db: Database session
            user_ids: Optional list of user IDs to filter by
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of users
        """
        query = db.query(User)
        
        if user_ids:
            try:
                user_uuids = [uuid.UUID(uid) for uid in user_ids]
                query = query.filter(User.id.in_(user_uuids))
            except ValueError:
                return []
                
        return query.offset(skip).limit(limit).all()

    def create(
        self, 
        db: Session, 
        phone: str,
        passwd_hash: str,
        email: Optional[str] = None,
        role: UserRole = UserRole.USER,
        is_active: bool = True
    ) -> User:
        """
        Create new user
        
        Args:
            db: Database session
            phone: Phone number
            passwd_hash: Hashed password
            email: Optional email
            role: User role
            is_active: Active status
            
        Returns:
            Created user
        """
        user = User(
            phone=phone,
            passwd_hash=passwd_hash,
            email=email,
            role=role,
            is_active=is_active
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)
        
        return user
    
    def update(self, db: Session, user_id: str, **kwargs) -> Optional[User]:
        """
        Update user details
        
        Args:
            db: Database session
            user_id: User ID
            kwargs: Fields to update
            
        Returns:
            Updated user or None if not found
        """
        user = self.get(db, user_id)
        if not user:
            return None
        
        for key, value in kwargs.items():
            if hasattr(user, key) and value is not None:
                setattr(user, key, value)
        
        db.commit()
        db.refresh(user)
        return user
    
    def update_last_login(self, db: Session, user: User) -> User:
        """
        Update user's last login timestamp
        
        Args:
            db: Database session
            user: User instance
            
        Returns:
            Updated user
        """
        setattr(user, 'last_login_at', datetime.now(timezone.utc))
        db.commit()
        db.refresh(user)
        return user
    
    def deactivate(self, db: Session, user_id: str) -> Optional[User]:
        """
        Deactivate user (soft delete)
        
        Args:
            db: Database session
            user_id: User ID
            
        Returns:
            Deactivated user or None if not found
        """
        user = self.get(db, user_id)
        if user:
            setattr(user, 'is_active', False)
            db.commit()
            db.refresh(user)
        return user
    
    def delete(self, db: Session, user_id: str) -> bool:
        """
        Permanently delete user
        
        Args:
            db: Database session
            user_id: User ID
            
        Returns:
            True if deleted, False if not found
        """
        user = self.get(db, user_id)
        if user:
            db.delete(user)
            db.commit()
            return True
        return False
    
    def exists_by_phone(self, db: Session, phone: str) -> bool:
        """
        Check if user exists by phone number
        
        Args:
            db: Database session
            phone: Phone number
            
        Returns:
            True if user exists, False otherwise
        """
        return db.query(User).filter(User.phone == phone).first() is not None


# Create instance
user = UserCRUD()