"""
Location API router
"""

from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends, status, Query
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user, get_api_key
from app.models.users import User
from app.crud.locations import location
from app.schemas.locations import (
    LocationResponse,
    LocationCreateRequest,
    LocationUpdateRequest,
    LocationSearchRequest,
    LocationListResponse,
    CountryResponse,
    CountryListResponse,
    CityListResponse,
    LocationStatsResponse
)

bearer_scheme = HTTPBearer()

router = APIRouter(
    prefix="/locations",
    tags=["locations"],
    responses={
        401: {"description": "Unauthorized"},
        404: {"description": "Not found"},
        422: {"description": "Validation error"}
    }
)


@router.get("", response_model=LocationListResponse, summary="Get all locations")
async def get_locations(
    skip: int = Query(0, description="Number of records to skip", ge=0),
    limit: int = Query(100, description="Maximum number of records to return", ge=1, le=1000),
    db: Session = Depends(get_db)
) -> LocationListResponse:
    """
    Get all locations with pagination
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        db: Database session
        
    Returns:
        LocationListResponse: List of locations with total count
    """
    locations = location.get_multi(db, skip=skip, limit=limit)
    total = location.get_location_count(db)
    
    return LocationListResponse(
        locations=[LocationResponse.model_validate(loc) for loc in locations],
        total=total
    )


@router.get("/search", response_model=LocationListResponse, summary="Search locations")
async def search_locations(
    q: str = Query(description="Search term for country or city", min_length=1),
    skip: int = Query(0, description="Number of records to skip", ge=0),
    limit: int = Query(50, description="Maximum number of records to return", ge=1, le=100),
    db: Session = Depends(get_db)
) -> LocationListResponse:
    """
    Search locations by country or city name
    
    Args:
        q: Search term
        skip: Number of records to skip
        limit: Maximum number of records to return
        db: Database session
        
    Returns:
        LocationListResponse: List of matching locations
    """
    locations = location.search_locations(db, q, skip=skip, limit=limit)
    total = len(locations)  # For search results, we return the actual count
    
    return LocationListResponse(
        locations=[LocationResponse.model_validate(loc) for loc in locations],
        total=total
    )


@router.get("/countries", response_model=CountryListResponse, summary="Get all countries")
async def get_countries(
    db: Session = Depends(get_db)
) -> CountryListResponse:
    """
    Get all unique countries
    
    Args:
        db: Database session
        
    Returns:
        CountryListResponse: List of countries with country codes
    """
    countries = location.get_all_countries(db)
    
    return CountryListResponse(
        countries=[CountryResponse(**country) for country in countries]
    )


@router.get("/countries/{country}/cities", response_model=CityListResponse, summary="Get cities in a country")
async def get_cities_by_country(
    country: str,
    db: Session = Depends(get_db)
) -> CityListResponse:
    """
    Get all cities in a specific country
    
    Args:
        country: Country name
        db: Database session
        
    Returns:
        CityListResponse: List of cities in the country
    """
    cities = location.get_cities_by_country(db, country)
    
    return CityListResponse(
        cities=cities,
        country=country
    )


@router.get("/popular", response_model=LocationListResponse, summary="Get popular locations")
async def get_popular_locations(
    limit: int = Query(20, description="Maximum number of locations to return", ge=1, le=100),
    db: Session = Depends(get_db)
) -> LocationListResponse:
    """
    Get popular locations (currently returns locations ordered alphabetically)
    
    Args:
        limit: Maximum number of locations to return
        db: Database session
        
    Returns:
        LocationListResponse: List of popular locations
    """
    # For now, return locations ordered alphabetically as "popular"
    popular_locations = location.get_multi(db, skip=0, limit=limit)
    
    return LocationListResponse(
        locations=[LocationResponse.model_validate(loc) for loc in popular_locations],
        total=len(popular_locations)
    )


@router.get("/stats", response_model=LocationStatsResponse, summary="Get location statistics")
async def get_location_stats(
    db: Session = Depends(get_db)
) -> LocationStatsResponse:
    """
    Get location statistics
    
    Args:
        db: Database session
        
    Returns:
        LocationStatsResponse: Location statistics
    """
    total_locations = location.get_location_count(db)
    total_countries = location.get_country_count(db)
    
    return LocationStatsResponse(
        total_locations=total_locations,
        total_countries=total_countries
    )


@router.get("/{location_id}", response_model=LocationResponse, summary="Get location by ID")
async def get_location(
    location_id: str,
    db: Session = Depends(get_db)
) -> LocationResponse:
    """
    Get location by ID
    
    Args:
        location_id: Location ID
        db: Database session
        
    Returns:
        LocationResponse: Location details
        
    Raises:
        HTTPException: If location not found
    """
    loc = location.get(db, location_id)
    if not loc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Location not found"
        )
    
    return LocationResponse.model_validate(loc)


@router.post("", response_model=LocationResponse, summary="Create new location")
async def create_location(
    location_data: LocationCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> LocationResponse:
    """
    Create a new location
    
    Args:
        location_data: Location creation data
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        LocationResponse: Created location details
        
    Raises:
        HTTPException: If creation fails or location already exists
    """
    # Check if location already exists
    existing = location.get_by_country_and_city(
        db, location_data.country, location_data.city
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Location already exists"
        )
    
    # Create new location
    new_location = location.create(
        db,
        country=location_data.country,
        country_code=location_data.country_code,
        city=location_data.city
    )
    
    if not new_location:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create location"
        )
    
    return LocationResponse.model_validate(new_location)


@router.put("/{location_id}", response_model=LocationResponse, summary="Update location")
async def update_location(
    location_id: str,
    location_data: LocationUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> LocationResponse:
    """
    Update location details
    
    Args:
        location_id: Location ID
        location_data: Location update data
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        LocationResponse: Updated location details
        
    Raises:
        HTTPException: If location not found or update fails
    """
    # Check if location exists
    existing = location.get(db, location_id)
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Location not found"
        )
    
    # Prepare update data
    update_data = location_data.model_dump(exclude_unset=True)
    
    # Update location
    updated_location = location.update(db, location_id, **update_data)
    
    if not updated_location:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update location"
        )
    
    return LocationResponse.model_validate(updated_location)


@router.delete("/{location_id}", summary="Delete location")
async def delete_location(
    location_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> dict:
    """
    Delete location
    
    Args:
        location_id: Location ID
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        dict: Success message
        
    Raises:
        HTTPException: If location not found or deletion fails
    """
    # Check if location exists
    existing = location.get(db, location_id)
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Location not found"
        )
    
    # Delete location
    success = location.delete(db, location_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete location"
        )
    
    return {"message": "Location deleted successfully"}


@router.post("/bulk", response_model=List[LocationResponse], summary="Bulk create locations")
async def bulk_create_locations(
    locations_data: List[LocationCreateRequest],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> List[LocationResponse]:
    """
    Bulk create multiple locations
    
    Args:
        locations_data: List of location creation data
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        List[LocationResponse]: List of created/existing locations
    """
    if not locations_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one location must be provided"
        )
    
    if len(locations_data) > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Maximum 100 locations can be created at once"
        )
    
    # Prepare location data
    location_dicts = [
        {
            "country": loc.country,
            "country_code": loc.country_code,
            "city": loc.city
        }
        for loc in locations_data
    ]
    
    # Bulk create locations
    created_locations = location.bulk_create(db, location_dicts)
    
    return [LocationResponse.model_validate(loc) for loc in created_locations]
