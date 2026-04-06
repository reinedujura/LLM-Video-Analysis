"""
Authentication and JWT token management following security standards.

Handles user authentication, token creation, and token verification.
Uses JWT tokens with proper expiration and secret key management.
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from pydantic import BaseModel

from app.core.config import get_settings
from app.exceptions import AuthenticationException

# HTTP Bearer credentials type (builtin in fastapi.security)
try:
    from fastapi.security import HTTPAuthCredentials
except ImportError:
    # Fallback for older FastAPI versions
    from typing import NamedTuple
    class HTTPAuthCredentials(NamedTuple):
        scheme: str
        credentials: str

security = HTTPBearer()


class TokenData(BaseModel):
    """JWT token payload data."""

    username: str
    exp: datetime


class TokenResponse(BaseModel):
    """Token response model for login endpoint."""

    access_token: str
    token_type: str = "bearer"
    expires_in: int


class JWTManager:
    """
    JWT token management following security standards.

    Handles creation, verification, and refresh of JWT tokens with
    proper expiration times and secret key management.
    """

    def __init__(self, settings=None):
        """
        Initialize JWT manager.

        Args:
            settings: Application settings (defaults to get_settings())
        """
        self.settings = settings or get_settings()
        self.algorithm = self.settings.ALGORITHM
        self.secret_key = self.settings.SECRET_KEY

    def create_access_token(
        self, username: str, expires_delta: Optional[timedelta] = None
    ) -> Dict[str, Any]:
        """
        Create a JWT access token.

        Args:
            username: Username to encode in token
            expires_delta: Custom expiration time (uses config default if None)

        Returns:
            Dictionary with access_token, token_type, and expires_in

        Example:
            token = jwt_manager.create_access_token("john_doe")
        """
        now = datetime.utcnow()

        if expires_delta:
            expire_time = now + expires_delta
        else:
            expire_time = now + timedelta(
                minutes=self.settings.ACCESS_TOKEN_EXPIRE_MINUTES
            )

        payload = {
            "sub": username,
            "iat": now,
            "exp": expire_time,
        }

        encoded_token = jwt.encode(
            payload, self.secret_key, algorithm=self.algorithm
        )

        return {
            "access_token": encoded_token,
            "token_type": "bearer",
            "expires_in": int(
                (expire_time - now).total_seconds()
            ),
        }

    def verify_token(self, token: str) -> TokenData:
        """
        Verify and decode JWT token.

        Args:
            token: JWT token string to verify

        Returns:
            TokenData with decoded token information

        Raises:
            AuthenticationException: If token is invalid or expired
        """
        try:
            payload = jwt.decode(
                token, self.secret_key, algorithms=[self.algorithm]
            )
            username = payload.get("sub")

            if not username:
                raise AuthenticationException(
                    "Token does not contain username claim"
                )

            return TokenData(
                username=username,
                exp=datetime.fromtimestamp(payload.get("exp")),
            )

        except jwt.ExpiredSignatureError:
            raise AuthenticationException("Token has expired")
        except jwt.InvalidTokenError:
            raise AuthenticationException("Invalid token")

    def get_current_user(
        self, credentials: HTTPAuthCredentials = Depends(security)
    ) -> str:
        """
        FastAPI dependency to get current authenticated user.

        Args:
            credentials: HTTP Bearer credentials from request header

        Returns:
            Username of authenticated user

        Raises:
            HTTPException: If authentication fails
        """
        try:
            token_data = self.verify_token(credentials.credentials)
            return token_data.username
        except AuthenticationException as exc:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=exc.detail,
                headers={"WWW-Authenticate": "Bearer"},
            )
