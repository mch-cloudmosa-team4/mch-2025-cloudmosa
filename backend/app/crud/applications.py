"""
CRUD operations for Application model
"""

from typing import List, Optional
from sqlalchemy.orm import Session

from app.models import Application, ApplicationStatus
from app.schemas import ApplicationCreate, ApplicationUpdate


class ApplicationCRUD:
    """
    CRUD operations for Application model
    """

    def get(self, db: Session, application_id: int) -> Optional[Application]:
        """
        Get application by ID

        Args:
            db: Database session
            application_id: Application ID

        Returns:
            Application or None if not found
        """
        return db.query(Application).filter(Application.id == application_id).first()

    def get_by_userid(
            self,
            db: Session,
            user_id: int,
            status: Optional[ApplicationStatus],
            skip: int = 0,
            limit: int = 100
        ) -> Optional[Application]:
        """
        Get application by ID

        Args:
            db: Database session
            user_id: User ID

        Returns:
            Application or None if not found
        """
        query = db.query(Application)

        if status:
            query.filter(Application.status == status)

        return query.offset(skip).limit(limit).filter(Application.applicant_user_id == user_id).all()

    def get_multi(
        self,
        db: Session,
        status: Optional[ApplicationStatus],
        skip: int = 0,
        limit: int = 100
    ) -> List[Application]:
        """
        Get multiple applications with pagination

        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return
            active_only: Whether to return only active applications

        Returns:
            List of applications
        """
        query = db.query(Application)

        if status:
            query = query.filter(Application.status == status)

        return query.offset(skip).limit(limit).all()


    def create(self, db: Session, obj_in: ApplicationCreate) -> Application:
        """
        Create new application

        Args:
            db: Database session
            obj_in: Application creation data

        Returns:
            Created application
        """
        db_obj = Application(**obj_in.model_dump())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        db_obj: Application,
        obj_in: ApplicationUpdate
    ) -> Application:
        """
        Update existing application

        Args:
            db: Database session
            db_obj: Existing application from database
            obj_in: Update data

        Returns:
            Updated application
        """
        update_data = obj_in.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(db_obj, field, value)

        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, application_id: int) -> Optional[Application]:
        """
        Delete application by ID

        Args:
            db: Database session
            application_id: Application ID

        Returns:
            Deleted application or None if not found
        """
        db_obj = self.get(db, application_id)
        if db_obj:
            db.delete(db_obj)
            db.commit()
        return db_obj

    def count(self, db: Session, active_only: bool = True) -> int:
        """
        Count total applications

        Args:
            db: Database session
            active_only: Whether to count only active applications

        Returns:
            Total count
        """
        query = db.query(Application)

        if active_only:
            query = query.filter(Application.is_active == True)

        return query.count()


# Create instance
applications = ApplicationCRUD()
