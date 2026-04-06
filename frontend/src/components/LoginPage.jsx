/* Login page component. */

import { useState } from "react";
import { useAuth } from "../context/AuthContext";
import { validateUsername, validatePassword, ValidationError } from "../utils/validation";
import "./LoginPage.css";

const LoginPage = () => {
    const { login, isLoading, error } = useAuth();
    const [username, setUsername] = useState("demo_user");
    const [password, setPassword] = useState("demo_password");
    const [validationError, setValidationError] = useState("");

    const handleSubmit = async (e) => {
        e.preventDefault();
        setValidationError("");

        try {
            validateUsername(username);
            validatePassword(password);

            const success = await login(username, password);
            if (!success) {
                setValidationError("Login failed. Please try again.");
            }
        } catch (err) {
            if (err instanceof ValidationError) {
                setValidationError(err.message);
            } else {
                setValidationError("An unexpected error occurred");
            }
        }
    };

    return (
        <div className="login-page">
            <div className="login-container">
                <div className="login-card">
                    <h1 className="login-title">Video Analytics</h1>
                    <p className="login-subtitle">
                        Analyze videos and images with AI
                    </p>

                    {(error || validationError) && (
                        <div className="alert alert-error">
                            {error || validationError}
                        </div>
                    )}

                    <form onSubmit={handleSubmit} className="login-form">
                        <div className="form-group">
                            <label htmlFor="username">Username</label>
                            <input
                                id="username"
                                type="text"
                                value={username}
                                onChange={(e) => setUsername(e.target.value)}
                                placeholder="Enter your username"
                                disabled={isLoading}
                            />
                        </div>

                        <div className="form-group">
                            <label htmlFor="password">Password</label>
                            <input
                                id="password"
                                type="password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                placeholder="Enter your password"
                                disabled={isLoading}
                            />
                        </div>

                        <button
                            type="submit"
                            className="btn-primary login-button"
                            disabled={isLoading}
                        >
                            {isLoading ? (
                                <>
                                    <span className="spinner"></span>
                                    Logging in...
                                </>
                            ) : (
                                "Login"
                            )}
                        </button>
                    </form>

                    <p className="demo-hint">
                        Demo credentials: demo_user / demo_password
                    </p>
                </div>
            </div>
        </div>
    );
};

export default LoginPage;
