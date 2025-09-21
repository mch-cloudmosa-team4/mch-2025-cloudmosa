"""
CRUD operations for Job model
"""

from typing import List, Optional
from sqlalchemy.orm import Session

from app.models import Job, JobStatus
from app.schemas import JobCreate, JobUpdate
from app.utils import embed_encode


class JobCRUD:
    """
    CRUD operations for Job model
    """

    def get(self, db: Session, job_id: str) -> Optional[Job]:
        """
        Get job by ID

        Args:
            db: Database session
            job_id: Job ID

        Returns:
            Job or None if not found
        """
        return db.query(Job).filter(Job.id == job_id).first()

    def get_multi(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
        active_only: bool = True
    ) -> List[Job]:
        """
        Get multiple job with pagination

        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return
            active_only: Whether to return only active jobs

        Returns:
            List of jobs
        """
        query = db.query(Job)
        
        if active_only:
            query = query.filter(Job.status == JobStatus.PUBLISHED)

        return query.offset(skip).limit(limit).all()
    
    def search(
        self,
        db: Session,
        search_str: str,
        skip: int = 0,
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
            query = query.filter(Job.status == JobStatus.PUBLISHED)

        return (
            query
            .order_by(Job.embedding.cosine_distance(search_str_embed).asc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create(self, db: Session, obj_in: JobCreate) -> Job:
        """
        Create new job

        Args:
            db: Database session
            obj_in: Job creation data

        Returns:
            Created job
        """
        db_obj = Job(
            employer_id = obj_in.employer_id,
            title = obj_in.title,
            description = obj_in.description,
            location_id = obj_in.location_id,
            reward = obj_in.reward,
            address = obj_in.address,
            work_type = obj_in.work_type,
            required_people = obj_in.required_people,
            start_date = obj_in.start_date,
            end_date = obj_in.end_date,
            status = obj_in.status
        )
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
        Update existing job
        
        Args:
            db: Database session
            db_obj: Existing job from database
            obj_in: Update data

        Returns:
            Updated job
        """
        update_data = obj_in.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(db_obj, field, value)
 
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, job_id: str) -> Optional[Job]:
        """
        Delete job by ID

        Args:
            db: Database session
            job_id: Job ID
  
        Returns:
            Deleted job or None if not found
        """
        db_obj = self.get(db, job_id)
        if db_obj:
            db.delete(db_obj)
            db.commit()
        return db_obj

    def count(self, db: Session, active_only: bool = True) -> int:
        """
        Count total jobs

        Args:
            db: Database session
            active_only: Whether to count only active jobs

        Returns:
            Total count
        """
        query = db.query(Job)

        if active_only:
            query = query.filter(Job.is_active == True)

        return query.count()


# Create instance
jobs = JobCRUD()
