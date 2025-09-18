"""
Database configuration and connection management
"""

from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session

from app.config import settings


class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy models
    """
    pass


# Create sync engine for main application
engine = create_engine(
    settings.database_url,
    echo=settings.database_echo,
    connect_args={"check_same_thread": False} if "sqlite" in settings.database_url else {}
)

# Create session factory for sync operations
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False, 
    bind=engine
)


def get_db() -> Generator[Session, None, None]:
    """
    Get database session for sync operations
    
    Yields:
        Session: SQLAlchemy database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """
    Create all database tables
    """
    Base.metadata.create_all(bind=engine)


def drop_tables():
    """
    Drop all database tables
    """
    Base.metadata.drop_all(bind=engine)
