/* React hooks for common functionality. */

import { useState, useCallback } from "react";
import ApiService from "../services/ApiService";

export const useApi = () => {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const request = useCallback(async (fn) => {
        setLoading(true);
        setError(null);

        try {
            const result = await fn();
            return result;
        } catch (err) {
            const message =
                err.response?.data?.detail ||
                err.message ||
                "An error occurred";
            setError(message);
            throw err;
        } finally {
            setLoading(false);
        }
    }, []);

    return { loading, error, request };
};

export const useAnalysis = () => {
    const [analysis, setAnalysis] = useState(null);
    const { loading, error, request } = useApi();

    const analyze = useCallback(
        async (file, analysisType, customPrompt) => {
            const result = await request(() =>
                ApiService.analyzeMedia(
                    file,
                    analysisType,
                    customPrompt
                )
            );
            setAnalysis(result);
            return result;
        },
        [request]
    );

    return { analysis, loading, error, analyze };
};
