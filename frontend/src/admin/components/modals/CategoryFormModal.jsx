import React, { useState, useEffect } from 'react';
import Modal from '../common/Modal';
import AdminButton from '../common/AdminButton';
import FormInput from '../tables/FormInput';
import Alert from '../common/Alert';

export default function CategoryFormModal({ 
  isOpen, 
  onClose, 
  onSubmit, 
  category = null,
  loading = false,
}) {
  const [formData, setFormData] = useState({
    category_name: '',
    description: '',
  });
  
  const [errors, setErrors] = useState({});
  const [submitError, setSubmitError] = useState('');

  useEffect(() => {
    if (category) {
      setFormData({
        category_name: category.category_name || category.name || '',
        description: category.description || '',
      });
    } else {
      setFormData({
        category_name: '',
        description: '',
      });
    }
    setErrors({});
    setSubmitError('');
  }, [category, isOpen]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }));
    }
  };

  const validateForm = () => {
    const newErrors = {};
    
    if (!formData.category_name.trim()) newErrors.category_name = 'Category name is required';
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateForm()) return;
    
    try {
      setSubmitError('');
      await onSubmit(formData);
      onClose();
    } catch (error) {
      setSubmitError(error.message || 'Failed to save category');
    }
  };

  return (
    <Modal 
      isOpen={isOpen} 
      title={category ? 'Edit Category' : 'Add New Category'} 
      onClose={onClose}
      size="md"
    >
      <form onSubmit={handleSubmit} className="space-y-4">
        {submitError && (
          <Alert type="error" message={submitError} onClose={() => setSubmitError('')} />
        )}
        
        <FormInput
          label="Category Name"
          name="category_name"
          value={formData.category_name}
          onChange={handleChange}
          placeholder="Enter category name"
          required
          error={errors.category_name}
        />
        
        <FormInput
          label="Description"
          name="description"
          value={formData.description}
          onChange={handleChange}
          placeholder="Enter category description"
          multiline
          rows={4}
        />
        
        <div className="flex gap-3 justify-end pt-4 border-t border-slate-200">
          <AdminButton variant="outline" onClick={onClose} disabled={loading}>
            Cancel
          </AdminButton>
          <AdminButton variant="primary" type="submit" disabled={loading}>
            {loading ? 'Saving...' : category ? 'Update Category' : 'Add Category'}
          </AdminButton>
        </div>
      </form>
    </Modal>
  );
}
