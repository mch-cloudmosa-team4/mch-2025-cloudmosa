"""
Location model for database storage - Geographic locations
"""

from datetime import datetime
import uuid
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Location(Base):
    """
    Location model for storing geographic locations
    """
    __tablename__ = "locations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    country = Column(String(255), nullable=False, index=True)
    country_code = Column(String(2), nullable=False, index=True)  # ISO 3166-1 alpha-2 code (optional)
    city = Column(String(255), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    profiles = relationship("Profile", back_populates="location")
    jobs = relationship("Job", back_populates="location")

    def __repr__(self):
        return f"<Location(id='{self.id}', country='{self.country}', city='{self.city}')>"