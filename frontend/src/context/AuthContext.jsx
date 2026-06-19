import React, { createContext, useEffect, useMemo, useState } from "react";
import {
  loadSession,
  logout as authLogout,
  login as authLogin,
  register as authRegister,
  updateProfile as authUpdateProfile,
  changePassword as authChangePassword,
  getRole,
} from "../services/authService";

const normalizeRole = (role) => {
  return typeof role === 'string' ? role.toLowerCase() : role;
};

export const AuthContext = createContext();

const AuthProvider = ({ children }) => {

  const [user, setUser] = useState(null);
  const [token, setToken] = useState(null);
  const [role, setRole] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [authLoading, setAuthLoading] = useState(true);
  const [authError, setAuthError] = useState(null);

  useEffect(() => {
    const session = loadSession();
    const userRole = getRole();
    
    console.log("[AUTH CONTEXT] Loading session - session exists:", !!session, "role:", userRole);
    
    if (session?.token && session?.user) {
      setUser(session.user);
      setToken(session.token);
      setRole(userRole || normalizeRole(session.user?.role) || null);
      setIsAuthenticated(true);
      console.log("[AUTH CONTEXT] Session loaded - normalized role:", userRole || normalizeRole(session.user?.role));
    }
    setAuthLoading(false);
  }, []);

  const login = async (payload) => {
    try {
      setAuthLoading(true);
      setAuthError(null);
      const response = await authLogin(payload);
      const normalizedRole = normalizeRole(response.user?.role);
      console.log("[AUTH CONTEXT] Login response received - raw role:", response.user?.role, "normalized role:", normalizedRole);
      
      setUser(response.user);
      setToken(response.token);
      setRole(normalizedRole || null);
      setIsAuthenticated(true);
      
      console.log("[AUTH CONTEXT] Auth state updated - isAuthenticated:", true, "role:", normalizedRole);
      return response;
    } catch (error) {
      setAuthError(error.message);
      throw error;
    } finally {
      setAuthLoading(false);
    }
  };

  const register = async (payload) => {
    try {
      setAuthLoading(true);
      setAuthError(null);
      const response = await authRegister(payload);
      const normalizedRole = normalizeRole(response.user?.role);
      setUser(response.user);
      setToken(response.token);
      setRole(normalizedRole || null);
      setIsAuthenticated(true);
      return response;
    } catch (error) {
      setAuthError(error.message);
      throw error;
    } finally {
      setAuthLoading(false);
    }
  };

  const logout = async () => {
    await authLogout();
    setUser(null);
    setToken(null);
    setRole(null);
    setIsAuthenticated(false);
  };

  const updateProfile = async (profile) => {
    const updatedUser = await authUpdateProfile(profile);
    setUser(updatedUser);
    return updatedUser;
  };

  const changePassword = async (data) => {
    const updatedUser = await authChangePassword(data);
    setUser(updatedUser);
    return updatedUser;
  };

  const value = useMemo(
    () => ({
      user,
      token,
      role,
      isAuthenticated,
      authLoading,
      authError,
      login,
      register,
      logout,
      updateProfile,
      changePassword,
    }),
    [user, token, role, isAuthenticated, authLoading, authError]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export default AuthProvider;