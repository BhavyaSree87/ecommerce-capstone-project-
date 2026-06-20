import React, { useState, useEffect } from 'react';
import Modal from '../common/Modal';
import AdminButton from '../common/AdminButton';
import FormInput from '../tables/FormInput';
import Alert from '../common/Alert';
import adminService from '../../../services/adminService';

export default function ProductFormModal({ 
  isOpen, 
  onClose, 
  onSubmit, 
  product = null,
  categories = [],
  loading = false,
}) {
  const [formData, setFormData] = useState({
    product_name: '',
    description: '',
    category: '',
    brand: '',
    price: '',
    stock: '',
    rating: '5',
    discount: '0',
    image_url: '',
  });
  const [errors, setErrors] = useState({});
  const [submitError, setSubmitError] = useState('');
  const [modalCategories, setModalCategories] = useState(categories || []);
  const [categoryLoading, setCategoryLoading] = useState(false);
  const [imagePreview, setImagePreview] = useState('');

  useEffect(() => {
    setModalCategories(categories || []);
  }, [categories]);

  useEffect(() => {
    if (!isOpen) return;

    const fetchCategories = async () => {
      setCategoryLoading(true);
      try {
        const response = await adminService.getAllCategories();
        console.log('Categories API response', response);
        setModalCategories(response || []);
      } catch (err) {
        console.error('Failed to fetch categories', err);
      } finally {
        setCategoryLoading(false);
      }
    };

    fetchCategories();
  }, [isOpen]);

  useEffect(() => {
    const initialPayload = {
      product_name: product?.product_name || product?.name || '',
      description: product?.description || '',
      category: product?.category || '',
      brand: product?.brand || '',
      price: product?.price || '',
      stock: product?.stock || '',
      rating: product?.rating || '5',
      discount: product?.discount || '0',
      image_url: product?.image_url || '',
    };

    setFormData(initialPayload);
    setErrors({});
    setSubmitError('');
    setImagePreview(product?.image_url || '');
  }, [product, isOpen]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));

    if (name === 'category') {
      console.log('Selected category', value);
    }

    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }));
    }
  };

  const handleImageChange = (e) => {
    // image URL input change handler
    const { value } = e.target;
    setFormData(prev => ({ ...prev, image_url: value }));
    setImagePreview(value);
  };

  const validateForm = () => {
    const newErrors = {};

    if (!formData.product_name.trim()) newErrors.product_name = 'Product name is required';
    if (!formData.category.trim()) newErrors.category = 'Category is required';
    if (!formData.price || parseFloat(formData.price) <= 0) newErrors.price = 'Valid price is required';
    if (!formData.stock || parseInt(formData.stock) < 0) newErrors.stock = 'Valid stock is required';
    if (!formData.image_url) newErrors.image_url = 'Product image URL is required';
    else {
      // validate URL format
      try {
        // eslint-disable-next-line no-new
        new URL(formData.image_url);
      } catch (e) {
        newErrors.image_url = 'Enter a valid image URL (https://...)';
      }
    }

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
      setSubmitError(error.message || 'Failed to save product');
    }
  };

  const fileInputClasses = 'w-full rounded-lg border border-slate-200 px-4 py-2 focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent';

  return (
    <Modal 
      isOpen={isOpen} 
      title={product ? 'Edit Product' : 'Add New Product'} 
      onClose={onClose}
      size="lg"
    >
      <form onSubmit={handleSubmit} className="space-y-4">
        {submitError && (
          <Alert type="error" message={submitError} onClose={() => setSubmitError('')} />
        )}

        <FormInput
          label="Product Name"
          name="product_name"
          value={formData.product_name}
          onChange={handleChange}
          placeholder="Enter product name"
          required
          error={errors.product_name}
        />

        <FormInput
          label="Brand"
          name="brand"
          value={formData.brand}
          onChange={handleChange}
          placeholder="Enter brand name"
        />

        <FormInput
          label="Description"
          name="description"
          value={formData.description}
          onChange={handleChange}
          placeholder="Enter product description"
          multiline
          rows={4}
        />

        <div className="grid grid-cols-2 gap-4">
          <FormInput
            label="Category"
            type="select"
            name="category"
            value={formData.category}
            onChange={handleChange}
            options={modalCategories}
            required
            disabled={categoryLoading}
            error={errors.category}
          />

          <FormInput
            label="Price (₹)"
            type="number"
            name="price"
            value={formData.price}
            onChange={handleChange}
            placeholder="0.00"
            step="0.01"
            required
            error={errors.price}
          />
        </div>

        <div className="grid grid-cols-3 gap-4">
          <FormInput
            label="Stock"
            type="number"
            name="stock"
            value={formData.stock}
            onChange={handleChange}
            placeholder="0"
            required
            error={errors.stock}
          />

          <FormInput
            label="Rating"
            type="number"
            name="rating"
            value={formData.rating}
            onChange={handleChange}
            min="0"
            max="5"
            step="0.1"
          />

          <FormInput
            label="Discount (%)"
            type="number"
            name="discount"
            value={formData.discount}
            onChange={handleChange}
            min="0"
            max="100"
          />
        </div>

        <div className="mb-4">
            <label className="block text-sm font-medium text-slate-700 mb-2">
              Product Image URL
              <span className="text-red-500">*</span>
            </label>
            <input
              type="url"
              name="image_url"
              value={formData.image_url}
              onChange={handleImageChange}
              placeholder="https://example.com/image.jpg"
              className={fileInputClasses}
            />
            {errors.image_url && <p className="text-red-500 text-sm mt-1">{errors.image_url}</p>}
        </div>

        {imagePreview && (
          <div className="mb-4">
            <p className="text-sm text-slate-600 mb-2">Image Preview</p>
            <img
              src={imagePreview}
              alt="Product preview"
              className="w-full rounded-lg border border-slate-200 object-cover"
              style={{ maxHeight: '320px' }}
            />
          </div>
        )}

        <div className="flex gap-3 justify-end pt-4 border-t border-slate-200">
          <AdminButton variant="outline" onClick={onClose} disabled={loading}>
            Cancel
          </AdminButton>
          <AdminButton variant="primary" type="submit" disabled={loading}>
            {loading ? 'Saving...' : product ? 'Update Product' : 'Add Product'}
          </AdminButton>
        </div>
      </form>
    </Modal>
  );
}
