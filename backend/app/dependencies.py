"""
Dependency injection functions for FastAPI
"""

from typing import Optional
from fastapi import Header, HTTPException, Query, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models.users import User
from app.crud.user import user
from app.utils.auth import get_user_id_from_token

# HTTP Bearer security scheme
security = HTTPBearer(auto_error=False)


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


async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """
    Get current user from JWT token
    
    Args:
        credentials: HTTP Bearer credentials
        db: Database session
        
    Returns:
        User: Current authenticated user
        
    Raises:
        HTTPException: If token is invalid or user not found
    """
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Extract user ID from token
    try:
        user_id = get_user_id_from_token(credentials.credentials)
        
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except Exception as e:
        # Check if it's a token expired error
        if "expired" in str(e).lower():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
    
    # Get user from database
    current_user = user.get(db, user_id)
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check if user is active
    if not getattr(current_user, 'is_active', True):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account is deactivated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return current_user


async def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """
    Get current user from JWT token (optional - doesn't raise exception if not provided)
    
    Args:
        credentials: HTTP Bearer credentials
        db: Database session
        
    Returns:
        User or None if not authenticated
    """
    if not credentials:
        return None
    
    try:
        user_id = get_user_id_from_token(credentials.credentials)
        if not user_id:
            return None
        
        current_user = user.get(db, user_id)
        if not current_user or not getattr(current_user, 'is_active', True):
            return None
            
        return current_user
    except Exception:
        # For optional authentication, return None on any error (including token expired)
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
    "current_user_optional": Depends(get_current_user_optional),
    "pagination": Depends(get_pagination_params),
}
