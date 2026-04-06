"""
Pydantic schemas for request/response validation.

Following type safety standards with comprehensive schema validation.
"""

from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class AnalysisType(str, Enum):
    """Supported analysis types for video/image analysis."""

    COMPREHENSIVE = "comprehensive"
    BULLETS = "bullets"
    DETAILED = "detailed"
    PARAGRAPHS_TIMECODE = "paragraphs-timecode"
    QA = "qa"
    TRANSCRIPTION = "transcription"


class LoginRequest(BaseModel):
    """User login request schema."""

    username: str = Field(
        ..., min_length=3, max_length=50, description="Username"
    )
    password: str = Field(
        ..., min_length=6, max_length=100, description="Password"
    )

    class Config:
        """Schema configuration."""

        json_schema_extra = {
            "example": {
                "username": "john_doe",
                "password": "secure_password_123",
            }
        }


class LoginResponse(BaseModel):
    """User login response schema."""

    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")
    expires_in: int = Field(..., description="Token expiration in seconds")


class VideoAnalysisRequest(BaseModel):
    """Video/image analysis request schema."""

    analysis_type: AnalysisType = Field(
        default=AnalysisType.COMPREHENSIVE,
        description="Type of analysis to perform",
    )
    custom_prompt: Optional[str] = Field(
        default=None,
        max_length=2000,
        description="Custom analysis prompt (optional)",
    )
    include_timestamps: bool = Field(
        default=True,
        description="Include timestamps in transcription (if applicable)",
    )

    class Config:
        """Schema configuration."""

        json_schema_extra = {
            "example": {
                "analysis_type": "comprehensive",
                "custom_prompt": None,
                "include_timestamps": True,
            }
        }


class AnalysisResult(BaseModel):
    """Analysis result schema."""

    analysis_id: str = Field(
        ..., description="Unique analysis identifier"
    )
    analysis_type: AnalysisType = Field(
        ..., description="Type of analysis performed"
    )
    result: str = Field(..., description="Analysis result text")
    created_at: str = Field(..., description="Creation timestamp")
    processing_time_seconds: float = Field(
        ..., description="Time taken for analysis"
    )


class VideoUploadResponse(BaseModel):
    """Video upload response schema."""

    video_id: str = Field(..., description="Uploaded video identifier")
    filename: str = Field(..., description="Original filename")
    size_bytes: int = Field(..., description="File size in bytes")
    mime_type: str = Field(..., description="MIME type of uploaded file")


class UserProfile(BaseModel):
    """User profile schema."""

    username: str = Field(..., description="Username")
    email: Optional[str] = Field(None, description="Email address")
    created_at: str = Field(..., description="Account creation timestamp")


class HealthCheckResponse(BaseModel):
    """Health check response schema."""

    status: str = Field(..., description="Service status")
    version: str = Field(..., description="API version")
    timestamp: str = Field(..., description="Current timestamp")
