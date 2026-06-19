import React, { useEffect, useState } from 'react';
import adminService from '../../services/adminService';
import DataTable from '../components/tables/DataTable';
import ProductFormModal from '../components/modals/ProductFormModal';
import AdminButton from '../components/common/AdminButton';
import LoadingSpinner from '../components/common/LoadingSpinner';
import Alert from '../components/common/Alert';

export default function AdminProducts() {
  const [products, setProducts] = useState([]);
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');
  const [successMessage, setSuccessMessage] = useState('');
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('');
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedProduct, setSelectedProduct] = useState(null);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      setError('');
      
      const [productsData, categoriesData] = await Promise.all([
        adminService.getAllProducts(),
        adminService.getAllCategories(),
      ]);
      
      setProducts(productsData);
      setCategories(categoriesData);
    } catch (err) {
      setError(err.message || 'Failed to load products');
    } finally {
      setLoading(false);
    }
  };

  const filteredProducts = products.filter(product => {
    const matchesSearch = (product.product_name || product.name || '')
      .toLowerCase()
      .includes(searchQuery.toLowerCase());
    const matchesCategory = !selectedCategory || product.category === selectedCategory;
    return matchesSearch && matchesCategory;
  });

  const handleAddProduct = () => {
    setSelectedProduct(null);
    setIsModalOpen(true);
  };

  const handleEditProduct = (product) => {
    setSelectedProduct(product);
    setIsModalOpen(true);
  };

  const handleDeleteProduct = async (id) => {
    try {
      setError('');
      await adminService.deleteProduct(id);
      setProducts(products.filter(p => p.id !== id));
      setSuccessMessage('Product deleted successfully');
      setTimeout(() => setSuccessMessage(''), 3000);
    } catch (err) {
      setError(err.message || 'Failed to delete product');
    }
  };

  const handleSubmitProduct = async (formData) => {
    try {
      setSubmitting(true);
      setError('');
      
      if (selectedProduct) {
        await adminService.updateProduct(selectedProduct.id, formData);
        setProducts(products.map(p => p.id === selectedProduct.id ? { ...p, ...formData } : p));
        setSuccessMessage('Product updated successfully');
      } else {
        const newProduct = await adminService.createProduct(formData);
        setProducts([...products, newProduct]);
        setSuccessMessage('Product created successfully');
      }
      
      setTimeout(() => setSuccessMessage(''), 3000);
    } catch (err) {
      setError(err.message || 'Failed to save product');
      throw err;
    } finally {
      setSubmitting(false);
    }
  };

  const columns = [
    {
      key: 'product_name',
      label: 'Product Name',
      render: (value, row) => row.product_name || row.name || '-',
    },
    {
      key: 'category',
      label: 'Category',
    },
    {
      key: 'brand',
      label: 'Brand',
    },
    {
      key: 'price',
      label: 'Price',
      render: (value) => `₹${value || 0}`,
    },
    {
      key: 'stock',
      label: 'Stock',
    },
    {
      key: 'rating',
      label: 'Rating',
      render: (value) => value || 0,
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
          <h1 className="text-3xl font-bold text-slate-900">Products Management</h1>
          <p className="text-slate-500 mt-1">{filteredProducts.length} products found</p>
        </div>
        <AdminButton variant="primary" onClick={handleAddProduct}>
          + Add Product
        </AdminButton>
      </div>

      {error && <Alert type="error" message={error} onClose={() => setError('')} />}
      {successMessage && <Alert type="success" message={successMessage} />}

      {/* Filters */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <input
          type="text"
          placeholder="Search products..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="rounded-lg border border-slate-200 px-4 py-2 focus:outline-none focus:ring-2 focus:ring-primary"
        />
        
        <select
          value={selectedCategory}
          onChange={(e) => setSelectedCategory(e.target.value)}
          className="rounded-lg border border-slate-200 px-4 py-2 focus:outline-none focus:ring-2 focus:ring-primary"
        >
          <option value="">All Categories</option>
          {categories.map(cat => (
            <option key={cat.id} value={cat.category_name || cat.name}>
              {cat.category_name || cat.name}
            </option>
          ))}
        </select>
      </div>

      {/* Table */}
      <DataTable
        columns={columns}
        data={filteredProducts}
        onEdit={handleEditProduct}
        onDelete={handleDeleteProduct}
        loading={loading}
        emptyMessage="No products found. Create your first product."
      />

      {/* Modal */}
      <ProductFormModal
        isOpen={isModalOpen}
        onClose={() => {
          setIsModalOpen(false);
          setSelectedProduct(null);
        }}
        onSubmit={handleSubmitProduct}
        product={selectedProduct}
        categories={categories}
        loading={submitting}
      />
    </div>
  );
}
