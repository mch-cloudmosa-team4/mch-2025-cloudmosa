"""
CRUD operations for File model
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.models import File
from app.schemas.files import FileCreate, FileUpdate


class FileCRUD:
    """
    CRUD operations for File model
    """
    
    def get(self, db: Session, file_id: str) -> Optional[File]:
        """
        Get file by ID
        
        Args:
            db: Database session
            file_id: File ID (UUID string)

        Returns:
            File or None if not found
        """
        return db.query(File).filter(File.id == file_id).first()
    
    def get_multi(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ) -> List[File]:
        """
        Get multiple files with pagination
        
        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return
            
            
        Returns:
            List of files
        """
        query = db.query(File)
        return query.offset(skip).limit(limit).all()
    
    def create(self, db: Session, obj_in: FileCreate) -> File:
        """
        Create new file record
        
        Args:
            db: Database session
            obj_in: File creation data
            
        Returns:
            Created file
        """
        db_obj = File(**obj_in.model_dump())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def update(
        self, 
        db: Session,
        db_obj: File,
        obj_in: FileUpdate
    ) -> File:
        """
        Update existing file
        
        Args:
            db: Database session
            db_obj: Existing file from database
            obj_in: Update data
            
        Returns:
            Updated file
        """
        update_data = obj_in.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(db_obj, field, value)
            
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def delete(self, db: Session, file_id: str) -> Optional[File]:
        """
        Delete file by ID
        
        Args:
            db: Database session
            file_id: File ID (UUID string)
            
        Returns:
            Deleted file or None if not found
        """
        db_obj = self.get(db, file_id)
        if db_obj:
            db.delete(db_obj)
            db.commit()
        return db_obj

    def count(self, db: Session) -> int:
        """
        Count total files
        """
        query = db.query(File)
        return query.count()


# Create instance
file = FileCRUD()
