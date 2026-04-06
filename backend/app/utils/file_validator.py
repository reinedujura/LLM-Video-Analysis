"""
File handling utilities following standards.

Provides validation and processing for file uploads.
"""

import mimetypes
from typing import List

from app.core.config import get_settings
from app.exceptions import ValidationException


class FileValidator:
    """
    File validation utilities.

    Validates file types, sizes, and other file-related constraints.
    """

    def __init__(self, settings=None):
        """
        Initialize file validator.

        Args:
            settings: Application settings (defaults to get_settings())
        """
        self.settings = settings or get_settings()

    def validate_file_size(self, file_size_bytes: int) -> None:
        """
        Validate that file size does not exceed limit.

        Args:
            file_size_bytes: Size of file in bytes

        Raises:
            ValidationException: If file is too large
        """
        if file_size_bytes > self.settings.MAX_FILE_SIZE_BYTES:
            max_mb = self.settings.MAX_FILE_SIZE_BYTES / (1024 * 1024)
            raise ValidationException(
                f"File size exceeds maximum allowed size of {max_mb:.0f}MB"
            )

    def validate_mime_type(self, mime_type: str) -> None:
        """
        Validate that MIME type is allowed.

        Args:
            mime_type: MIME type of file

        Raises:
            ValidationException: If MIME type is not allowed
        """
        allowed_types = self.settings.get_allowed_mimetypes()

        if mime_type not in allowed_types:
            raise ValidationException(
                f"File type '{mime_type}' is not supported. "
                f"Allowed types: {', '.join(allowed_types)}"
            )

    def get_mime_type(self, filename: str) -> str:
        """
        Get MIME type from filename.

        Args:
            filename: Name of file

        Returns:
            MIME type string

        Raises:
            ValidationException: If MIME type cannot be determined
        """
        mime_type, _ = mimetypes.guess_type(filename)

        if not mime_type:
            raise ValidationException(
                f"Cannot determine file type for '{filename}'"
            )

        return mime_type

    def validate_file(
        self, filename: str, file_size_bytes: int
    ) -> str:
        """
        Validate file (size and type).

        Args:
            filename: Name of file to validate
            file_size_bytes: Size of file in bytes

        Returns:
            MIME type of file

        Raises:
            ValidationException: If validation fails
        """
        self.validate_file_size(file_size_bytes)
        mime_type = self.get_mime_type(filename)
        self.validate_mime_type(mime_type)

        return mime_type
