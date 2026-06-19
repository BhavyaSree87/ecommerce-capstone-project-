import React, { useEffect, useState } from 'react';
import adminService from '../../services/adminService';
import DataTable from '../components/tables/DataTable';
import Modal from '../components/common/Modal';
import AdminButton from '../components/common/AdminButton';
import LoadingSpinner from '../components/common/LoadingSpinner';
import Alert from '../components/common/Alert';

export default function AdminOrders() {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');
  const [successMessage, setSuccessMessage] = useState('');
  const [isStatusModalOpen, setIsStatusModalOpen] = useState(false);
  const [selectedOrder, setSelectedOrder] = useState(null);
  const [newStatus, setNewStatus] = useState('');

  const statuses = ['Pending', 'Processing', 'Shipped', 'Delivered', 'Cancelled'];

  useEffect(() => {
    fetchOrders();
  }, []);

  const fetchOrders = async () => {
    try {
      setLoading(true);
      setError('');
      const data = await adminService.getAllOrders();
      setOrders(data);
    } catch (err) {
      setError(err.message || 'Failed to load orders');
    } finally {
      setLoading(false);
    }
  };

  const handleUpdateStatus = (order) => {
    setSelectedOrder(order);
    setNewStatus(order.status || 'Pending');
    setIsStatusModalOpen(true);
  };

  const handleSubmitStatusChange = async () => {
    try {
      setSubmitting(true);
      setError('');
      
      await adminService.updateOrderStatus(selectedOrder.id, newStatus);
      setOrders(orders.map(o => o.id === selectedOrder.id ? { ...o, status: newStatus } : o));
      setSuccessMessage('Order status updated successfully');
      setIsStatusModalOpen(false);
      setTimeout(() => setSuccessMessage(''), 3000);
    } catch (err) {
      setError(err.message || 'Failed to update order status');
    } finally {
      setSubmitting(false);
    }
  };

  const columns = [
    {
      key: 'id',
      label: 'Order ID',
      render: (value) => `#${value}`,
    },
    {
      key: 'user_id',
      label: 'User ID',
    },
    {
      key: 'order_date',
      label: 'Date',
      render: (value) => {
        if (!value) return '-';
        const date = new Date(value);
        return date.toLocaleDateString();
      },
    },
    {
      key: 'status',
      label: 'Status',
      render: (value) => (
        <span className={`px-3 py-1 rounded-full text-xs font-medium ${
          value === 'Delivered' ? 'bg-emerald-100 text-emerald-700' :
          value === 'Cancelled' ? 'bg-red-100 text-red-700' :
          value === 'Shipped' ? 'bg-blue-100 text-blue-700' :
          value === 'Processing' ? 'bg-orange-100 text-orange-700' :
          'bg-slate-100 text-slate-700'
        }`}>
          {value || 'Pending'}
        </span>
      ),
    },
    {
      key: 'total_amount',
      label: 'Total Amount',
      render: (value) => `₹${(value || 0).toLocaleString()}`,
    },
  ];

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
        <h1 className="text-3xl font-bold text-slate-900">Orders Management</h1>
        <p className="text-slate-500 mt-1">{orders.length} orders total</p>
      </div>

      {error && <Alert type="error" message={error} onClose={() => setError('')} />}
      {successMessage && <Alert type="success" message={successMessage} />}

      {/* Status Filter Cards */}
      <div className="grid grid-cols-2 sm:grid-cols-5 gap-3">
        {statuses.map(status => {
          const count = orders.filter(o => (o.status || 'Pending') === status).length;
          return (
            <div key={status} className="rounded-lg border border-slate-200 bg-white p-3 text-center">
              <p className="text-2xl font-bold text-slate-900">{count}</p>
              <p className="text-xs text-slate-500">{status}</p>
            </div>
          );
        })}
      </div>

      {/* Table */}
      <DataTable
        columns={columns}
        data={orders}
        onEdit={(order) => {
          setSelectedOrder(order);
          setNewStatus(order.status || 'Pending');
          setIsStatusModalOpen(true);
        }}
        hideDelete
        loading={loading}
        emptyMessage="No orders found yet."
        editButtonLabel="Update Status"
      />

      {/* Status Update Modal */}
      {selectedOrder && (
        <Modal
          isOpen={isStatusModalOpen}
          title="Update Order Status"
          onClose={() => setIsStatusModalOpen(false)}
          size="md"
        >
          <div className="space-y-4">
            <div>
              <p className="text-sm font-medium text-slate-600">Order #{selectedOrder.id}</p>
              <p className="text-xs text-slate-500 mt-1">₹{(selectedOrder.total_amount || 0).toLocaleString()}</p>
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">
                New Status
              </label>
              <select
                value={newStatus}
                onChange={(e) => setNewStatus(e.target.value)}
                className="w-full rounded-lg border border-slate-200 px-4 py-2 focus:outline-none focus:ring-2 focus:ring-primary"
              >
                {statuses.map(status => (
                  <option key={status} value={status}>
                    {status}
                  </option>
                ))}
              </select>
            </div>

            <div className="flex gap-3 justify-end pt-4 border-t border-slate-200">
              <AdminButton 
                variant="outline" 
                onClick={() => setIsStatusModalOpen(false)}
                disabled={submitting}
              >
                Cancel
              </AdminButton>
              <AdminButton 
                variant="primary" 
                onClick={handleSubmitStatusChange}
                disabled={submitting}
              >
                {submitting ? 'Updating...' : 'Update Status'}
              </AdminButton>
            </div>
          </div>
        </Modal>
      )}
    </div>
  );
}
