/* Analysis page component for video/image analysis. */

import { useState } from "react";
import { useAuth } from "../context/AuthContext";
import { useApi } from "../hooks/useApi";
import { validateFile, formatFileSize, ValidationError } from "../utils/validation";
import ApiService from "../services/ApiService";
import { ANALYSIS_TYPES } from "../config";
import "./AnalysisPage.css";

const AnalysisPage = () => {
    const { logout } = useAuth();
    const { loading, error, request } = useApi();
    const [selectedFile, setSelectedFile] = useState(null);
    const [analysisType, setAnalysisType] = useState(
        ANALYSIS_TYPES.COMPREHENSIVE
    );
    const [customPrompt, setCustomPrompt] = useState("");
    const [analysis, setAnalysis] = useState(null);
    const [validationError, setValidationError] = useState("");

    const handleFileSelect = (e) => {
        const file = e.target.files[0];
        setValidationError("");
        setAnalysis(null);

        if (file) {
            try {
                validateFile(file);
                setSelectedFile(file);
            } catch (err) {
                if (err instanceof ValidationError) {
                    setValidationError(err.message);
                }
                setSelectedFile(null);
            }
        }
    };

    const handleAnalyze = async () => {
        if (!selectedFile) {
            setValidationError("Please select a file first");
            return;
        }

        setValidationError("");

        try {
            const result = await request(() =>
                ApiService.analyzeMedia(
                    selectedFile,
                    analysisType,
                    customPrompt || undefined
                )
            );
            setAnalysis(result);
        } catch (err) {
            setValidationError("Analysis failed: " + err.message);
        }
    };

    const handleLogout = () => {
        logout();
    };

    return (
        <div className="analysis-page">
            <header className="header">
                <div className="header-content">
                    <h1>Video Analytics</h1>
                    <button
                        className="btn-secondary"
                        onClick={handleLogout}
                    >
                        Logout
                    </button>
                </div>
            </header>

            <main className="main-content">
                <div className="container">
                    <div className="analysis-grid">
                        {/* Upload Section */}
                        <div className="upload-section">
                            <h2>Upload Media</h2>

                            {(error || validationError) && (
                                <div className="alert alert-error">
                                    {error || validationError}
                                </div>
                            )}

                            <div className="upload-area">
                                <input
                                    type="file"
                                    id="file-input"
                                    onChange={handleFileSelect}
                                    accept="image/*,video/*"
                                    disabled={loading}
                                    className="file-input"
                                />
                                <label
                                    htmlFor="file-input"
                                    className="upload-label"
                                >
                                    <span className="upload-icon">📁</span>
                                    <span className="upload-text">
                                        {selectedFile
                                            ? `Selected: ${selectedFile.name}`
                                            : "Click to select or drag file"}
                                    </span>
                                    {selectedFile && (
                                        <span className="file-size">
                                            {formatFileSize(selectedFile.size)}
                                        </span>
                                    )}
                                </label>
                            </div>

                            <div className="form-group">
                                <label htmlFor="analysis-type">
                                    Analysis Type
                                </label>
                                <select
                                    id="analysis-type"
                                    value={analysisType}
                                    onChange={(e) =>
                                        setAnalysisType(e.target.value)
                                    }
                                    disabled={loading}
                                >
                                    {Object.entries(ANALYSIS_TYPES).map(
                                        ([key, value]) => (
                                            <option key={value} value={value}>
                                                {key.replace(/_/g, " ")}
                                            </option>
                                        )
                                    )}
                                </select>
                            </div>

                            <div className="form-group">
                                <label htmlFor="custom-prompt">
                                    Custom Prompt (Optional)
                                </label>
                                <textarea
                                    id="custom-prompt"
                                    value={customPrompt}
                                    onChange={(e) =>
                                        setCustomPrompt(e.target.value)
                                    }
                                    placeholder="Enter custom analysis prompt..."
                                    disabled={loading}
                                    rows="4"
                                />
                            </div>

                            <button
                                className="btn-primary analyze-button"
                                onClick={handleAnalyze}
                                disabled={!selectedFile || loading}
                            >
                                {loading ? (
                                    <>
                                        <span className="spinner"></span>
                                        Analyzing...
                                    </>
                                ) : (
                                    "Analyze Media"
                                )}
                            </button>
                        </div>

                        {/* Results Section */}
                        {analysis && (
                            <div className="results-section">
                                <h2>Analysis Results</h2>

                                <div className="result-card">
                                    <div className="result-header">
                                        <span className="result-type">
                                            {analysis.analysis_type}
                                        </span>
                                        <span className="result-time">
                                            {analysis.processing_time_seconds.toFixed(
                                                2
                                            )}{" "}
                                            seconds
                                        </span>
                                    </div>

                                    <div className="result-content">
                                        {analysis.result}
                                    </div>

                                    <div className="result-footer">
                                        <small className="text-muted">
                                            ID: {analysis.analysis_id}
                                        </small>
                                    </div>
                                </div>

                                <button
                                    className="btn-secondary"
                                    onClick={() => {
                                        setAnalysis(null);
                                        setSelectedFile(null);
                                        document.getElementById(
                                            "file-input"
                                        ).value = "";
                                    }}
                                >
                                    Analyze Another File
                                </button>
                            </div>
                        )}
                    </div>
                </div>
            </main>
        </div>
    );
};

export default AnalysisPage;
