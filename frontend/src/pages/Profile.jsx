import React, { useContext, useEffect, useState } from "react";
import { AuthContext } from "../context/AuthContext";
import Toast from "../components/common/Toast";

export default function Profile() {
  const { user, updateProfile, changePassword } = useContext(AuthContext);
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    mobile: "",
  });
  const [passwordData, setPasswordData] = useState({
    currentPassword: "",
    newPassword: "",
    confirmPassword: "",
  });
  const [toast, setToast] = useState(null);

  useEffect(() => {
    if (user) {
      setFormData({
        name: user.name || "",
        email: user.email || "",
        mobile: user.mobile || "",
      });
    }
  }, [user]);

  const handleChange = (e) => {
    setFormData((prev) => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const handlePasswordChange = (e) => {
    setPasswordData((prev) => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const handleProfileSubmit = async (e) => {
    e.preventDefault();

    if (!formData.name || !formData.email || !formData.mobile) {
      setToast({ message: "Please complete all profile fields.", type: "error" });
      return;
    }

    try {
      await updateProfile(formData);
      setToast({ message: "Profile updated successfully." });
    } catch (err) {
      setToast({ message: err.message, type: "error" });
    }
  };

  const handlePasswordSubmit = async (e) => {
    e.preventDefault();
    if (passwordData.newPassword !== passwordData.confirmPassword) {
      setToast({ message: "New passwords do not match.", type: "error" });
      return;
    }

    try {
      await changePassword({
        email: user.email,
        oldPassword: passwordData.currentPassword,
        newPassword: passwordData.newPassword,
      });
      setToast({ message: "Password updated successfully." });
      setPasswordData({ currentPassword: "", newPassword: "", confirmPassword: "" });
    } catch (err) {
      setToast({ message: err.message, type: "error" });
    }
  };

  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      <div className="grid gap-6 lg:grid-cols-[1fr_360px]">
        <div className="space-y-6">
          <section className="bg-white rounded-3xl shadow-sm p-6">
            <h1 className="text-2xl font-semibold mb-4">My Profile</h1>
            <form onSubmit={handleProfileSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-slate-700">Name</label>
                <input
                  name="name"
                  value={formData.name}
                  onChange={handleChange}
                  className="w-full border rounded-xl px-4 py-3 mt-2"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-700">Email</label>
                <input
                  name="email"
                  value={formData.email}
                  type="email"
                  onChange={handleChange}
                  className="w-full border rounded-xl px-4 py-3 mt-2"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-700">Mobile</label>
                <input
                  name="mobile"
                  value={formData.mobile}
                  onChange={handleChange}
                  className="w-full border rounded-xl px-4 py-3 mt-2"
                />
              </div>
              <button type="submit" className="bg-primary text-white rounded-2xl px-5 py-3 font-medium hover:bg-pink-600 transition">Save profile</button>
            </form>
          </section>

          <section className="bg-white rounded-3xl shadow-sm p-6">
            <h2 className="text-2xl font-semibold mb-4">Change Password</h2>
            <form onSubmit={handlePasswordSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-slate-700">Current Password</label>
                <input
                  name="currentPassword"
                  value={passwordData.currentPassword}
                  type="password"
                  onChange={handlePasswordChange}
                  className="w-full border rounded-xl px-4 py-3 mt-2"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-700">New Password</label>
                <input
                  name="newPassword"
                  value={passwordData.newPassword}
                  type="password"
                  onChange={handlePasswordChange}
                  className="w-full border rounded-xl px-4 py-3 mt-2"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-700">Confirm Password</label>
                <input
                  name="confirmPassword"
                  value={passwordData.confirmPassword}
                  type="password"
                  onChange={handlePasswordChange}
                  className="w-full border rounded-xl px-4 py-3 mt-2"
                />
              </div>
              <button type="submit" className="bg-primary text-white rounded-2xl px-5 py-3 font-medium hover:bg-pink-600 transition">Update password</button>
            </form>
          </section>
        </div>

        <aside className="space-y-6">
          <div className="bg-white rounded-3xl shadow-sm p-6">
            <h2 className="text-xl font-semibold mb-4">Account Summary</h2>
            <div className="space-y-3 text-sm text-slate-600">
              <p><span className="font-semibold">Name:</span> {user?.name}</p>
              <p><span className="font-semibold">Email:</span> {user?.email}</p>
              <p><span className="font-semibold">Mobile:</span> {user?.mobile}</p>
            </div>
          </div>
          <div className="bg-white rounded-3xl shadow-sm p-6">
            <h3 className="text-xl font-semibold mb-3">Address Management</h3>
            <p className="text-sm text-slate-500">Address management will be available soon.</p>
          </div>
        </aside>
      </div>

      {toast && <Toast message={toast.message} type={toast.type} onClose={() => setToast(null)} />}
    </div>
  );
}
