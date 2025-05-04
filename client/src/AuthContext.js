import React, { createContext, useContext, useState, useEffect } from 'react';
import axios from './axiosConfig';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [isAdmin, setIsAdmin] = useState(false);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        checkAuthStatus();
    }, []);

    const checkAuthStatus = async () => {
        try {
            const response = await axios.get('/api/auth/status');
            setIsAuthenticated(response.data.authenticated);
            setIsAdmin(response.data.is_admin || false);
        } catch (error) {
            console.error('Auth check failed:', error);
            setIsAuthenticated(false);
            setIsAdmin(false);
        } finally {
            setIsLoading(false);
        }
    };

    const login = async (username, password) => {
        try {
            const response = await axios.post('/api/auth/login', { username, password });
            setIsAuthenticated(true);
            setIsAdmin(response.data.is_admin || false);
            return { success: true };
        } catch (error) {
            console.error('Login failed:', error);
            return { 
                success: false, 
                error: error.response?.data?.error || 'Login failed' 
            };
        }
    };

    const logout = async () => {
        try {
            await axios.post('/api/auth/logout');
            setIsAuthenticated(false);
            setIsAdmin(false);
        } catch (error) {
            console.error('Logout failed:', error);
        }
    };

    if (isLoading) {
        return null; // or a loading spinner
    }

    return (
        <AuthContext.Provider value={{ 
            isAuthenticated, 
            isAdmin, 
            login, 
            logout 
        }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (!context) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
};

export default AuthContext; 