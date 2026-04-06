"""Exception module for error handling."""

from .exceptions import (
    ApplicationException,
    AuthenticationException,
    AuthorizationException,
    ErrorCode,
    ExternalServiceException,
    RateLimitException,
    ResourceNotFoundException,
    ValidationException,
)

__all__ = [
    "ApplicationException",
    "AuthenticationException",
    "AuthorizationException",
    "ErrorCode",
    "ExternalServiceException",
    "RateLimitException",
    "ResourceNotFoundException",
    "ValidationException",
]
