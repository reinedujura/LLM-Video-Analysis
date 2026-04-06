"""
Health check and status endpoints.
"""

from datetime import datetime

from fastapi import APIRouter

from app.core.config import get_settings
from app.schemas import HealthCheckResponse

router = APIRouter(tags=["health"])

settings = get_settings()


@router.get("/health", response_model=HealthCheckResponse)
async def health_check() -> HealthCheckResponse:
    """
    Health check endpoint.

    Returns:
        HealthCheckResponse with service status

    Example:
        GET /health
        Response: {
            "status": "healthy",
            "version": "1.0.0",
            "timestamp": "2024-01-15T10:30:00Z"
        }
    """
    return HealthCheckResponse(
        status="healthy",
        version=settings.API_VERSION,
        timestamp=datetime.utcnow().isoformat() + "Z",
    )
