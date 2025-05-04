import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './components/Login';
import Dashboard from './components/Dashboard';
import RaceReport from './components/RaceReport';
import { useAuth } from './AuthContext';

function App() {
    const { isAuthenticated } = useAuth();

    return (
        <Router>
            <Routes>
                <Route path="/login" element={!isAuthenticated ? <Login /> : <Navigate to="/" />} />
                <Route path="/" element={isAuthenticated ? <Dashboard /> : <Navigate to="/login" />} />
                <Route path="/race-report/:raceId" element={isAuthenticated ? <RaceReport /> : <Navigate to="/login" />} />
            </Routes>
        </Router>
    );
}

export default App;