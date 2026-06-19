import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import AdminLayout from './AdminLayout';
import Dashboard from './pages/Dashboard';
import Products from './pages/Products';
import Categories from './pages/Categories';
import Orders from './pages/Orders';
import Users from './pages/Users';

export default function AdminRoutes() {
  return (
    <Routes>
      <Route path="" element={<Navigate to="dashboard" replace />} />
      <Route path="dashboard" element={<AdminLayout><Dashboard /></AdminLayout>} />
      <Route path="products" element={<AdminLayout><Products /></AdminLayout>} />
      <Route path="categories" element={<AdminLayout><Categories /></AdminLayout>} />
      <Route path="orders" element={<AdminLayout><Orders /></AdminLayout>} />
      <Route path="users" element={<AdminLayout><Users /></AdminLayout>} />
      <Route path="*" element={<Navigate to="dashboard" replace />} />
    </Routes>
  );
}
