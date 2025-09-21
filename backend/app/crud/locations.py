"""
CRUD operations for Location model
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
import uuid

from app.models.locations import Location


class LocationCRUD:
    """
    CRUD operations for Location model
    """
    
    def get(self, db: Session, location_id: str) -> Optional[Location]:
        """
        Get location by ID
        
        Args:
            db: Database session
            location_id: Location ID (UUID string)
            
        Returns:
            Location or None if not found
        """
        try:
            location_uuid = uuid.UUID(location_id) if isinstance(location_id, str) else location_id
            return db.query(Location).filter(Location.id == location_uuid).first()
        except ValueError:
            return None
    
    def get_by_country_and_city(
        self, 
        db: Session, 
        country: str, 
        city: str
    ) -> Optional[Location]:
        """
        Get location by country and city
        
        Args:
            db: Database session
            country: Country name
            city: City name
            
        Returns:
            Location or None if not found
        """
        return db.query(Location).filter(
            and_(
                func.lower(Location.country) == country.lower(),
                func.lower(Location.city) == city.lower()
            )
        ).first()
    
    def get_by_country_code_and_city(
        self, 
        db: Session, 
        country_code: str, 
        city: str
    ) -> Optional[Location]:
        """
        Get location by country code and city
        
        Args:
            db: Database session
            country_code: Country code (ISO 3166-1 alpha-2)
            city: City name
            
        Returns:
            Location or None if not found
        """
        return db.query(Location).filter(
            and_(
                func.lower(Location.country_code) == country_code.lower(),
                func.lower(Location.city) == city.lower()
            )
        ).first()
    
    def get_by_country(
        self, 
        db: Session, 
        country: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[Location]:
        """
        Get all locations in a country
        
        Args:
            db: Database session
            country: Country name
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of locations in the country
        """
        return db.query(Location)\
            .filter(func.lower(Location.country) == country.lower())\
            .order_by(Location.city)\
            .offset(skip).limit(limit).all()
    
    def get_by_country_code(
        self, 
        db: Session, 
        country_code: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[Location]:
        """
        Get all locations in a country by country code
        
        Args:
            db: Database session
            country_code: Country code (ISO 3166-1 alpha-2)
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of locations in the country
        """
        return db.query(Location)\
            .filter(func.lower(Location.country_code) == country_code.lower())\
            .order_by(Location.city)\
            .offset(skip).limit(limit).all()
    
    def get_cities_by_country(
        self, 
        db: Session, 
        country: str
    ) -> List[str]:
        """
        Get all city names in a country
        
        Args:
            db: Database session
            country: Country name
            
        Returns:
            List of city names
        """
        result = db.query(Location.city)\
            .filter(func.lower(Location.country) == country.lower())\
            .order_by(Location.city)\
            .all()
        return [city[0] for city in result]
    
    def get_all_countries(self, db: Session) -> List[dict]:
        """
        Get all unique countries
        
        Args:
            db: Database session
            
        Returns:
            List of dictionaries with country and country_code
        """
        result = db.query(Location.country, Location.country_code)\
            .distinct()\
            .order_by(Location.country)\
            .all()
        return [{"country": country, "country_code": code} for country, code in result]
    
    def get_multi(
        self, 
        db: Session, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[Location]:
        """
        Get multiple locations
        
        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of locations
        """
        return db.query(Location)\
            .order_by(Location.country, Location.city)\
            .offset(skip).limit(limit).all()
    
    def create(
        self, 
        db: Session, 
        country: str,
        country_code: str,
        city: str
    ) -> Optional[Location]:
        """
        Create new location
        
        Args:
            db: Database session
            country: Country name
            country_code: Country code (ISO 3166-1 alpha-2)
            city: City name
            
        Returns:
            Created location or None if failed
        """
        try:
            # Check if location already exists
            existing = self.get_by_country_and_city(db, country, city)
            if existing:
                return existing
            
            location = Location(
                country=country.strip(),
                country_code=country_code.upper().strip(),
                city=city.strip()
            )
            
            db.add(location)
            db.commit()
            db.refresh(location)
            
            return location
        except Exception:
            db.rollback()
            return None
    
    def get_or_create(
        self, 
        db: Session, 
        country: str,
        country_code: str,
        city: str
    ) -> Optional[Location]:
        """
        Get existing location or create new one
        
        Args:
            db: Database session
            country: Country name
            country_code: Country code (ISO 3166-1 alpha-2)
            city: City name
            
        Returns:
            Location (existing or newly created) or None if failed
        """
        # First try to find existing location
        location = self.get_by_country_and_city(db, country, city)
        if location:
            return location
        
        # Create new location if not found
        return self.create(db, country, country_code, city)
    
    def update(
        self, 
        db: Session, 
        location_id: str, 
        **kwargs
    ) -> Optional[Location]:
        """
        Update location details
        
        Args:
            db: Database session
            location_id: Location ID
            kwargs: Fields to update
            
        Returns:
            Updated location or None if not found
        """
        location = self.get(db, location_id)
        if not location:
            return None
        
        for key, value in kwargs.items():
            if hasattr(location, key) and value is not None:
                if key == "country_code":
                    setattr(location, key, value.upper().strip())
                else:
                    setattr(location, key, value.strip() if isinstance(value, str) else value)
        
        db.commit()
        db.refresh(location)
        return location
    
    def delete(self, db: Session, location_id: str) -> bool:
        """
        Delete location
        
        Args:
            db: Database session
            location_id: Location ID
            
        Returns:
            True if deleted, False if not found
        """
        location = self.get(db, location_id)
        if location:
            db.delete(location)
            db.commit()
            return True
        return False
    
    def search_locations(
        self, 
        db: Session, 
        search_term: str,
        skip: int = 0,
        limit: int = 50
    ) -> List[Location]:
        """
        Search locations by country or city name
        
        Args:
            db: Database session
            search_term: Search term
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of matching locations
        """
        search_pattern = f"%{search_term.lower()}%"
        return db.query(Location)\
            .filter(
                or_(
                    func.lower(Location.country).contains(search_pattern),
                    func.lower(Location.city).contains(search_pattern)
                )
            )\
            .order_by(Location.country, Location.city)\
            .offset(skip).limit(limit).all()
    
    def get_location_count(self, db: Session) -> int:
        """
        Get total number of locations
        
        Args:
            db: Database session
            
        Returns:
            Total location count
        """
        return db.query(Location).count()
    
    def get_country_count(self, db: Session) -> int:
        """
        Get total number of unique countries
        
        Args:
            db: Database session
            
        Returns:
            Total country count
        """
        return db.query(Location.country).distinct().count()
    
    def exists(
        self, 
        db: Session, 
        country: str, 
        city: str
    ) -> bool:
        """
        Check if location exists
        
        Args:
            db: Database session
            country: Country name
            city: City name
            
        Returns:
            True if location exists, False otherwise
        """
        return self.get_by_country_and_city(db, country, city) is not None
    
    def bulk_create(
        self, 
        db: Session, 
        locations: List[dict]
    ) -> List[Location]:
        """
        Bulk create locations
        
        Args:
            db: Database session
            locations: List of location dictionaries with keys: country, country_code, city
            
        Returns:
            List of created locations
        """
        created_locations = []
        
        for location_data in locations:
            country = location_data.get('country')
            country_code = location_data.get('country_code')
            city = location_data.get('city')
            
            if country and country_code and city:
                location = self.get_or_create(db, country, country_code, city)
                if location:
                    created_locations.append(location)
        
        return created_locations


# Create instance
location = LocationCRUD()
