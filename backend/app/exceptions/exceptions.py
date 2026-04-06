"""
Application-wide exception handling following error handling standards.

Defines custom exceptions with standardized error codes and messages.
"""

from enum import Enum
from typing import Optional


class ErrorCode(Enum):
    """
    Standard error codes following application error code conventions.
    
    Format: [SERVICE]_[ERROR_TYPE]_[DETAIL]
    """

    # Authentication & Authorization (100-199)
    INVALID_CREDENTIALS = (101, "Invalid username or password")
    TOKEN_EXPIRED = (102, "Authentication token has expired")
    INSUFFICIENT_PERMISSIONS = (103, "User lacks required permissions")
    INVALID_TOKEN = (104, "Invalid or malformed authentication token")
    SESSION_NOT_FOUND = (105, "User session not found")

    # Validation Errors (200-299)
    INVALID_INPUT = (201, "Input validation failed")
    MISSING_FIELD = (202, "Required field is missing")
    INVALID_FORMAT = (203, "Invalid data format")
    VALUE_OUT_OF_RANGE = (204, "Value is out of acceptable range")
    DUPLICATE_RESOURCE = (205, "Resource already exists")

    # Resource Errors (300-399)
    NOT_FOUND = (301, "Requested resource not found")
    ALREADY_EXISTS = (302, "Resource already exists")
    RESOURCE_LOCKED = (303, "Resource is locked for modification")
    RESOURCE_CONFLICT = (304, "Resource state conflict")

    # Service Errors (400-499)
    SERVICE_UNAVAILABLE = (401, "Service temporarily unavailable")
    DATABASE_ERROR = (402, "Database operation failed")
    EXTERNAL_API_ERROR = (403, "External API request failed")
    TIMEOUT = (404, "Request timeout")
    RATE_LIMIT_EXCEEDED = (405, "Rate limit exceeded")

    # System Errors (500-599)
    INTERNAL_ERROR = (501, "Internal server error")
    OUT_OF_MEMORY = (502, "Out of memory")
    DISK_FULL = (503, "Disk space full")
    UNKNOWN_ERROR = (504, "Unknown error occurred")


class ApplicationException(Exception):
    """
    Base application exception with standardized error handling.
    
    All application exceptions inherit from this class.
    """

    def __init__(
        self,
        error_code: ErrorCode,
        detail: Optional[str] = None,
        status_code: int = 400,
    ) -> None:
        """
        Initialize application exception.

        Args:
            error_code: Standard error code enum
            detail: Additional error details
            status_code: HTTP status code for the response

        Example:
            raise ApplicationException(
                error_code=ErrorCode.INVALID_INPUT,
                detail="Video file must be MP4 or WebM format"
            )
        """
        self.code = error_code.value[0]
        self.message = error_code.value[1]
        self.detail = detail or ""
        self.status_code = status_code
        super().__init__(self.message)


class ValidationException(ApplicationException):
    """Raised when input validation fails."""

    def __init__(self, detail: str) -> None:
        super().__init__(
            error_code=ErrorCode.INVALID_INPUT,
            detail=detail,
            status_code=400,
        )


class AuthenticationException(ApplicationException):
    """Raised when authentication fails."""

    def __init__(self, detail: str = "Authentication failed") -> None:
        super().__init__(
            error_code=ErrorCode.INVALID_CREDENTIALS,
            detail=detail,
            status_code=401,
        )


class AuthorizationException(ApplicationException):
    """Raised when user lacks required permissions."""

    def __init__(self, detail: str = "Insufficient permissions") -> None:
        super().__init__(
            error_code=ErrorCode.INSUFFICIENT_PERMISSIONS,
            detail=detail,
            status_code=403,
        )


class ResourceNotFoundException(ApplicationException):
    """Raised when requested resource not found."""

    def __init__(self, resource_type: str, resource_id: str) -> None:
        super().__init__(
            error_code=ErrorCode.NOT_FOUND,
            detail=f"{resource_type} with ID '{resource_id}' not found",
            status_code=404,
        )


class RateLimitException(ApplicationException):
    """Raised when rate limit is exceeded."""

    def __init__(self, detail: str = "Rate limit exceeded") -> None:
        super().__init__(
            error_code=ErrorCode.RATE_LIMIT_EXCEEDED,
            detail=detail,
            status_code=429,
        )


class ExternalServiceException(ApplicationException):
    """Raised when external service fails."""

    def __init__(self, service_name: str, detail: str) -> None:
        super().__init__(
            error_code=ErrorCode.EXTERNAL_API_ERROR,
            detail=f"{service_name}: {detail}",
            status_code=502,
        )
