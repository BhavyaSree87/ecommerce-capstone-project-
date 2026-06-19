import React, { useContext, useMemo, useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { AuthContext } from "../../context/AuthContext";
import { ShopContext } from "../../context/ShopContext";

export default function Navbar() {
  const { user, role, isAuthenticated, logout } = useContext(AuthContext);
  const { products, wishlistCount, cartCount, searchQuery, setSearchQuery } = useContext(ShopContext);
  const [mobileOpen, setMobileOpen] = useState(false);
  const location = useLocation();
  const navigate = useNavigate();

  const suggestions = useMemo(() => {
    if (!searchQuery || searchQuery.length < 2) return [];
    const normalized = searchQuery.toLowerCase();
    return products
      .filter(
        (product) =>
          product.name.toLowerCase().includes(normalized) ||
          product.brand.toLowerCase().includes(normalized)
      )
      .slice(0, 5);
  }, [products, searchQuery]);

  const handleSearchChange = (e) => {
    const value = e.target.value;
    setSearchQuery(value);
    if (!location.pathname.startsWith("/search")) {
      navigate("/search");
    }
  };

  const handleLogout = async () => {
    await logout();
    navigate("/");
  };

  return (
    <header className="sticky top-0 z-40 bg-white shadow-sm">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16 gap-4">
          <div className="flex items-center gap-6">
            <Link to="/" className="text-2xl font-bold text-primary">StyleHub</Link>
            <nav className="hidden md:flex gap-4 text-sm text-gray-600 items-center">
              <Link to="/">Home</Link>
              <Link to="/categories">Categories</Link>
              <Link to="/products">Products</Link>
              <Link to="/wishlist" className="relative">
                Wishlist
                {wishlistCount > 0 && (
                  <span className="absolute -top-2 -right-5 bg-primary text-white text-[10px] rounded-full px-1">{wishlistCount}</span>
                )}
              </Link>
            </nav>
          </div>

          <div className="relative flex-1 hidden md:flex justify-center">
            <input
              value={searchQuery}
              onChange={handleSearchChange}
              type="search"
              placeholder="Search products, brands and more"
              className="w-full max-w-xl border rounded-md px-3 py-2 text-sm"
            />
            {suggestions.length > 0 && (
              <div className="absolute top-full left-0 right-0 mt-2 bg-white border border-slate-200 rounded-2xl shadow-lg overflow-hidden">
                {suggestions.map((item) => (
                  <Link
                    key={item.id}
                    to={`/product/${item.id}`}
                    className="block px-4 py-3 text-sm text-slate-700 hover:bg-slate-100"
                  >
                    <span className="font-medium">{item.name}</span> · {item.brand}
                  </Link>
                ))}
              </div>
            )}
          </div>

          <div className="flex items-center gap-4">
            <Link to="/cart" className="relative text-gray-600 hover:text-primary">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4"/></svg>
              {cartCount > 0 && (
                <span className="absolute -top-2 -right-3 bg-primary text-white text-[10px] rounded-full px-1">{cartCount}</span>
              )}
            </Link>
            {isAuthenticated ? (
              <div className="hidden md:flex items-center gap-3 text-sm text-gray-600">
                <span className="px-3 py-2 rounded-full bg-slate-100">Hi, {user?.name?.split(" ")[0] || "User"}</span>
                {role === 'admin' && (
                  <Link to="/admin/dashboard" className="text-slate-600 hover:text-primary">Admin Panel</Link>
                )}
                <Link to="/profile" className="text-slate-600 hover:text-primary">Profile</Link>
                <Link to="/orders" className="text-slate-600 hover:text-primary">Orders</Link>
                <button onClick={handleLogout} className="text-red-500 hover:text-red-600">Logout</button>
              </div>
            ) : (
              <div className="hidden md:flex items-center gap-3">
                <Link to="/login" className="text-sm font-medium text-blue-600">Login</Link>
                <Link to="/register" className="text-sm font-medium text-blue-600">Register</Link>
              </div>
            )}
          </div>

          <button
            type="button"
            onClick={() => setMobileOpen(!mobileOpen)}
            className="md:hidden text-gray-600"
            aria-label="Toggle navigation"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>
        </div>

        {mobileOpen && (
          <div className="mt-3 space-y-3 pb-4 md:hidden">
            <input
              value={searchQuery}
              onChange={handleSearchChange}
              type="search"
              placeholder="Search products, brands and more"
              className="w-full border rounded-md px-3 py-2 text-sm"
            />
            <div className="flex flex-col gap-2 text-sm">
              <Link to="/">Home</Link>
              <Link to="/categories">Categories</Link>
              <Link to="/products">Products</Link>
              <Link to="/wishlist" className="flex items-center justify-between">
                Wishlist
                {wishlistCount > 0 && (
                  <span className="bg-primary text-white text-[10px] rounded-full px-2">{wishlistCount}</span>
                )}
              </Link>
              <Link to="/cart" className="flex items-center justify-between">
                Cart
                {cartCount > 0 && (
                  <span className="bg-primary text-white text-[10px] rounded-full px-2">{cartCount}</span>
                )}
              </Link>
              {isAuthenticated ? (
                <>
                  {role === 'admin' && (
                    <Link to="/admin/dashboard" className="text-blue-600">Admin Panel</Link>
                  )}
                  <Link to="/profile" className="text-blue-600">Profile</Link>
                  <Link to="/orders" className="text-blue-600">Orders</Link>
                  <button onClick={handleLogout} className="text-red-500 text-left">Logout</button>
                </>
              ) : (
                <>
                  <Link to="/login" className="text-blue-600">Login</Link>
                  <Link to="/register" className="text-blue-600">Register</Link>
                </>
              )}
            </div>
          </div>
        )}
      </div>
    </header>
  );
}

