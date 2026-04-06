/* Main Application component. */

import { useState, useEffect } from "react";
import { AuthProvider, useAuth } from "./context/AuthContext";
import LoginPage from "./components/LoginPage";
import AnalysisPage from "./components/AnalysisPage";
import "./styles/index.css";

const AppContent = () => {
    const { isAuthenticated } = useAuth();

    return isAuthenticated ? <AnalysisPage /> : <LoginPage />;
};

function App() {
    return (
        <AuthProvider>
            <AppContent />
        </AuthProvider>
    );
}

export default App;
