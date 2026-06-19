import React, { useEffect, useState } from 'react';
import adminService from '../../services/adminService';
import DataTable from '../components/tables/DataTable';
import CategoryFormModal from '../components/modals/CategoryFormModal';
import AdminButton from '../components/common/AdminButton';
import LoadingSpinner from '../components/common/LoadingSpinner';
import Alert from '../components/common/Alert';

export default function AdminCategories() {
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');
  const [successMessage, setSuccessMessage] = useState('');
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedCategory, setSelectedCategory] = useState(null);

  useEffect(() => {
    fetchCategories();
  }, []);

  const fetchCategories = async () => {
    try {
      setLoading(true);
      setError('');
      const data = await adminService.getAllCategories();
      setCategories(data);
    } catch (err) {
      setError(err.message || 'Failed to load categories');
    } finally {
      setLoading(false);
    }
  };

  const handleAddCategory = () => {
    setSelectedCategory(null);
    setIsModalOpen(true);
  };

  const handleEditCategory = (category) => {
    setSelectedCategory(category);
    setIsModalOpen(true);
  };

  const handleDeleteCategory = async (id) => {
    try {
      setError('');
      await adminService.deleteCategory(id);
      setCategories(categories.filter(c => c.id !== id));
      setSuccessMessage('Category deleted successfully');
      setTimeout(() => setSuccessMessage(''), 3000);
    } catch (err) {
      setError(err.message || 'Failed to delete category');
    }
  };

  const handleSubmitCategory = async (formData) => {
    try {
      setSubmitting(true);
      setError('');
      
      if (selectedCategory) {
        await adminService.updateCategory(selectedCategory.id, formData);
        setCategories(categories.map(c => c.id === selectedCategory.id ? { ...c, ...formData } : c));
        setSuccessMessage('Category updated successfully');
      } else {
        const newCategory = await adminService.createCategory(formData);
        setCategories([...categories, newCategory]);
        setSuccessMessage('Category created successfully');
      }
      
      setTimeout(() => setSuccessMessage(''), 3000);
    } catch (err) {
      setError(err.message || 'Failed to save category');
      throw err;
    } finally {
      setSubmitting(false);
    }
  };

  const columns = [
    {
      key: 'category_name',
      label: 'Category Name',
      render: (value, row) => row.category_name || row.name || '-',
    },
    {
      key: 'description',
      label: 'Description',
      render: (value) => value || '-',
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
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold text-slate-900">Categories Management</h1>
          <p className="text-slate-500 mt-1">{categories.length} categories</p>
        </div>
        <AdminButton variant="primary" onClick={handleAddCategory}>
          + Add Category
        </AdminButton>
      </div>

      {error && <Alert type="error" message={error} onClose={() => setError('')} />}
      {successMessage && <Alert type="success" message={successMessage} />}

      {/* Table */}
      <DataTable
        columns={columns}
        data={categories}
        onEdit={handleEditCategory}
        onDelete={handleDeleteCategory}
        loading={loading}
        emptyMessage="No categories found. Create your first category."
      />

      {/* Modal */}
      <CategoryFormModal
        isOpen={isModalOpen}
        onClose={() => {
          setIsModalOpen(false);
          setSelectedCategory(null);
        }}
        onSubmit={handleSubmitCategory}
        category={selectedCategory}
        loading={submitting}
      />
    </div>
  );
}
