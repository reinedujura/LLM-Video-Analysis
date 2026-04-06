"""
Main FastAPI application following architecture standards.

Configures FastAPI with middleware, routes, error handlers, and CORS.
"""

import logging
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.api import analysis_routes, auth_routes, health_routes
from app.core.config import get_settings
from app.exceptions import ApplicationException
from app.utils import configure_logging, get_logger

# Load environment variables from .env file
load_dotenv()

# Configure logging
configure_logging()
logger = get_logger(__name__)

# Load settings
settings = get_settings()

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application startup and shutdown events.

    Args:
        app: FastAPI application instance
    """
    # Startup
    logger.info(f"Starting {settings.SERVICE_NAME}")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Debug mode: {settings.DEBUG}")

    yield

    # Shutdown
    logger.info(f"Shutting down {settings.SERVICE_NAME}")


# Create FastAPI app
app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION,
    lifespan=lifespan,
)

# Apply rate limiter
app.state.limiter = limiter

# ============================================================================
# MIDDLEWARE SETUP
# ============================================================================

# CORS Middleware - must be before other middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# ERROR HANDLERS
# ============================================================================


@app.exception_handler(ApplicationException)
async def application_exception_handler(
    request: Request, exc: ApplicationException
):
    """
    Handle application exceptions with standardized error response.

    Args:
        request: FastAPI request
        exc: Application exception

    Returns:
        JSON error response
    """
    logger.error(
        f"Application error: code={exc.code}, message={exc.message}, "
        f"detail={exc.detail}"
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": exc.code,
                "message": exc.message,
                "detail": exc.detail,
            },
        },
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """
    Handle unexpected exceptions.

    Args:
        request: FastAPI request
        exc: Exception

    Returns:
        JSON error response
    """
    logger.error(f"Unexpected error: {str(exc)}", exc_info=True)

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error": {
                "code": 501,
                "message": "Internal server error",
                "detail": (
                    "An unexpected error occurred"
                    if not settings.DEBUG
                    else str(exc)
                ),
            },
        },
    )


# ============================================================================
# ROUTE REGISTRATION
# ============================================================================

app.include_router(health_routes.router)
app.include_router(auth_routes.router)
app.include_router(analysis_routes.router)


# ============================================================================
# ROOT ENDPOINT
# ============================================================================


@app.get("/")
async def root():
    """
    Root endpoint with API information.

    Returns:
        API information and available endpoints
    """
    return {
        "name": settings.API_TITLE,
        "version": settings.API_VERSION,
        "description": settings.API_DESCRIPTION,
        "docs": "/docs",
        "openapi": "/openapi.json",
    }


# ============================================================================
# APPLICATION EXPORT
# ============================================================================

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host=settings.HOST,
        port=settings.PORT,
        log_level=settings.LOG_LEVEL.lower(),
    )
