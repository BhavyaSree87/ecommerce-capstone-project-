import React, { useContext } from 'react';
import { Navigate } from 'react-router-dom';
import AdminSidebar from './components/AdminSidebar';
import { AuthContext } from '../context/AuthContext';
import Loader from '../components/common/Loader';

export default function AdminLayout({ children }) {
  const { isAuthenticated, authLoading, role } = useContext(AuthContext);
  const storedRole = window.localStorage.getItem('role')?.toLowerCase() || window.localStorage.getItem('ecom_user_role')?.toLowerCase();
  const storedToken = window.localStorage.getItem('token') || window.localStorage.getItem('ecom_jwt_token');
  const effectiveRole = role?.toLowerCase() || storedRole;

  console.log(
    "[ADMIN LAYOUT] Render - isAuthenticated:",
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

  if (!isAuthenticated && !(storedToken && effectiveRole === 'admin')) {
    console.log("[ADMIN LAYOUT] Not authenticated or not admin - redirecting to login");
    return <Navigate to="/login" replace />;
  }

  if (effectiveRole !== 'admin') {
    console.log("[ADMIN LAYOUT] Not admin (role:", effectiveRole, ") - redirecting to home");
    return <Navigate to="/" replace />;
  }

  return (
    <div className="flex h-screen bg-slate-50">
      <AdminSidebar />
      <main className="flex-1 overflow-auto lg:ml-0">
        {/* Header for mobile */}
        <div className="sticky top-0 z-10 border-b border-slate-200 bg-white p-4 lg:hidden">
          <h1 className="text-xl font-semibold text-slate-900">Admin Panel</h1>
        </div>
        
        {/* Content */}
        <div className="p-4 sm:p-6 lg:p-8">
          {children}
        </div>
      </main>
    </div>
  );
}
