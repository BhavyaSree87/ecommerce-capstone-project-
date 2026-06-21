import React, { useContext } from 'react';
import { Navigate } from 'react-router-dom';
import { AuthContext } from '../../context/AuthContext';
import Loader from './Loader';
import { getToken, getRole } from '../../services/authService';

export default function ProtectedAdminRoute({ children }) {
  const { isAuthenticated, authLoading, role } = useContext(AuthContext);
  const storedRole = getRole();
  const storedToken = getToken();
  const isAdminLocal = !!storedToken && storedRole === 'admin';

  console.log(
    "[PROTECTED ADMIN ROUTE] Checking access - isAuthenticated:",
    isAuthenticated,
    "context role:",
    role,
    "stored role:",
    storedRole,
    "authLoading:",
    authLoading,
    "token exists:",
    !!storedToken
  );

  if (authLoading) {
    return <Loader />;
  }

  if (!isAuthenticated && !isAdminLocal) {
    console.log("[PROTECTED ADMIN ROUTE] Not authenticated or admin - redirecting to login");
    return <Navigate to="/login" replace />;
  }

  if ((role?.toLowerCase() || storedRole) !== 'admin') {
    console.log("[PROTECTED ADMIN ROUTE] Not admin - redirecting to home");
    return <Navigate to="/" replace />;
  }

  console.log("[PROTECTED ADMIN ROUTE] Access granted for admin");
  return children;
}
