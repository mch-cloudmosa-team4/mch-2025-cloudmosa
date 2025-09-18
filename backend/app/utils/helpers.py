"""
Utility functions for the application
"""

import logging
import hashlib
import secrets
from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
from functools import wraps


def setup_logging(level: str = "INFO") -> logging.Logger:
    """
    Set up application logging
    
    Args:
        level: Logging level
        
    Returns:
        Logger: Configured logger instance
    """
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    logger = logging.getLogger("[Project name]-backend")
    return logger


def generate_id(length: int = 16) -> str:
    """
    Generate a secure random ID
    
    Args:
        length: Length of the ID
        
    Returns:
        str: Generated ID
    """
    return secrets.token_urlsafe(length)[:length]


def hash_string(text: str, salt: Optional[str] = None) -> str:
    """
    Hash a string with optional salt
    
    Args:
        text: Text to hash
        salt: Optional salt
        
    Returns:
        str: Hashed string
    """
    if salt:
        text = text + salt
    
    return hashlib.sha256(text.encode()).hexdigest()


def calculate_pagination(page: int, size: int, total: int) -> Dict[str, Any]:
    """
    Calculate pagination metadata
    
    Args:
        page: Current page number (1-indexed)
        size: Page size
        total: Total number of items
        
    Returns:
        dict: Pagination metadata
    """
    pages = (total + size - 1) // size  # Ceiling division
    has_next = page < pages
    has_prev = page > 1
    
    return {
        "page": page,
        "size": size,
        "total": total,
        "pages": pages,
        "has_next": has_next,
        "has_prev": has_prev
    }


def utc_now() -> datetime:
    """
    Get current UTC datetime
    
    Returns:
        datetime: Current UTC datetime
    """
    return datetime.now(timezone.utc)


def format_error_response(errors: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Format validation errors for API response
    
    Args:
        errors: List of error dictionaries
        
    Returns:
        dict: Formatted error response
    """
    formatted_errors = []
    
    for error in errors:
        formatted_errors.append({
            "field": error.get("loc", [])[-1] if error.get("loc") else None,
            "message": error.get("msg", "Unknown error"),
            "type": error.get("type", "unknown")
        })
    
    return {
        "success": False,
        "message": "Validation error",
        "errors": formatted_errors,
        "timestamp": utc_now().isoformat()
    }


def async_timer(func):
    """
    Decorator to measure execution time of async functions
    
    Args:
        func: Function to measure
        
    Returns:
        Decorated function
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = datetime.now()
        result = await func(*args, **kwargs)
        end_time = datetime.now()
        
        duration = (end_time - start_time).total_seconds()
        logger = logging.getLogger("[Project name]-backend")
        logger.info(f"{func.__name__} executed in {duration:.4f} seconds")
        
        return result
    
    return wrapper


# Initialize logger
logger = setup_logging()
