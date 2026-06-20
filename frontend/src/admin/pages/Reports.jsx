import React, { useEffect, useState } from 'react';
import adminService from '../../services/adminService';
import LoadingSpinner from '../components/common/LoadingSpinner';
import Alert from '../components/common/Alert';

export default function AdminReports() {
  const [orders, setOrders] = useState([]);
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [reportType, setReportType] = useState('sales');
  const [dateRange, setDateRange] = useState('month');

  useEffect(() => {
    fetchReportData();
  }, [reportType, dateRange]);

  const fetchReportData = async () => {
    try {
      setLoading(true);
      setError('');
      
      const [ordersData, productsData] = await Promise.all([
        adminService.getAllOrders(),
        adminService.getAllProducts(),
      ]);
      
      setOrders(ordersData);
      setProducts(productsData);
    } catch (err) {
      setError(err.message || 'Failed to load reports');
    } finally {
      setLoading(false);
    }
  };

  const calculateMetrics = () => {
    if (orders.length === 0) return {};

    const totalRevenue = orders.reduce((sum, order) => sum + (order.total_amount || 0), 0);
    const totalOrders = orders.length;
    const avgOrderValue = totalRevenue / totalOrders;
    const completedOrders = orders.filter(o => o.status === 'Delivered').length;
    const cancelledOrders = orders.filter(o => o.status === 'Cancelled').length;

    return {
      totalRevenue,
      totalOrders,
      avgOrderValue,
      completedOrders,
      cancelledOrders,
      conversionRate: ((completedOrders / totalOrders) * 100).toFixed(2),
    };
  };

  const getTopProducts = () => {
    return products
      .sort((a, b) => (b.rating || 0) - (a.rating || 0))
      .slice(0, 10);
  };

  const getSalesPerDay = () => {
    const salesByDay = {};
    orders.forEach(order => {
      const dateValue = order.order_date || order.created_at || order.createdAt;
      if (dateValue) {
        const date = new Date(dateValue).toLocaleDateString();
        salesByDay[date] = (salesByDay[date] || 0) + (order.total_amount || 0);
      }
    });
    return Object.entries(salesByDay).map(([date, amount]) => ({ date, amount }));
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center py-20">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  const metrics = calculateMetrics();
  const topProducts = getTopProducts();
  const salesData = getSalesPerDay();

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-slate-900">Reports & Analytics</h1>
        <p className="text-slate-500 mt-1">View comprehensive sales and revenue reports</p>
      </div>

      {error && <Alert type="error" message={error} onClose={() => setError('')} />}

      {/* Filters */}
      <div className="flex gap-4 flex-wrap">
        <select
          value={reportType}
          onChange={(e) => setReportType(e.target.value)}
          className="rounded-lg border border-slate-200 px-4 py-2 focus:outline-none focus:ring-2 focus:ring-primary"
        >
          <option value="sales">Sales Report</option>
          <option value="revenue">Revenue Report</option>
          <option value="products">Product Report</option>
        </select>
        
        <select
          value={dateRange}
          onChange={(e) => setDateRange(e.target.value)}
          className="rounded-lg border border-slate-200 px-4 py-2 focus:outline-none focus:ring-2 focus:ring-primary"
        >
          <option value="week">Last 7 Days</option>
          <option value="month">Last 30 Days</option>
          <option value="year">Last Year</option>
          <option value="all">All Time</option>
        </select>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="rounded-2xl border border-slate-200 bg-white p-6">
          <p className="text-sm text-slate-500">Total Revenue</p>
          <p className="text-3xl font-bold text-emerald-600 mt-2">
            ₹{(metrics.totalRevenue || 0).toLocaleString()}
          </p>
        </div>
        
        <div className="rounded-2xl border border-slate-200 bg-white p-6">
          <p className="text-sm text-slate-500">Total Orders</p>
          <p className="text-3xl font-bold text-blue-600 mt-2">{metrics.totalOrders || 0}</p>
        </div>
        
        <div className="rounded-2xl border border-slate-200 bg-white p-6">
          <p className="text-sm text-slate-500">Avg Order Value</p>
          <p className="text-3xl font-bold text-purple-600 mt-2">
            ₹{Math.round(metrics.avgOrderValue || 0).toLocaleString()}
          </p>
        </div>
        
        <div className="rounded-2xl border border-slate-200 bg-white p-6">
          <p className="text-sm text-slate-500">Completion Rate</p>
          <p className="text-3xl font-bold text-orange-600 mt-2">{metrics.conversionRate || 0}%</p>
        </div>
      </div>

      {/* Order Status Breakdown */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="rounded-2xl border border-slate-200 bg-white p-6">
          <p className="text-sm font-medium text-slate-600">Completed Orders</p>
          <p className="text-2xl font-bold text-emerald-600 mt-2">{metrics.completedOrders || 0}</p>
        </div>
        
        <div className="rounded-2xl border border-slate-200 bg-white p-6">
          <p className="text-sm font-medium text-slate-600">Cancelled Orders</p>
          <p className="text-2xl font-bold text-red-600 mt-2">{metrics.cancelledOrders || 0}</p>
        </div>
        
        <div className="rounded-2xl border border-slate-200 bg-white p-6">
          <p className="text-sm font-medium text-slate-600">Pending/Processing</p>
          <p className="text-2xl font-bold text-blue-600 mt-2">
            {(metrics.totalOrders || 0) - (metrics.completedOrders || 0) - (metrics.cancelledOrders || 0)}
          </p>
        </div>
      </div>

      {/* Top Products */}
      <div className="rounded-2xl border border-slate-200 bg-white p-6">
        <h2 className="text-lg font-semibold text-slate-900 mb-4">Top 10 Products by Rating</h2>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead className="border-b border-slate-200">
              <tr>
                <th className="text-left font-medium text-slate-600 py-2">Product</th>
                <th className="text-center font-medium text-slate-600 py-2">Price</th>
                <th className="text-center font-medium text-slate-600 py-2">Rating</th>
                <th className="text-right font-medium text-slate-600 py-2">Stock</th>
              </tr>
            </thead>
            <tbody>
              {topProducts.map((product) => (
                <tr key={product.id} className="border-b border-slate-100 hover:bg-slate-50">
                  <td className="py-3 text-slate-700">{product.product_name || product.name}</td>
                  <td className="text-center py-3">₹{product.price}</td>
                  <td className="text-center py-3 font-semibold">{product.rating || 0}</td>
                  <td className="text-right py-3 text-slate-600">{product.stock || 0} units</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Recent Sales Activity */}
      <div className="rounded-2xl border border-slate-200 bg-white p-6">
        <h2 className="text-lg font-semibold text-slate-900 mb-4">Recent Sales Activity</h2>
        <div className="space-y-2">
          {salesData.slice(-10).reverse().map((entry, idx) => (
            <div key={idx} className="flex items-center justify-between p-3 rounded-lg border border-slate-100">
              <p className="text-sm text-slate-700">{entry.date}</p>
              <p className="text-sm font-semibold text-emerald-600">₹{entry.amount.toLocaleString()}</p>
            </div>
          ))}
          {salesData.length === 0 && (
            <p className="text-center text-slate-500 py-8">No sales data available</p>
          )}
        </div>
      </div>
    </div>
  );
}
