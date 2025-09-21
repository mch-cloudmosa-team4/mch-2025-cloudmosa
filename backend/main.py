"""
[Project name] Backend API

A FastAPI-based backend server with modular architecture.
"""

from contextlib import asynccontextmanager
from typing import Dict, Any

from fastapi import FastAPI, Request, status, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi

from app.config import settings
from app.router import health_router, items_router, auth_router, profile_router, files_router, job_router, application_router, search_router
from app.router import health_router, items_router, auth_router, profile_router, files_router, job_router, skills_router, user_skills_router
from app.utils import logger, format_error_response
from app.database import create_tables, ensure_extensions


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan events
    """
    # Startup
    logger.info(f"Starting {settings.app_name} v{settings.version}")
    logger.info(f"Debug mode: {settings.debug}")
    logger.info("Creating database tables...")
    ensure_extensions()
    create_tables()
    logger.info("Database tables created successfully")
    yield
    # Shutdown
    logger.info(f"Shutting down {settings.app_name}")


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    description=settings.description,
    version=settings.version,
    debug=settings.debug,
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["*"],
)


# Custom exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """
    Handle HTTPException with custom detail messages
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.detail,
            "error_code": f"HTTP_{exc.status_code}",
            "path": str(request.url)
        }
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Handle validation errors
    """
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=format_error_response([error.copy() for error in exc.errors()])
    )


@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    """
    Handle 404 errors
    """
    # Check if it's an HTTPException with custom detail
    if hasattr(exc, 'detail') and exc.detail:
        message = exc.detail
    else:
        message = "The requested resource was not found"
    
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "success": False,
            "message": message,
            "error_code": "NOT_FOUND",
            "path": str(request.url)
        }
    )


@app.exception_handler(500)
async def internal_server_error_handler(request: Request, exc):
    """
    Handle internal server errors
    """
    logger.error(f"Internal server error: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "message": "Internal server error occurred",
            "error_code": "INTERNAL_ERROR"
        }
    )


# Root endpoint
@app.get("/", tags=["root"])
async def root() -> Dict[str, Any]:
    """
    Root endpoint - API information
    """
    return {
        "message": f"Welcome to {settings.app_name}",
        "version": settings.version,
        "status": "running",
        "docs": "/docs" if settings.debug else "Documentation disabled in production"
    }


# Include routers
app.include_router(health_router, prefix=settings.api_prefix)
app.include_router(items_router, prefix=settings.api_prefix)
app.include_router(files_router, prefix=settings.api_prefix)
app.include_router(auth_router, prefix=settings.api_prefix)
app.include_router(profile_router, prefix=settings.api_prefix)
app.include_router(job_router, prefix=settings.api_prefix)
app.include_router(application_router, prefix=settings.api_prefix)
app.include_router(search_router, prefix=settings.api_prefix)
app.include_router(skills_router, prefix=settings.api_prefix)
app.include_router(user_skills_router, prefix=settings.api_prefix)


# Custom OpenAPI schema
def custom_openapi():
    """
    Generate custom OpenAPI schema
    """
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=settings.app_name,
        version=settings.version,
        description=settings.description,
        routes=app.routes,
    )
    
    # Add custom info
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level="debug" if settings.debug else "info"
    )