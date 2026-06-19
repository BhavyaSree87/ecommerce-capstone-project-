import React, { useEffect, useState } from 'react';
import adminService from '../../services/adminService';
import LoadingSpinner from '../components/common/LoadingSpinner';
import Alert from '../components/common/Alert';

export default function AdminInventory() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [searchQuery, setSearchQuery] = useState('');
  const [editingId, setEditingId] = useState(null);
  const [newStock, setNewStock] = useState('');

  useEffect(() => {
    fetchProducts();
  }, []);

  const fetchProducts = async () => {
    try {
      setLoading(true);
      setError('');
      const data = await adminService.getAllProducts();
      setProducts(data);
    } catch (err) {
      setError(err.message || 'Failed to load inventory');
    } finally {
      setLoading(false);
    }
  };

  const handleUpdateStock = async (id, currentStock) => {
    try {
      setError('');
      const stock = parseInt(newStock) || currentStock;
      await adminService.updateProduct(id, { stock });
      setProducts(products.map(p => p.id === id ? { ...p, stock } : p));
      setEditingId(null);
      setNewStock('');
    } catch (err) {
      setError(err.message || 'Failed to update stock');
    }
  };

  const filteredProducts = products.filter(product => {
    const searchLower = searchQuery.toLowerCase();
    return (product.product_name || product.name || '').toLowerCase().includes(searchLower);
  });

  const lowStockProducts = filteredProducts.filter(p => p.stock < 10);
  const outOfStockProducts = filteredProducts.filter(p => p.stock === 0);

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
        <h1 className="text-3xl font-bold text-slate-900">Inventory Management</h1>
        <p className="text-slate-500 mt-1">{filteredProducts.length} products in inventory</p>
      </div>

      {error && <Alert type="error" message={error} onClose={() => setError('')} />}

      {/* Stock Alerts */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="rounded-2xl border border-orange-200 bg-orange-50 p-4">
          <p className="text-sm font-medium text-orange-700">Low Stock (<10)</p>
          <p className="text-2xl font-bold text-orange-900 mt-1">{lowStockProducts.length}</p>
        </div>
        
        <div className="rounded-2xl border border-red-200 bg-red-50 p-4">
          <p className="text-sm font-medium text-red-700">Out of Stock</p>
          <p className="text-2xl font-bold text-red-900 mt-1">{outOfStockProducts.length}</p>
        </div>
        
        <div className="rounded-2xl border border-emerald-200 bg-emerald-50 p-4">
          <p className="text-sm font-medium text-emerald-700">In Stock</p>
          <p className="text-2xl font-bold text-emerald-900 mt-1">
            {filteredProducts.filter(p => p.stock > 0).length}
          </p>
        </div>
      </div>

      {/* Search */}
      <div>
        <input
          type="text"
          placeholder="Search products..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="w-full rounded-lg border border-slate-200 px-4 py-2 focus:outline-none focus:ring-2 focus:ring-primary"
        />
      </div>

      {/* Inventory Table */}
      <div className="rounded-2xl border border-slate-200 bg-white shadow-sm overflow-hidden">
        <table className="w-full">
          <thead className="border-b border-slate-200 bg-slate-50">
            <tr>
              <th className="text-left font-semibold text-slate-900 px-6 py-3">Product Name</th>
              <th className="text-left font-semibold text-slate-900 px-6 py-3">SKU</th>
              <th className="text-center font-semibold text-slate-900 px-6 py-3">Current Stock</th>
              <th className="text-left font-semibold text-slate-900 px-6 py-3">Status</th>
              <th className="text-center font-semibold text-slate-900 px-6 py-3">Action</th>
            </tr>
          </thead>
          <tbody>
            {filteredProducts.map((product) => (
              <tr key={product.id} className="border-b border-slate-100 hover:bg-slate-50">
                <td className="px-6 py-4 text-sm text-slate-700 font-medium">
                  {product.product_name || product.name}
                </td>
                <td className="px-6 py-4 text-sm text-slate-600">SKU-{product.id}</td>
                <td className="px-6 py-4 text-center">
                  {editingId === product.id ? (
                    <div className="flex items-center gap-2 justify-center">
                      <input
                        type="number"
                        value={newStock}
                        onChange={(e) => setNewStock(e.target.value)}
                        className="w-16 rounded border border-slate-200 px-2 py-1 text-sm"
                        placeholder={product.stock}
                      />
                      <button
                        onClick={() => handleUpdateStock(product.id, product.stock)}
                        className="text-xs bg-emerald-500 text-white px-2 py-1 rounded hover:bg-emerald-600"
                      >
                        Save
                      </button>
                      <button
                        onClick={() => setEditingId(null)}
                        className="text-xs bg-slate-300 text-slate-700 px-2 py-1 rounded hover:bg-slate-400"
                      >
                        Cancel
                      </button>
                    </div>
                  ) : (
                    <span className="font-semibold text-slate-900">{product.stock || 0}</span>
                  )}
                </td>
                <td className="px-6 py-4 text-sm">
                  <span className={`px-3 py-1 rounded-full text-xs font-medium ${
                    product.stock === 0 ? 'bg-red-100 text-red-700' :
                    product.stock < 10 ? 'bg-orange-100 text-orange-700' :
                    'bg-emerald-100 text-emerald-700'
                  }`}>
                    {product.stock === 0 ? 'Out of Stock' :
                     product.stock < 10 ? 'Low Stock' :
                     'In Stock'}
                  </span>
                </td>
                <td className="px-6 py-4 text-center">
                  <button
                    onClick={() => {
                      setEditingId(product.id);
                      setNewStock(product.stock);
                    }}
                    className="text-xs bg-blue-100 text-blue-700 px-3 py-1 rounded hover:bg-blue-200"
                  >
                    Edit
                  </button>
                </td>
              </tr>
            ))}
            {filteredProducts.length === 0 && (
              <tr>
                <td colSpan="5" className="px-6 py-8 text-center text-slate-500">
                  No products found
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
