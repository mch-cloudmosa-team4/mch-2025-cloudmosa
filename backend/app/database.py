"""
Database configuration and connection management
"""

from typing import Generator
import logging
from sqlalchemy import create_engine, text
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
    echo=settings.database_echo
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


def ensure_extensions() -> None:
    """
    Ensure required PostgreSQL extensions are available.
    """
    try:
        with engine.connect() as connection:
            connection.execute(text('CREATE EXTENSION IF NOT EXISTS "citext"'))
            connection.execute(text('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"'))
            connection.execute(text('CREATE EXTENSION IF NOT EXISTS "vector"'))
            connection.commit()
    except Exception as exc:
        logging.getLogger("[Project name]-backend").warning(
            f"Failed to ensure PostgreSQL extensions: {exc}"
        )
