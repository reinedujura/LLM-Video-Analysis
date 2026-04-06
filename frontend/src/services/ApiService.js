/* API service for communicating with backend. */

import { config } from "../config";

class ApiService {
    static async request(
        endpoint,
        options = {}
    ) {
        const url = `${config.API_BASE_URL}${endpoint}`;
        const isFormData = options.body instanceof FormData;

        const headersCopy = {
            ...options.headers,
        };

        // Don't set Content-Type for FormData (browser sets it automatically)
        if (!isFormData && !headersCopy["Content-Type"]) {
            headersCopy["Content-Type"] = "application/json";
        }

        // Add auth token if available
        const token = localStorage.getItem("access_token");
        if (token) {
            headersCopy.Authorization = `Bearer ${token}`;
        }

        try {
            const response = await fetch(url, {
                ...options,
                headers: headersCopy,
            });

            if (!response.ok) {
                const error = await response.json().catch(() => ({}));
                throw new Error(error.detail || `HTTP ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error(`API request failed: ${endpoint}`, error);
            throw error;
        }
    }

    static async login(username, password) {
        /*
         * Login with username and password.
         * @returns {Object} Token and user info
         */
        const response = await this.request(
            config.API_ENDPOINTS.LOGIN,
            {
                method: "POST",
                body: JSON.stringify({ username, password }),
            }
        );

        if (response.access_token) {
            localStorage.setItem("access_token", response.access_token);
            localStorage.setItem(
                "token_expires_in",
                response.expires_in
            );
        }

        return response;
    }

    static logout() {
        /* Clear authentication tokens. */
        localStorage.removeItem("access_token");
        localStorage.removeItem("token_expires_in");
    }

    static async analyzeMedia(file, analysisType, customPrompt) {
        /*
         * Analyze media file (video or image).
         *
         * @param {File} file - Media file to analyze
         * @param {string} analysisType - Type of analysis
         * @param {string} customPrompt - Optional custom prompt
         * @returns {Object} Analysis result
         */
        const formData = new FormData();
        formData.append("file", file);
        formData.append("analysis_type", analysisType);
        if (customPrompt) {
            formData.append("custom_prompt", customPrompt);
        }

        return this.request(
            config.API_ENDPOINTS.ANALYZE,
            {
                method: "POST",
                body: formData,
            }
        );
    }

    static async healthCheck() {
        /* Check API health status. */
        return this.request(config.API_ENDPOINTS.HEALTH);
    }
}

export default ApiService;
