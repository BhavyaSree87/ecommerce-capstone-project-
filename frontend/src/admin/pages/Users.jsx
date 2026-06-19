import React, { useEffect, useState } from 'react';
import adminService from '../../services/adminService';
import DataTable from '../components/tables/DataTable';
import LoadingSpinner from '../components/common/LoadingSpinner';
import Alert from '../components/common/Alert';

export default function AdminUsers() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [successMessage, setSuccessMessage] = useState('');
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    try {
      setLoading(true);
      setError('');
      const data = await adminService.getAllUsers();
      setUsers(data);
    } catch (err) {
      setError(err.message || 'Failed to load users');
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteUser = async (id) => {
    if (!window.confirm('Are you sure you want to delete this user? This action cannot be undone.')) {
      return;
    }

    try {
      setError('');
      await adminService.deleteUser(id);
      setUsers(users.filter(u => u.id !== id));
      setSuccessMessage('User deleted successfully');
      setTimeout(() => setSuccessMessage(''), 3000);
    } catch (err) {
      setError(err.message || 'Failed to delete user');
    }
  };

  const filteredUsers = users.filter(user => {
    const searchLower = searchQuery.toLowerCase();
    return (
      (user.username || '').toLowerCase().includes(searchLower) ||
      (user.email || '').toLowerCase().includes(searchLower) ||
      (user.first_name || '').toLowerCase().includes(searchLower) ||
      (user.last_name || '').toLowerCase().includes(searchLower)
    );
  });

  const columns = [
    {
      key: 'username',
      label: 'Username',
    },
    {
      key: 'email',
      label: 'Email',
    },
    {
      key: 'first_name',
      label: 'First Name',
      render: (value) => value || '-',
    },
    {
      key: 'last_name',
      label: 'Last Name',
      render: (value) => value || '-',
    },
    {
      key: 'created_at',
      label: 'Joined Date',
      render: (value) => {
        if (!value) return '-';
        const date = new Date(value);
        return date.toLocaleDateString();
      },
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
        <h1 className="text-3xl font-bold text-slate-900">Users Management</h1>
        <p className="text-slate-500 mt-1">{filteredUsers.length} users found</p>
      </div>

      {error && <Alert type="error" message={error} onClose={() => setError('')} />}
      {successMessage && <Alert type="success" message={successMessage} />}

      {/* Search */}
      <div>
        <input
          type="text"
          placeholder="Search by username, email, or name..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="w-full rounded-lg border border-slate-200 px-4 py-2 focus:outline-none focus:ring-2 focus:ring-primary"
        />
      </div>

      {/* Table */}
      <DataTable
        columns={columns}
        data={filteredUsers}
        onDelete={handleDeleteUser}
        hideEdit
        loading={loading}
        emptyMessage="No users found."
        deleteButtonLabel="Remove"
      />

      {/* Stats */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="rounded-2xl border border-slate-200 bg-white p-6">
          <p className="text-sm text-slate-500">Total Users</p>
          <p className="text-3xl font-bold text-slate-900 mt-2">{users.length}</p>
        </div>
        
        <div className="rounded-2xl border border-slate-200 bg-white p-6">
          <p className="text-sm text-slate-500">Unique Emails</p>
          <p className="text-3xl font-bold text-slate-900 mt-2">
            {new Set(users.map(u => u.email)).size}
          </p>
        </div>
        
        <div className="rounded-2xl border border-slate-200 bg-white p-6">
          <p className="text-sm text-slate-500">Profile Completion</p>
          <p className="text-3xl font-bold text-slate-900 mt-2">
            {Math.round((users.filter(u => u.first_name && u.last_name).length / users.length * 100) || 0)}%
          </p>
        </div>
      </div>
    </div>
  );
}
