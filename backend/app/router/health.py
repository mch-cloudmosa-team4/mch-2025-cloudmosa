"""
Health check and system information router
"""

from fastapi import APIRouter, Depends
from app.config import settings
from app.models import HealthCheck, BaseResponse


router = APIRouter(
    prefix="/health",
    tags=["health"],
    responses={
        200: {"description": "Success"},
        503: {"description": "Service unavailable"}
    }
)


@router.get("/", response_model=HealthCheck, summary="Health check")
async def health_check() -> HealthCheck:
    """
    Check if the service is healthy and running
    
    Returns:
        HealthCheck: Service health status
    """
    return HealthCheck(
        status="healthy",
        version=settings.version
    )


@router.get("/info", response_model=BaseResponse, summary="System information")
async def system_info() -> BaseResponse:
    """
    Get basic system information
    
    Returns:
        BaseResponse: System information
    """
    return BaseResponse(
        message=f"Welcome to {settings.app_name} v{settings.version}"
    )
