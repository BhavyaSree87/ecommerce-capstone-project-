import React, { useContext, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";

const Register = () => {
  const { register } = useContext(AuthContext);
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    mobile: "",
    password: "",
    confirmPassword: "",
    address: "",
    city: "",
    state: "",
    pincode: "",
  });

  const [error, setError] = useState(null);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
    setError(null);
  };

  const getDisplayError = (error) => {
    if (!error) return "Unable to register. Please try again.";
    if (typeof error === "string") return error;
    if (error.message) return error.message;
    if (error.detail) {
      if (typeof error.detail === "string") return error.detail;
      if (Array.isArray(error.detail)) {
        const messages = error.detail.map((item) => {
          if (typeof item === "string") return item;
          if (item?.msg) return item.msg;
          if (item?.message) return item.message;
          return null;
        }).filter(Boolean);
        if (messages.length) return messages.join(", ");
      }
    }
    return "Unable to register. Please try again.";
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!formData.name || !formData.email || !formData.mobile || !formData.password || !formData.confirmPassword || !formData.address || !formData.city || !formData.state || !formData.pincode) {
      setError("Please fill in all fields.");
      return;
    }

    if (formData.password !== formData.confirmPassword) {
      setError("Passwords do not match.");
      return;
    }

    try {
      await register({
        name: formData.name,
        email: formData.email,
        mobile: formData.mobile,
        password: formData.password,
        address: formData.address,
        city: formData.city,
        state: formData.state,
        pincode: formData.pincode,
      });
      navigate("/", { replace: true });
    } catch (err) {
      setError(getDisplayError(err));
    }
  };

  return (
    <div className="min-h-screen flex justify-center items-center bg-gray-100 px-4">
      <div className="bg-white shadow-lg rounded-3xl p-8 w-full max-w-md">
        <h2 className="text-3xl font-bold text-center mb-6">Register</h2>

        <form onSubmit={handleSubmit} className="space-y-4">
          {error && <div className="rounded-2xl bg-rose-100 border border-rose-200 p-3 text-rose-700">{error}</div>}

          <div>
            <label className="block text-sm font-medium text-slate-700 mb-2">Full Name</label>
            <input
              type="text"
              name="name"
              placeholder="Full name"
              value={formData.name}
              onChange={handleChange}
              className="w-full border rounded-2xl px-4 py-3"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-700 mb-2">Email</label>
            <input
              type="email"
              name="email"
              placeholder="Email"
              value={formData.email}
              onChange={handleChange}
              className="w-full border rounded-2xl px-4 py-3"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-700 mb-2">Mobile</label>
            <input
              type="text"
              name="mobile"
              placeholder="Mobile number"
              value={formData.mobile}
              onChange={handleChange}
              className="w-full border rounded-2xl px-4 py-3"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-700 mb-2">Address</label>
            <input
              type="text"
              name="address"
              placeholder="Street address"
              value={formData.address}
              onChange={handleChange}
              className="w-full border rounded-2xl px-4 py-3"
            />
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">City</label>
              <input
                type="text"
                name="city"
                placeholder="City"
                value={formData.city}
                onChange={handleChange}
                className="w-full border rounded-2xl px-4 py-3"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">State</label>
              <input
                type="text"
                name="state"
                placeholder="State"
                value={formData.state}
                onChange={handleChange}
                className="w-full border rounded-2xl px-4 py-3"
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-700 mb-2">Pincode</label>
            <input
              type="text"
              name="pincode"
              placeholder="Pincode"
              value={formData.pincode}
              onChange={handleChange}
              className="w-full border rounded-2xl px-4 py-3"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-700 mb-2">Password</label>
            <input
              type="password"
              name="password"
              placeholder="Password"
              value={formData.password}
              onChange={handleChange}
              className="w-full border rounded-2xl px-4 py-3"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-700 mb-2">Confirm Password</label>
            <input
              type="password"
              name="confirmPassword"
              placeholder="Confirm password"
              value={formData.confirmPassword}
              onChange={handleChange}
              className="w-full border rounded-2xl px-4 py-3"
            />
          </div>

          <button type="submit" className="w-full bg-primary text-white py-3 rounded-3xl font-semibold hover:bg-pink-600 transition">
            Register
          </button>
        </form>

        <p className="text-center mt-6 text-sm text-slate-600">
          Already have an account?
          <Link to="/login" className="text-primary font-semibold ml-1">Login</Link>
        </p>
      </div>
    </div>
  );
};

export default Register;