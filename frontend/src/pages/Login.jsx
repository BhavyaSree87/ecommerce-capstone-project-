import React, { useContext, useEffect, useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";

const Login = () => {
  const { login, isAuthenticated, authError, role } = useContext(AuthContext);
  const [formData, setFormData] = useState({ email: "", password: "" });
  const [error, setError] = useState(null);
  const navigate = useNavigate();
  const location = useLocation();
  const from = location.state?.from?.pathname || "/";

  useEffect(() => {
    if (isAuthenticated) {
      const normalizedRole = role?.toLowerCase();
      console.log("[LOGIN PAGE] Authenticated - raw role:", role, "normalized role:", normalizedRole);
      
      if (normalizedRole === 'admin') {
        console.log("[LOGIN PAGE] Admin user detected - redirecting to /admin/dashboard");
        navigate('/admin/dashboard', { replace: true });
      } else {
        console.log("[LOGIN PAGE] Regular user - redirecting to:", from);
        navigate(from, { replace: true });
      }
    }
  }, [isAuthenticated, role, from, navigate]);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
    setError(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!formData.email || !formData.password) {
      setError("Please enter both email and password.");
      return;
    }

    try {
      console.log("[LOGIN PAGE] Attempting login with email:", formData.email);
      const response = await login(formData);
      console.log("[LOGIN PAGE] Login successful - response:", response);
      console.log("[LOGIN PAGE] User role from response:", response.user?.role);
    } catch (err) {
      console.log("[LOGIN PAGE] Login failed:", err.message);
      setError(err.message || "Unable to login. Please try again.");
    }
  };

  return (
    <div className="min-h-screen flex justify-center items-center bg-gray-100 px-4">
      <div className="bg-white shadow-lg rounded-3xl p-8 w-full max-w-md">
        <h2 className="text-3xl font-bold text-center mb-6">Login</h2>

        <form onSubmit={handleSubmit} className="space-y-5">
          {(error || authError) && (
            <div className="rounded-2xl bg-rose-100 border border-rose-200 p-3 text-rose-700">
              {error || authError}
            </div>
          )}

          <div>
            <label className="block text-sm font-medium text-slate-700 mb-2">Email</label>
            <input
              type="email"
              name="email"
              placeholder="Enter your email"
              value={formData.email}
              onChange={handleChange}
              className="w-full border rounded-2xl px-4 py-3"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-700 mb-2">Password</label>
            <input
              type="password"
              name="password"
              placeholder="Enter your password"
              value={formData.password}
              onChange={handleChange}
              className="w-full border rounded-2xl px-4 py-3"
            />
          </div>

          <button
            type="submit"
            className="w-full bg-primary text-white py-3 rounded-3xl font-semibold hover:bg-pink-600 transition"
          >
            Login
          </button>
        </form>

        <p className="text-center mt-6 text-sm text-slate-600">
          Don&apos;t have an account?{' '}
          <Link to="/register" className="text-primary font-semibold">
            Register
          </Link>
        </p>
      </div>
    </div>
  );
};

export default Login;