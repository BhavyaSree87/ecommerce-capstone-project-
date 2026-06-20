import React, { useEffect, useState } from 'react';
import adminService from '../../services/adminService';
import LoadingSpinner from '../components/common/LoadingSpinner';
import Alert from '../components/common/Alert';

export default function AdminPayments() {
  const [payments, setPayments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(() => {
    fetchPayments();
  }, []);

  const fetchPayments = async () => {
    try {
      setLoading(true);
      setError('');
      // Using orders API to show payment history
      const orders = await adminService.getAllOrders();
      const paymentsData = orders.map(order => ({
        id: order.id,
        orderId: order.id,
        amount: order.total_amount,
        method: 'Card/Digital',
        status: order.status,
        date: order.order_date || order.created_at || order.createdAt,
      }));
      setPayments(paymentsData);
    } catch (err) {
      setError(err.message || 'Failed to load payments');
    } finally {
      setLoading(false);
    }
  };

  const filteredPayments = payments.filter(payment => {
    const searchLower = searchQuery.toLowerCase();
    return (
      payment.id.toString().includes(searchLower) ||
      payment.method.toLowerCase().includes(searchLower)
    );
  });

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
        <h1 className="text-3xl font-bold text-slate-900">Payment Management</h1>
        <p className="text-slate-500 mt-1">{filteredPayments.length} payments total</p>
      </div>

      {error && <Alert type="error" message={error} onClose={() => setError('')} />}

      {/* Search */}
      <div>
        <input
          type="text"
          placeholder="Search by Payment ID or method..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="w-full rounded-lg border border-slate-200 px-4 py-2 focus:outline-none focus:ring-2 focus:ring-primary"
        />
      </div>

      {/* Payment Table */}
      <div className="rounded-2xl border border-slate-200 bg-white shadow-sm overflow-hidden">
        <table className="w-full">
          <thead className="border-b border-slate-200 bg-slate-50">
            <tr>
              <th className="text-left font-semibold text-slate-900 px-6 py-3">Payment ID</th>
              <th className="text-left font-semibold text-slate-900 px-6 py-3">Order ID</th>
              <th className="text-left font-semibold text-slate-900 px-6 py-3">Amount</th>
              <th className="text-left font-semibold text-slate-900 px-6 py-3">Method</th>
              <th className="text-left font-semibold text-slate-900 px-6 py-3">Status</th>
              <th className="text-left font-semibold text-slate-900 px-6 py-3">Date</th>
            </tr>
          </thead>
          <tbody>
            {filteredPayments.map((payment) => (
              <tr key={payment.id} className="border-b border-slate-100 hover:bg-slate-50">
                <td className="px-6 py-4 text-sm text-slate-700">#{payment.id}</td>
                <td className="px-6 py-4 text-sm text-slate-700">#{payment.orderId}</td>
                <td className="px-6 py-4 text-sm font-semibold text-slate-900">₹{(payment.amount || 0).toLocaleString()}</td>
                <td className="px-6 py-4 text-sm text-slate-700">{payment.method}</td>
                <td className="px-6 py-4 text-sm">
                  <span className={`px-3 py-1 rounded-full text-xs font-medium ${
                    payment.status === 'Delivered' ? 'bg-emerald-100 text-emerald-700' :
                    payment.status === 'Cancelled' ? 'bg-red-100 text-red-700' :
                    'bg-blue-100 text-blue-700'
                  }`}>
                    {payment.status || 'Pending'}
                  </span>
                </td>
                <td className="px-6 py-4 text-sm text-slate-700">
                  {payment.date ? new Date(payment.date).toLocaleDateString() : '-'}
                </td>
              </tr>
            ))}
            {filteredPayments.length === 0 && (
              <tr>
                <td colSpan="6" className="px-6 py-8 text-center text-slate-500">
                  No payments found
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="rounded-2xl border border-slate-200 bg-white p-6">
          <p className="text-sm text-slate-500">Total Transactions</p>
          <p className="text-3xl font-bold text-slate-900 mt-2">{payments.length}</p>
        </div>
        
        <div className="rounded-2xl border border-slate-200 bg-white p-6">
          <p className="text-sm text-slate-500">Total Revenue</p>
          <p className="text-3xl font-bold text-emerald-600 mt-2">
            ₹{payments.reduce((sum, p) => sum + (p.amount || 0), 0).toLocaleString()}
          </p>
        </div>
        
        <div className="rounded-2xl border border-slate-200 bg-white p-6">
          <p className="text-sm text-slate-500">Avg Transaction</p>
          <p className="text-3xl font-bold text-slate-900 mt-2">
            ₹{payments.length > 0 ? Math.round(payments.reduce((sum, p) => sum + (p.amount || 0), 0) / payments.length).toLocaleString() : 0}
          </p>
        </div>
      </div>
    </div>
  );
}
