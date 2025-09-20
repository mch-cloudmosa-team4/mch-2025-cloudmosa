"""
Authentication utilities - JWT tokens, password hashing, etc.
"""

from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
import uuid
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.config import settings
from app.utils import logger
from app.models import User


# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT settings
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1
REFRESH_TOKEN_EXPIRE_DAYS = 30


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain text password against a hashed password
    
    Args:
        plain_password: Plain text password
        hashed_password: Hashed password from database
        
    Returns:
        True if password matches, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hash a plain text password
    
    Args:
        password: Plain text password
        
    Returns:
        Hashed password
    """
    return pwd_context.hash(password)


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token
    
    Args:
        data: Data to encode in the token
        expires_delta: Optional custom expiration time
        
    Returns:
        JWT access token string
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT refresh token
    
    Args:
        data: Data to encode in the token
        expires_delta: Optional custom expiration time
        
    Returns:
        JWT refresh token string
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str, token_type: str = "access") -> Optional[Dict[str, Any]]:
    """
    Verify and decode a JWT token
    
    Args:
        token: JWT token string
        token_type: Expected token type ("access" or "refresh")
        
    Returns:
        Decoded token payload or None if invalid
        
    Raises:
        JWTError: If token is expired (with "token expired" message)
    """
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[ALGORITHM])

        # Check token type
        if payload.get("type") != token_type:
            return None
        
        # Check expiration
        if datetime.now() > datetime.fromtimestamp(payload.get("exp", 0)):
            logger.warning(f"Token expired: {token}")
            raise JWTError("Token expired")

        return payload
    except JWTError as e:
        # Re-raise JWT errors to distinguish between expired and other errors
        raise e


def get_user_id_from_token(token: str) -> Optional[str]:
    """
    Extract user ID from JWT token
    
    Args:
        token: JWT token string
        
    Returns:
        User ID string or None if invalid token
        
    Raises:
        JWTError: If token is expired (with "token expired" message)
    """
    try:
        payload = verify_token(token, token_type="access")
        if not payload:
            return None
        
        user_id = payload.get("sub")
        if not user_id:
            return None
            
        # Validate UUID format
        try:
            uuid.UUID(user_id)
            return user_id
        except ValueError:
            return None
    except JWTError as e:
        # Re-raise JWT errors (including token expired)
        raise e


def create_verification_code() -> str:
    """
    Create a 6-digit verification code
    
    Returns:
        6-digit string
    """
    import random
    return f"{random.randint(0, 999999):06d}"


def is_token_expired(token: str) -> bool:
    """
    Check if a token is expired without validating signature
    
    Args:
        token: JWT token string
        
    Returns:
        True if expired, False if still valid
    """
    try:
        # Decode without verification to check expiration
        payload = jwt.decode(token, key="", options={"verify_signature": False})
        exp_timestamp = payload.get("exp", 0)
        return datetime.now(timezone.utc) > datetime.fromtimestamp(exp_timestamp)
    except JWTError:
        return True


# In-memory storage for refresh tokens (in production, use Redis or database)
_refresh_tokens: Dict[str, Dict[str, Any]] = {}


def create_tokens(user: User) -> Dict[str, str]:
    """
    Create access and refresh tokens for user
    
    Args:
        user: Authenticated user (User model instance)
        
    Returns:
        Dictionary with access_token and refresh_token
    """
    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})
    
    # Store refresh token
    _refresh_tokens[refresh_token] = {
        "user_id": str(user.id),
        "created_at": datetime.now(timezone.utc),
        "expires_at": datetime.now(timezone.utc) + timedelta(days=30)  # 30-day expiry
    }
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }


def refresh_access_token(refresh_token: str) -> Optional[str]:
    """
    Create new access token from refresh token
    
    Args:
        refresh_token: Valid refresh token
        
    Returns:
        New access token or None if refresh token invalid/expired
    """
    token_data = _refresh_tokens.get(refresh_token)
    if not token_data:
        return None
        
    # Check if expired
    if datetime.now(timezone.utc) > token_data["expires_at"]:
        del _refresh_tokens[refresh_token]
        return None
    
    # Create new access token
    access_token = create_access_token(data={"sub": token_data["user_id"]})
    return access_token


def revoke_refresh_token(refresh_token: str) -> bool:
    """
    Revoke a refresh token (logout)
    
    Args:
        refresh_token: Refresh token to revoke
        
    Returns:
        True if token was revoked, False if not found
    """
    if refresh_token in _refresh_tokens:
        del _refresh_tokens[refresh_token]
        return True
    return False


def cleanup_expired_tokens():
    """
    Clean up expired refresh tokens
    """
    current_time = datetime.now(timezone.utc)
    expired_tokens = []
    
    for token, data in _refresh_tokens.items():
        if current_time > data["expires_at"]:
            expired_tokens.append(token)
    
    for token in expired_tokens:
        del _refresh_tokens[token]