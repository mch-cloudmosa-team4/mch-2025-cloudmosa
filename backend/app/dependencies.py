"""
Dependency injection functions for FastAPI
"""

from typing import Optional
from fastapi import Header, HTTPException, Query, Depends
from sqlalchemy.orm import Session
from app.config import settings
from app.database import get_db


async def get_api_key(x_api_key: Optional[str] = Header(None)) -> Optional[str]:
    """
    Extract and validate API key from header (for future authentication)
    
    Args:
        x_api_key: API key from header
        
    Returns:
        str: Valid API key
        
    Note:
        Currently returns the key without validation.
        Implement actual validation logic when needed.
    """
    # TODO: Add actual API key validation logic
    return x_api_key


async def get_current_user(api_key: Optional[str] = Depends(get_api_key)) -> Optional[dict]:
    """
    Get current user from API key (for future authentication)
    
    Args:
        api_key: Validated API key
        
    Returns:
        dict: User information
        
    Note:
        Currently returns a mock user.
        Implement actual user lookup logic when needed.
    """
    if api_key:
        # TODO: Implement actual user lookup from database
        return {"id": 1, "username": "user", "email": "user@example.com"}
    return None


def get_pagination_params(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(10, ge=1, le=100, description="Page size")
) -> dict:
    """
    Extract pagination parameters from query string
    
    Args:
        page: Page number (1-indexed)
        size: Number of items per page
        
    Returns:
        dict: Pagination parameters with skip and limit
    """
    skip = (page - 1) * size
    return {"page": page, "size": size, "skip": skip, "limit": size}


def validate_content_type(content_type: str = Header(...)) -> str:
    """
    Validate content type for certain endpoints
    
    Args:
        content_type: Content-Type header value
        
    Returns:
        str: Validated content type
        
    Raises:
        HTTPException: If content type is not supported
    """
    allowed_types = ["application/json", "application/x-www-form-urlencoded"]
    if content_type not in allowed_types:
        raise HTTPException(
            status_code=415,
            detail=f"Unsupported content type. Allowed: {', '.join(allowed_types)}"
        )
    return content_type


# Common dependencies for reuse
CommonDeps = {
    "current_user": Depends(get_current_user),
    "pagination": Depends(get_pagination_params),
}
