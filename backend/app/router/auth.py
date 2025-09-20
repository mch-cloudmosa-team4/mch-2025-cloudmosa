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
from app.schemas.auth import PhoneLoginRequest, TokenResponse, UserInfo, RefreshTokenRequest, LogoutRequest
from app.models.base import BaseResponse
from app.models.users import User
from app.crud.user import user
from app.utils.auth import create_tokens, refresh_access_token, revoke_refresh_token
from app.models.profiles import Profile

router = APIRouter(
    prefix="/auth", 
    tags=["Authentication"]
)
bearer_scheme = HTTPBearer(
    description="Access token authentication"
)


@router.post("/login", response_model=TokenResponse)
async def login_with_phone(
    request: PhoneLoginRequest,
    db: Session = Depends(get_db)
):
    """
    Login with phone number. If user does not exist, create a new user.
    
    Phone format: +2348012345678
    
    Returns access token and user information.
    """
    # Check if user exists or create new one
    existing_user = user.get_by_phone(db, request.phone)
    
    if existing_user:
        # Verify password
        if request.passwd_hash != existing_user.passwd_hash:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid phone number or password"
            )

        # Get user profile
        profile = db.query(Profile).filter(Profile.user_id == existing_user.id).first()
        user_obj = existing_user
    else:
        # Create new user with profile
        user_obj = user.create_user_with_profile(
            db=db,
            phone=request.phone,
            passwd_hash=request.passwd_hash,
            display_name=f"User {request.phone[-4:]}",
            primary_language_code="en"
        )
        # Get the created profile
        profile = db.query(Profile).filter(Profile.user_id == user_obj.id).first()
    
    # Create tokens
    tokens = create_tokens(user_obj)
    
    return TokenResponse(
        access_token=tokens["access_token"],
        refresh_token=tokens["refresh_token"],
        token_type="bearer",
        user=UserInfo(
            user_id=str(user_obj.id),
            phone=str(user_obj.phone),
            email=getattr(user_obj, 'email', None),
            display_name=str(profile.display_name) if profile else f"User {request.phone[-4:]}",
            is_active=getattr(user_obj, 'is_active', True),
            created_at=getattr(user_obj, 'created_at', None) or datetime.now(timezone.utc),
            last_login_at=getattr(user_obj, 'last_login_at', None)
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
