/* React context for authentication state management. */

import { createContext, useContext, useState } from "react";

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [isAuthenticated, setIsAuthenticated] = useState(
        localStorage.getItem("access_token") !== null
    );
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);

    const login = async (username, password) => {
        /* Authenticate user. */
        setIsLoading(true);
        setError(null);

        try {
            const response = await fetch("/api/auth/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ username, password }),
            });

            if (!response.ok) {
                const data = await response.json();
                throw new Error(data.detail || "Login failed");
            }

            const data = await response.json();
            localStorage.setItem("access_token", data.access_token);
            localStorage.setItem("token_expires_in", data.expires_in);
            setIsAuthenticated(true);

            return true;
        } catch (err) {
            setError(err.message);
            return false;
        } finally {
            setIsLoading(false);
        }
    };

    const logout = () => {
        /* Logout user. */
        localStorage.removeItem("access_token");
        localStorage.removeItem("token_expires_in");
        setIsAuthenticated(false);
    };

    return (
        <AuthContext.Provider
            value={{
                isAuthenticated,
                isLoading,
                error,
                login,
                logout,
            }}
        >
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (!context) {
        throw new Error("useAuth must be used within AuthProvider");
    }
    return context;
};
