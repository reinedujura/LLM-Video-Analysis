"""
User authentication and management service.

Implements service layer for user authentication.
Single responsibility: handles user login and credential verification.
"""

import json
import logging
from typing import Optional

from app.core.security import hash_password, verify_password
from app.exceptions import AuthenticationException
from app.schemas import UserProfile
from app.utils import get_logger

logger = get_logger(__name__)


class AuthenticationService:
    """
    User authentication service.

    Handles user login, password verification, and user management.
    Currently uses JSON file storage (can be replaced with database).
    """

    def __init__(self, users_file: str = "users.json"):
        """
        Initialize authentication service.

        Args:
            users_file: Path to users storage file
        """
        self.users_file = users_file
        self._load_users()

    def _load_users(self) -> None:
        """Load users from storage file."""
        try:
            with open(self.users_file, "r") as f:
                self.users = json.load(f)
        except FileNotFoundError:
            # Create default demo user if file doesn't exist
            self.users = {
                "demo_user": {
                    "username": "demo_user",
                    "password": hash_password("demo_password"),
                    "email": "demo@example.com",
                }
            }
            self._save_users()

    def _save_users(self) -> None:
        """Save users to storage file."""
        with open(self.users_file, "w") as f:
            json.dump(self.users, f, indent=2)

    def authenticate_user(
        self, username: str, password: str
    ) -> UserProfile:
        """
        Authenticate a user by username and password.

        Args:
            username: Username
            password: Plain text password

        Returns:
            UserProfile if authentication successful

        Raises:
            AuthenticationException: If credentials are invalid
        """
        user = self.users.get(username)

        if not user:
            logger.warning(f"Login attempt for non-existent user: {username}")
            raise AuthenticationException("Invalid credentials")

        if not verify_password(password, user.get("password", "")):
            logger.warning(f"Failed login attempt for user: {username}")
            raise AuthenticationException("Invalid credentials")

        logger.info(f"User authenticated: {username}")

        return UserProfile(
            username=user["username"],
            email=user.get("email"),
            created_at=user.get("created_at", ""),
        )

    def get_user(self, username: str) -> Optional[UserProfile]:
        """
        Get user profile by username.

        Args:
            username: Username to lookup

        Returns:
            UserProfile if found, None otherwise
        """
        user = self.users.get(username)

        if not user:
            return None

        return UserProfile(
            username=user["username"],
            email=user.get("email"),
            created_at=user.get("created_at", ""),
        )
