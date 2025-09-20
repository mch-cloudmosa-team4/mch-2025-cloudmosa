"""
CRUD operations for Job model
"""

from typing import List, Optional
from sqlalchemy.orm import Session

from app.models import JobPicture


class JobPictureCRUD:
    """
    CRUD operations for Job model
    """

    def get(self, db: Session, job_id: int) -> List[JobPicture]:
        """
        Get job pictures by job ID

        Args:
            db: Database session
            job_id: Job ID

        Returns:
            JobPicture or None if not found
        """
        return db.query(JobPicture).filter(JobPicture.job_id == job_id).all()

    def create(self, db: Session, job_id: int, picture_id: int) -> JobPicture:
        """
        Create new jobs

        Args:
            db: Database session
            job_id: Job ID
            picture_id: Picture ID

        Returns:
            Created JobPicture
        """
        db_obj = JobPicture(job_id=job_id, picture_id=picture_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, job_id: int) -> Optional[JobPicture]:
        """
        Delete jobs by ID

        Args:
            db: Database session
            jobs_id: Job ID
  
        Returns:
            Deleted jobs or None if not found
        """
        db_objs = db.query(JobPicture).filter(JobPicture.job_id == job_id).all()
        if db_objs:
            for db_obj in db_objs:
                db.delete(db_obj)
            db.commit()
        return db_objs


# Create instance
job_pictures = JobPictureCRUD()
