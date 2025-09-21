"""
CRUD operations for Job model
"""

from typing import List, Optional
from sqlalchemy.orm import Session

from app.models import JobRequirement


class JobRequirementCRUD:
    """
    CRUD operations for Job model
    """

    def get(self, db: Session, job_id: str) -> List[JobRequirement]:
        """
        Get job pictures by job ID

        Args:
            db: Database session
            job_id: Job ID

        Returns:
            JobRequirement or None if not found
        """
        return db.query(JobRequirement).filter(JobRequirement.job_id == job_id).all()

    def create(self, db: Session, job_id: str, skill_id: str, min_level: int = 1) -> JobRequirement:
        """
        Create new jobs

        Args:
            db: Database session
            job_id: Job ID
            skill_id: Skill ID

        Returns:
            Created JobRequirement
        """
        if min_level:
            db_obj = JobRequirement(job_id=job_id, skill_id=skill_id, min_level=min_level)
        else:
            db_obj = JobRequirement(job_id=job_id, skill_id=skill_id, min_level=min_level)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, job_id: str) -> Optional[JobRequirement]:
        """
        Delete jobs by ID

        Args:
            db: Database session
            jobs_id: Job ID
  
        Returns:
            Deleted jobs or None if not found
        """
        db_objs = db.query(JobRequirement).filter(JobRequirement.job_id == job_id).all()
        print(db_objs)
        if db_objs:
            for db_obj in db_objs:
                db.delete(db_obj)
            db.commit()
        return db_objs


# Create instance
job_requirements = JobRequirementCRUD()
