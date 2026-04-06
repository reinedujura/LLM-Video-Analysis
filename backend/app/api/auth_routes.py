"""
Authentication API endpoints.

REST endpoints for user login and token management.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.core.security import JWTManager
from app.exceptions import ApplicationException
from app.schemas import LoginRequest, LoginResponse
from app.services import AuthenticationService
from app.utils import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/api/auth", tags=["authentication"])


@router.post("/login", response_model=LoginResponse)
async def login(
    request: LoginRequest,
    auth_service: Annotated[
        AuthenticationService, Depends(lambda: AuthenticationService())
    ] = None,
    jwt_manager: Annotated[
        JWTManager, Depends(lambda: JWTManager())
    ] = None,
) -> LoginResponse:
    """
    User login endpoint.

    Args:
        request: Login request with username and password
        auth_service: Authentication service instance
        jwt_manager: JWT token manager

    Returns:
        LoginResponse with access token

    Raises:
        HTTPException: If authentication fails
    """
    if auth_service is None:
        auth_service = AuthenticationService()
    if jwt_manager is None:
        jwt_manager = JWTManager()

    try:
        # Authenticate user
        user = auth_service.authenticate_user(
            request.username, request.password
        )

        # Create JWT token
        token_data = jwt_manager.create_access_token(user.username)

        logger.info(f"User login successful: {user.username}")

        return LoginResponse(
            access_token=token_data["access_token"],
            token_type=token_data["token_type"],
            expires_in=token_data["expires_in"],
        )

    except ApplicationException as exc:
        logger.warning(f"Login failed: {exc.detail}")
        raise HTTPException(
            status_code=exc.status_code,
            detail=exc.detail,
        )
