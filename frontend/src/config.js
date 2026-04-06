/* Frontend configuration loaded from environment variables. */

const API_BASE_URL =
    import.meta.env.VITE_API_URL || "http://localhost:8000";

export const config = {
    API_BASE_URL,
    API_ENDPOINTS: {
        LOGIN: "/api/auth/login",
        HEALTH: "/health",
        ANALYZE: "/api/analysis/analyze",
    },
};

export const ANALYSIS_TYPES = {
    COMPREHENSIVE: "comprehensive",
    BULLETS: "bullets",
    DETAILED: "detailed",
    PARAGRAPHS_TIMECODE: "paragraphs-timecode",
    QA: "qa",
    TRANSCRIPTION: "transcription",
};

export const ALLOWED_FILE_TYPES = {
    IMAGE: ["image/jpeg", "image/png", "image/webp", "image/gif"],
    VIDEO: ["video/mp4", "video/webm", "video/quicktime"],
};

export const MAX_FILE_SIZE_BYTES = 200 * 1024 * 1024; // 200MB
