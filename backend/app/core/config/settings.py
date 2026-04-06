"""
Application configuration following configuration management standards.

Loads all settings from environment variables with proper validation.
Never hardcode secrets - all sensitive data comes from .env files.
"""

import os
from typing import List, Optional
from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    All sensitive data (API keys, database passwords, secrets) must be
    loaded from environment variables or .env files. Never commit secrets
    to version control.
    """

    # ============================================================================
    # Server Configuration
    # ============================================================================
    DEBUG: bool = False
    ENVIRONMENT: str = "production"
    SERVICE_NAME: str = "video-analytics-api"
    API_TITLE: str = "LLM Video Analytics API"
    API_VERSION: str = "1.0.0"
    API_DESCRIPTION: str = (
        "Analyze videos and images using Google Gemini AI with "
        "transcription and translation capabilities"
    )

    # ============================================================================
    # Server Host & Port
    # ============================================================================
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # ============================================================================
    # Security & Authentication
    # ============================================================================
    SECRET_KEY: str = ""  # REQUIRED - Set in .env
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # ============================================================================
    # CORS Configuration
    # ============================================================================
    CORS_ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://localhost",
        "https://127.0.0.1",
    ]

    # ============================================================================
    # Google Gemini AI Configuration
    # ============================================================================
    GEMINI_API_KEY: str = ""  # REQUIRED - Set in .env
    GEMINI_MODEL: str = "models/gemini-2.5-pro"
    GEMINI_TEMPERATURE: float = 0.0
    GEMINI_TIMEOUT_SECONDS: int = 300

    # ============================================================================
    # File Upload Configuration
    # ============================================================================
    MAX_FILE_SIZE_BYTES: int = 200 * 1024 * 1024  # 200MB
    ALLOWED_IMAGE_MIMETYPES: List[str] = [
        "image/jpeg",
        "image/png",
        "image/webp",
        "image/gif",
    ]
    ALLOWED_VIDEO_MIMETYPES: List[str] = [
        "video/mp4",
        "video/webm",
        "video/quicktime",
    ]

    # ============================================================================
    # Analysis Configuration
    # ============================================================================
    VALID_ANALYSIS_TYPES: List[str] = [
        "comprehensive",
        "bullets",
        "detailed",
        "paragraphs-timecode",
        "qa",
        "transcription",
    ]
    DEFAULT_ANALYSIS_TYPE: str = "comprehensive"

    # ============================================================================
    # Rate Limiting
    # ============================================================================
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_REQUESTS_PER_MINUTE: int = 30

    # ============================================================================
    # Logging Configuration
    # ============================================================================
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = (
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    def get_allowed_mimetypes(self) -> List[str]:
        """Get combined list of allowed MIME types for uploads."""
        return self.ALLOWED_IMAGE_MIMETYPES + self.ALLOWED_VIDEO_MIMETYPES

    def validate_settings(self) -> None:
        """
        Validate that all required settings are configured.

        Raises:
            ValueError: If required settings are missing
        """
        required_settings = {
            "SECRET_KEY": self.SECRET_KEY,
            "GEMINI_API_KEY": self.GEMINI_API_KEY,
        }

        missing_settings = [
            key for key, value in required_settings.items() if not value
        ]

        if missing_settings:
            raise ValueError(
                f"Missing required settings: {', '.join(missing_settings)}. "
                f"Set these in your .env file or environment variables."
            )

    class Config:
        """Pydantic configuration."""

        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """
    Get application settings (cached).

    Uses LRU cache to load settings only once per application lifetime.

    Returns:
        Settings instance with all application configuration

    Raises:
        ValueError: If required settings are missing
    """
    settings = Settings()
    settings.validate_settings()
    return settings
