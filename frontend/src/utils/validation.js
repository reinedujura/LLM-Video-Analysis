/* Validation utilities for frontend form and file validation. */

import { ALLOWED_FILE_TYPES, MAX_FILE_SIZE_BYTES } from "../config";

export class ValidationError extends Error {
    constructor(message) {
        super(message);
        this.name = "ValidationError";
    }
}

export const validateUsername = (username) => {
    /* Validate username format. */
    if (!username || username.length < 3) {
        throw new ValidationError("Username must be at least 3 characters");
    }
    if (username.length > 50) {
        throw new ValidationError(
            "Username must not exceed 50 characters"
        );
    }
};

export const validatePassword = (password) => {
    /* Validate password strength. */
    if (!password || password.length < 6) {
        throw new ValidationError(
            "Password must be at least 6 characters"
        );
    }
    if (password.length > 100) {
        throw new ValidationError(
            "Password must not exceed 100 characters"
        );
    }
};

export const validateFile = (file) => {
    /* Validate file for upload. */
    if (!file) {
        throw new ValidationError("File is required");
    }

    // Check file type
    const allowedTypes = [
        ...ALLOWED_FILE_TYPES.IMAGE,
        ...ALLOWED_FILE_TYPES.VIDEO,
    ];

    if (!allowedTypes.includes(file.type)) {
        throw new ValidationError(
            `File type '${file.type}' is not supported`
        );
    }

    // Check file size
    if (file.size > MAX_FILE_SIZE_BYTES) {
        const maxSizeMB = MAX_FILE_SIZE_BYTES / (1024 * 1024);
        throw new ValidationError(
            `File size exceeds ${maxSizeMB}MB limit`
        );
    }
};

export const formatFileSize = (bytes) => {
    /* Format bytes to human readable size. */
    if (bytes === 0) return "0 Bytes";

    const k = 1024;
    const sizes = ["Bytes", "KB", "MB", "GB"];
    const i = Math.floor(Math.log(bytes) / Math.log(k));

    return (
        Math.round((bytes / Math.pow(k, i)) * 100) / 100 +
        " " +
        sizes[i]
    );
};
