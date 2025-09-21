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
from .applications import ApplicationBase, ApplicationCreate, ApplicationUpdate, ApplicationResponse
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
from .user_skills import (
    UserSkillBase,
    UserSkillCreate,
    UserSkillUpdate,
    UserSkillResponse,
    UserSkillsRequest,
    UserSkillSummary,
    UserSkillsResponse,
    MultipleUserSkillsResponse
)
from .locations import (
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
    "ApplicationBase",
    "ApplicationCreate",
    "ApplicationUpdate",
    "ApplicationResponse",
    "SkillBase",
    "SkillCreate",
    "SkillUpdate",
    "SkillResponse",
    "SkillSearchResponse",
    "SkillListResponse",
    "SkillStatisticsResponse",
    "PopularSkillResponse",
    "UserSkillBase",
    "UserSkillCreate",
    "UserSkillUpdate",
    "UserSkillResponse",
    "UserSkillsRequest",
    "UserSkillSummary",
    "UserSkillsResponse",
    "MultipleUserSkillsResponse",
    "LocationResponse",
    "LocationCreateRequest",
    "LocationUpdateRequest",
    "LocationSearchRequest",
    "LocationListResponse",
    "CountryResponse",
    "CountryListResponse",
    "CityListResponse",
    "LocationStatsResponse"
]
