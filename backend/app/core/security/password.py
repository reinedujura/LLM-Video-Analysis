"""Password hashing utilities following security standards."""

from passlib.context import CryptContext

# Create password hashing context with PBKDF2 (no 72-byte limit, no backend issues)
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt.

    Args:
        password: Plain text password to hash

    Returns:
        Hashed password string

    Example:
        hashed = hash_password("my_secure_password")
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.

    Args:
        plain_password: Plain text password to verify
        hashed_password: Hashed password from database

    Returns:
        True if password matches, False otherwise

    Example:
        if verify_password("user_input", stored_hash):
            # Password is correct
    """
    return pwd_context.verify(plain_password, hashed_password)
