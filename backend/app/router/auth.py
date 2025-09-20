"""
Simplified authentication router (no OTP)
"""

from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from jose.exceptions import JWTError

from app.database import get_db
from app.dependencies import get_current_user
from app.schemas.auth import LoginRequest, RegisterRequest, PhoneLoginRequest, TokenResponse, UserInfo, RefreshTokenRequest, LogoutRequest
from app.models.base import BaseResponse
from app.models.users import User
from app.models.profiles import Profile, Gender
from app.crud.user import user
from app.crud.profile import profile
from app.utils.auth import create_tokens, refresh_access_token, revoke_refresh_token, verify_password, get_password_hash

router = APIRouter(
    prefix="/auth", 
    tags=["Authentication"]
)
bearer_scheme = HTTPBearer(
    description="Access token authentication"
)


@router.post("/login", response_model=TokenResponse)
async def login(
    request: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    Login with phone number and password.
    
    Phone format: +2348012345678
    
    Returns access token and user information.
    """
    # Check if user exists
    existing_user = user.get_by_phone(db, request.phone)
    
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid phone number or password"
        )

    # Verify password
    if request.passwd_hash != str(existing_user.passwd_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid phone number or password"
        )

    # Get user profile
    profile = db.query(Profile).filter(Profile.user_id == existing_user.id).first()
    
    # Update last login time
    user.update_last_login(db, existing_user)
    
    # Create tokens
    tokens = create_tokens(existing_user)
    
    return TokenResponse(
        access_token=tokens["access_token"],
        refresh_token=tokens["refresh_token"],
        token_type="bearer",
        user=UserInfo(
            user_id=str(existing_user.id),
            phone=str(existing_user.phone),
            email=getattr(existing_user, 'email', None),
            display_name=str(profile.display_name) if profile else f"User {request.phone[-4:]}",
            is_active=getattr(existing_user, 'is_active', True),
            created_at=getattr(existing_user, 'created_at', None) or datetime.now(timezone.utc),
            last_login_at=getattr(existing_user, 'last_login_at', None)
        )
    )


@router.post("/register", response_model=TokenResponse)
async def register(
    request: RegisterRequest,
    db: Session = Depends(get_db)
):
    """
    Register a new user with basic information.
    
    Phone format: +2348012345678
    
    Returns access token and user information.
    """
    # Check if user already exists
    if user.get_by_phone(db, request.phone):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this phone number already exists"
        )
    
    # Create new user
    new_user = user.create(
        db=db,
        phone=request.phone,
        passwd_hash=request.passwd_hash,
        email=request.email,
    )
    
    # Create profile
    try:
        user_profile = profile.create(
            db=db,
            user_id=str(new_user.id),
            display_name=request.display_name,
            birthday=request.birthday,
            gender=Gender(request.gender),
            location_id=request.location_id,
            primary_language_code=request.primary_language_code,
        )
    except Exception as e:
        # Rollback user creation if profile fails
        user.delete(db, str(new_user.id))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user profile"
        ) from e

    # Create tokens
    tokens = create_tokens(new_user)
    
    return TokenResponse(
        access_token=tokens["access_token"],
        refresh_token=tokens["refresh_token"],
        token_type="bearer",
        user=UserInfo(
            user_id=str(new_user.id),
            phone=str(new_user.phone),
            email=getattr(new_user, 'email', None),
            display_name=str(getattr(user_profile, 'display_name', f"User {request.phone[-4:]}")),
            is_active=getattr(new_user, 'is_active', True),
            created_at=getattr(new_user, 'created_at', None) or datetime.now(timezone.utc),
            last_login_at=getattr(new_user, 'last_login_at', None)
        )
    )


@router.post("/refresh")
async def refresh_token(request: RefreshTokenRequest):
    """
    Refresh access token using refresh token
    
    This endpoint allows you to get a new access token using your refresh token
    when the current access token expires.
    
    Returns:
    - New access token
    - Same refresh token (reused)
    """
    access_token = refresh_access_token(request.refresh_token)

    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token"
        )
    
    return {
        "access_token": access_token,
        "refresh_token": request.refresh_token,  # Keep the same refresh token
        "token_type": "bearer"
    }


@router.post("/logout", response_model=BaseResponse)
async def logout(request: LogoutRequest):
    """
    Logout by revoking the refresh token
    
    This endpoint invalidates the provided refresh token, effectively
    logging the user out from all devices using that token.
    
    Required: Valid refresh token in request body
    """
    success = revoke_refresh_token(request.refresh_token)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Refresh token not found"
        )
    
    return BaseResponse(message="Successfully logged out")
