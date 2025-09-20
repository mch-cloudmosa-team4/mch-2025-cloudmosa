"""
CRUD operations for Job model
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.models import Job
from app.schemas import JobCreate, JobUpdate
from app.utils import embed_encode


class JobCRUD:
    """
    CRUD operations for Job model
    """

    def get(self, db: Session, jobs_id: int) -> Optional[Job]:
        """
        Get jobs by ID

        Args:
            db: Database session
            jobs_id: Job ID

        Returns:
            Job or None if not found
        """
        return db.query(Job).filter(Job.id == jobs_id).first()

    def get_multi(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
        active_only: bool = True
    ) -> List[Job]:
        """
        Get multiple jobss with pagination

        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return
            active_only: Whether to return only active jobss

        Returns:
            List of jobss
        """
        query = db.query(Job)
        
        if active_only:
            query = query.filter(Job.is_active == True)

        return query.offset(skip).limit(limit).all()
    
    def search(
        self,
        db: Session,
        search_str: str,
        limit: int = 100,
        active_only: bool = True
    ) -> List[Job]:
        """
        Search jobs with input search string

        Args:
            db: Database session
            search_str: search string

        Returns:
            Matched jobs
        """
        search_str_embed = embed_encode(search_str)
        query = db.query(Job)
        
        if active_only:
            query = query.filter(Job.is_active == True)

        return (
            query
            .order_by(Job.embedding.cosine_distance(search_str_embed))
            .limit(limit)
            .all()
        )

    def create(self, db: Session, obj_in: JobCreate) -> Job:
        """
        Create new jobs

        Args:
            db: Database session
            obj_in: Job creation data

        Returns:
            Created jobs
        """
        db_obj = Job(**obj_in.model_dump())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, 
        db: Session, 
        db_obj: Job, 
        obj_in: JobUpdate
    ) -> Job:
        """
        Update existing jobs
        
        Args:
            db: Database session
            db_obj: Existing jobs from database
            obj_in: Update data

        Returns:
            Updated jobs
        """
        update_data = obj_in.model_dump(exclude_unset=True)

        for field, value in update_data.jobss():
            setattr(db_obj, field, value)
 
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, jobs_id: int) -> Optional[Job]:
        """
        Delete jobs by ID

        Args:
            db: Database session
            jobs_id: Job ID
  
        Returns:
            Deleted jobs or None if not found
        """
        db_obj = self.get(db, jobs_id)
        if db_obj:
            db.delete(db_obj)
            db.commit()
        return db_obj

    def count(self, db: Session, active_only: bool = True) -> int:
        """
        Count total jobss

        Args:
            db: Database session
            active_only: Whether to count only active jobss

        Returns:
            Total count
        """
        query = db.query(Job)

        if active_only:
            query = query.filter(Job.is_active == True)

        return query.count()


# Create instance
jobs = JobCRUD()
