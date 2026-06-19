import React, { useEffect, useState } from 'react';
import adminService from '../../services/adminService';
import LoadingSpinner from '../components/common/LoadingSpinner';
import Alert from '../components/common/Alert';

export default function AdminDashboard() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const safeArray = (value) => {
      if (Array.isArray(value)) return value;
      if (value?.items && Array.isArray(value.items)) return value.items;
      return [];
    };

    const normalizeOrder = (order) => {
      if (Array.isArray(order)) {
        return {
          id: order[0],
          item_id: order[1],
          product_id: order[2],
          quantity: order[3],
          price: order[4],
          status: order[5],
          user_id: order[6],
          created_at: order[7],
          total_amount: order[3] * order[4],
        };
      }
      return order;
    };

    const fetchStats = async () => {
      try {
        setLoading(true);
        setError('');

        const dashboardStats = await adminService.getDashboardStats();
        const products = safeArray(await adminService.getAllProducts());
        const categories = safeArray(await adminService.getAllCategories());
        const orders = safeArray(await adminService.getAllOrders()).map(normalizeOrder);
        const users = safeArray(await adminService.getAllUsers());

        const totalRevenue = orders.reduce((sum, order) => sum + (order.total_amount || 0), 0);
        const recentOrders = orders.slice(0, 5);
        const topProducts = products
          .slice()
          .sort((a, b) => (b.rating || 0) - (a.rating || 0))
          .slice(0, 5);

        setStats({
          totalProducts: dashboardStats?.total_products ?? products.length,
          totalCategories: categories.length,
          totalOrders: dashboardStats?.total_orders ?? orders.length,
          totalUsers: dashboardStats?.total_users ?? users.length,
          totalRevenue: dashboardStats?.total_revenue ?? totalRevenue,
          recentOrders,
          topProducts,
        });
      } catch (err) {
        setError(err.message || 'Failed to load dashboard stats');
        setStats({
          totalProducts: 0,
          totalCategories: 0,
          totalOrders: 0,
          totalUsers: 0,
          totalRevenue: 0,
          recentOrders: [],
          topProducts: [],
        });
      } finally {
        setLoading(false);
      }
    };

    fetchStats();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center py-20">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-slate-900">Dashboard</h1>
        <p className="text-slate-500 mt-1">Welcome to your admin panel</p>
      </div>

      {error && <Alert type="error" message={error} />}

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-5 gap-4">
        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm hover:shadow-md transition">
          <p className="text-sm text-slate-500">Total Products</p>
          <p className="text-3xl font-bold text-slate-900 mt-4">{stats?.totalProducts || 0}</p>
        </div>

        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm hover:shadow-md transition">
          <p className="text-sm text-slate-500">Categories</p>
          <p className="text-3xl font-bold text-slate-900 mt-4">{stats?.totalCategories || 0}</p>
        </div>

        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm hover:shadow-md transition">
          <p className="text-sm text-slate-500">Total Orders</p>
          <p className="text-3xl font-bold text-slate-900 mt-4">{stats?.totalOrders || 0}</p>
        </div>

        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm hover:shadow-md transition">
          <p className="text-sm text-slate-500">Total Users</p>
          <p className="text-3xl font-bold text-slate-900 mt-4">{stats?.totalUsers || 0}</p>
        </div>

        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm hover:shadow-md transition">
          <p className="text-sm text-slate-500">Total Revenue</p>
          <p className="text-3xl font-bold text-rose-600 mt-4">₹{(stats?.totalRevenue || 0).toLocaleString()}</p>
        </div>
      </div>

      {/* Recent Orders and Top Products */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Recent Orders */}
        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
          <h2 className="text-lg font-semibold text-slate-900 mb-4">Recent Orders</h2>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-slate-200">
                  <th className="text-left font-medium text-slate-600 py-2">Order ID</th>
                  <th className="text-left font-medium text-slate-600 py-2">Status</th>
                  <th className="text-right font-medium text-slate-600 py-2">Amount</th>
                </tr>
              </thead>
              <tbody>
                {stats?.recentOrders.map((order) => (
                  <tr key={order.id} className="border-b border-slate-100 hover:bg-slate-50">
                    <td className="py-3">#{order.id}</td>
                    <td className="py-3">
                      <span className={`px-3 py-1 rounded-full text-xs font-medium ${
                        order.status === 'Delivered' ? 'bg-emerald-100 text-emerald-700' :
                        order.status === 'Cancelled' ? 'bg-red-100 text-red-700' :
                        'bg-blue-100 text-blue-700'
                      }`}>
                        {order.status || 'Pending'}
                      </span>
                    </td>
                    <td className="text-right py-3">₹{(order.total_amount || 0).toLocaleString()}</td>
                  </tr>
                ))}
                {(!stats?.recentOrders || stats.recentOrders.length === 0) && (
                  <tr>
                    <td colSpan="3" className="py-8 text-center text-slate-500">
                      No recent orders
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>

        {/* Top Selling Products */}
        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
          <h2 className="text-lg font-semibold text-slate-900 mb-4">Top Products</h2>
          <div className="space-y-3">
            {stats?.topProducts.map((product) => (
              <div key={product.id} className="flex items-center justify-between p-3 rounded-lg border border-slate-100 hover:bg-slate-50">
                <div className="flex-1 min-w-0">
                  <p className="font-medium text-slate-900 truncate">{product.product_name || product.name}</p>
                  <p className="text-xs text-slate-500">₹{product.price}</p>
                </div>
                <div className="flex items-center gap-4 ml-2">
                  <span className="text-sm font-semibold text-slate-700">{product.rating || 0}</span>
                </div>
              </div>
            ))}
            {(!stats?.topProducts || stats.topProducts.length === 0) && (
              <p className="text-center text-slate-500 py-8">No products yet</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
