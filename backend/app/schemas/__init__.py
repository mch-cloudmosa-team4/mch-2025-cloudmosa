# Pydantic schemas module

from .common import (
    PaginationMeta,
    PaginatedResponse, 
    ApiError,
    ValidationError,
    ValidationErrorResponse
)
from .item import ItemBase, ItemCreate, ItemUpdate, ItemResponse
from .auth import (
    PhoneLoginRequest,
    TokenResponse,
    RefreshTokenRequest,
    LogoutRequest,
    UserInfo
)
from .profile import (
    ProfileResponse,
    ProfileUpdateRequest,
    ProfileListResponse,
    ProfileUpdateResponse
)
from .jobs import JobBase, JobCreate, JobUpdate, JobResponse
from .skills import (
    SkillBase,
    SkillCreate,
    SkillUpdate,
    SkillResponse,
    SkillSearchResponse,
    SkillListResponse,
    SkillStatisticsResponse,
    PopularSkillResponse
)

__all__ = [
    "PaginationMeta",
    "PaginatedResponse",
    "ApiError", 
    "ValidationError",
    "ValidationErrorResponse",
    "ItemBase",
    "ItemCreate", 
    "ItemUpdate",
    "ItemResponse",
    "PhoneLoginRequest",
    "TokenResponse",
    "RefreshTokenRequest",
    "LogoutRequest",
    "UserInfo",
    "ProfileResponse",
    "ProfileUpdateRequest",
    "ProfileListResponse",
    "ProfileUpdateResponse",
    "ItemResponse",
    "JobBase",
    "JobCreate",
    "JobUpdate",
    "JobResponse",
    "SkillBase",
    "SkillCreate",
    "SkillUpdate",
    "SkillResponse",
    "SkillSearchResponse",
    "SkillListResponse",
    "SkillStatisticsResponse",
    "PopularSkillResponse"
]
