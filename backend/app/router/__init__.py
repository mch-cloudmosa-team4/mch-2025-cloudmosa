# API routers module

from .health import router as health_router
from .items import router as items_router
from .files import router as files_router
from .auth import router as auth_router
from .profile import router as profile_router
from .jobs import router as job_router
from .skills import router as skills_router
from .user_skills import router as user_skills_router

__all__ = ["health_router", "items_router", "auth_router", "profile_router", "files_router", "job_router", "skills_router", "user_skills_router"]
