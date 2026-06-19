import React, { useState } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { useContext } from 'react';
import { AuthContext } from '../../context/AuthContext';

export default function AdminSidebar() {
  const location = useLocation();
  const navigate = useNavigate();
  const { logout } = useContext(AuthContext);
  const [isMobileSidebarOpen, setIsMobileSidebarOpen] = useState(false);

  const menuItems = [
    { label: 'Dashboard', path: '/admin/dashboard' },
    { label: 'Products', path: '/admin/products' },
    { label: 'Categories', path: '/admin/categories' },
    { label: 'Orders', path: '/admin/orders' },
    { label: 'Users', path: '/admin/users' },
  ];

  const isActive = (path) => location.pathname === path;

  const handleLogout = async () => {
    await logout();
    navigate('/');
  };

  return (
    <>
      {/* Mobile Menu Button */}
      <button
        onClick={() => setIsMobileSidebarOpen(!isMobileSidebarOpen)}
        className="fixed top-4 left-4 z-40 lg:hidden rounded-lg bg-slate-100 px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-200"
      >
        Menu
      </button>

      {/* Overlay for mobile */}
      {isMobileSidebarOpen && (
        <div
          className="fixed inset-0 z-30 bg-black bg-opacity-50 lg:hidden"
          onClick={() => setIsMobileSidebarOpen(false)}
        />
      )}

      {/* Sidebar */}
      <div
        className={`fixed left-0 top-0 h-screen w-64 bg-white border-r border-slate-200 transform transition-transform duration-300 z-40 lg:relative lg:translate-x-0 ${
          isMobileSidebarOpen ? 'translate-x-0' : '-translate-x-full'
        }`}
      >
        <div className="flex flex-col h-full">
          {/* Logo */}
          <div className="border-b border-slate-200 p-6">
            <Link to="/admin/dashboard" className="text-2xl font-bold text-primary">
              Admin Panel
            </Link>
            <p className="text-xs text-slate-500 mt-1">StyleHub Shop</p>
          </div>

          {/* Navigation */}
          <nav className="flex-1 p-4 space-y-2 overflow-y-auto">
            {menuItems.map((item) => (
              <Link
                key={item.path}
                to={item.path}
                onClick={() => setIsMobileSidebarOpen(false)}
                className={`block px-4 py-3 rounded-lg transition ${
                  isActive(item.path)
                    ? 'bg-primary text-white font-medium'
                    : 'text-slate-700 hover:bg-slate-100'
                }`}
              >
                {item.label}
              </Link>
            ))}
          </nav>

          {/* Footer */}
          <div className="border-t border-slate-200 p-4 space-y-2">
            <button
              onClick={() => {
                handleLogout();
                setIsMobileSidebarOpen(false);
              }}
              className="w-full px-4 py-2 rounded-lg bg-red-50 text-red-600 hover:bg-red-100 transition font-medium"
            >
              Logout
            </button>
          </div>
        </div>
      </div>
    </>
  );
}
