import React, { useContext, useState } from 'react';
import { AuthContext } from '../../context/AuthContext';
import AdminButton from '../components/common/AdminButton';
import Alert from '../components/common/Alert';

export default function AdminSettings() {
  const { user } = useContext(AuthContext);
  const [successMessage, setSuccessMessage] = useState('');
  const [settings, setSettings] = useState({
    siteName: 'StyleHub',
    siteDescription: 'Premium Fashion and Lifestyle E-Commerce Platform',
    adminEmail: user?.email || '',
    currency: 'INR',
    taxRate: '18',
    shippingCost: '50',
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setSettings(prev => ({ ...prev, [name]: value }));
  };

  const handleSave = () => {
    setSuccessMessage('Settings saved successfully');
    setTimeout(() => setSuccessMessage(''), 3000);
    console.log('Settings saved:', settings);
  };

  return (
    <div className="space-y-6 max-w-2xl">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-slate-900">Admin Settings</h1>
        <p className="text-slate-500 mt-1">Configure your admin panel and store settings</p>
      </div>

      {successMessage && <Alert type="success" message={successMessage} />}

      {/* General Settings */}
      <div className="rounded-2xl border border-slate-200 bg-white p-6">
        <h2 className="text-lg font-semibold text-slate-900 mb-4">General Settings</h2>
        
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-2">Site Name</label>
            <input
              type="text"
              name="siteName"
              value={settings.siteName}
              onChange={handleChange}
              className="w-full rounded-lg border border-slate-200 px-4 py-2 focus:outline-none focus:ring-2 focus:ring-primary"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-700 mb-2">Site Description</label>
            <textarea
              name="siteDescription"
              value={settings.siteDescription}
              onChange={handleChange}
              rows="3"
              className="w-full rounded-lg border border-slate-200 px-4 py-2 focus:outline-none focus:ring-2 focus:ring-primary"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-700 mb-2">Admin Email</label>
            <input
              type="email"
              name="adminEmail"
              value={settings.adminEmail}
              onChange={handleChange}
              className="w-full rounded-lg border border-slate-200 px-4 py-2 focus:outline-none focus:ring-2 focus:ring-primary"
            />
          </div>
        </div>
      </div>

      {/* Business Settings */}
      <div className="rounded-2xl border border-slate-200 bg-white p-6">
        <h2 className="text-lg font-semibold text-slate-900 mb-4">Business Settings</h2>
        
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-2">Currency</label>
            <select
              name="currency"
              value={settings.currency}
              onChange={handleChange}
              className="w-full rounded-lg border border-slate-200 px-4 py-2 focus:outline-none focus:ring-2 focus:ring-primary"
            >
              <option value="INR">Indian Rupee (₹)</option>
              <option value="USD">US Dollar ($)</option>
              <option value="EUR">Euro (€)</option>
              <option value="GBP">British Pound (£)</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-700 mb-2">Tax Rate (%)</label>
            <input
              type="number"
              name="taxRate"
              value={settings.taxRate}
              onChange={handleChange}
              min="0"
              max="100"
              step="0.01"
              className="w-full rounded-lg border border-slate-200 px-4 py-2 focus:outline-none focus:ring-2 focus:ring-primary"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-700 mb-2">Shipping Cost (₹)</label>
            <input
              type="number"
              name="shippingCost"
              value={settings.shippingCost}
              onChange={handleChange}
              min="0"
              className="w-full rounded-lg border border-slate-200 px-4 py-2 focus:outline-none focus:ring-2 focus:ring-primary"
            />
          </div>
        </div>
      </div>

      {/* Admin Profile */}
      <div className="rounded-2xl border border-slate-200 bg-white p-6">
        <h2 className="text-lg font-semibold text-slate-900 mb-4">Admin Profile</h2>
        
        <div className="space-y-3">
          <div className="flex items-center justify-between p-3 rounded-lg bg-slate-50">
            <p className="text-sm text-slate-600">Admin Name</p>
            <p className="text-sm font-medium text-slate-900">{user?.name || 'Admin'}</p>
          </div>
          
          <div className="flex items-center justify-between p-3 rounded-lg bg-slate-50">
            <p className="text-sm text-slate-600">Email</p>
            <p className="text-sm font-medium text-slate-900">{user?.email || 'N/A'}</p>
          </div>
          
          <div className="flex items-center justify-between p-3 rounded-lg bg-slate-50">
            <p className="text-sm text-slate-600">Role</p>
            <p className="text-sm font-medium text-slate-900">Administrator</p>
          </div>
        </div>
      </div>

      {/* Action Buttons */}
      <div className="flex gap-4">
        <AdminButton variant="primary" onClick={handleSave}>
          Save Settings
        </AdminButton>
        <AdminButton variant="outline">
          Reset to Defaults
        </AdminButton>
      </div>
    </div>
  );
}
