import React, { useContext } from 'react'
import Filters from '../components/Filters'
import ProductCard from '../components/products/ProductCard'
import { ShopContext } from '../context/ShopContext'
import Loader from '../components/common/Loader'

export default function Products(){
  const { filteredProducts, searchQuery, cartItems, wishlistItems, loading, productsError } = useContext(ShopContext)

  if (loading) {
    return <Loader />
  }

  if (productsError) {
    return (
      <div className="max-w-6xl mx-auto px-4 py-8">
        <div className="rounded-3xl border border-red-200 bg-red-50 p-8 text-center">
          <h2 className="text-2xl font-semibold text-red-700 mb-2">Unable to load products</h2>
          <p className="text-slate-600">{productsError}</p>
        </div>
      </div>
    )
  }

  return (
    <div className="max-w-6xl mx-auto px-4 py-8 grid grid-cols-1 lg:grid-cols-[280px_minmax(0,1fr)] gap-6">
      <div>
        <Filters />
      </div>
      <div>
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 mb-6">
          <div>
            <h1 className="text-2xl font-semibold">Products</h1>
            <p className="text-sm text-slate-500">{filteredProducts.length} items found</p>
          </div>
          <div className="flex flex-wrap gap-3">
            <div className="rounded-full bg-slate-100 px-3 py-2 text-sm text-slate-600">Cart: {cartItems.length}</div>
            <div className="rounded-full bg-slate-100 px-3 py-2 text-sm text-slate-600">Wishlist: {wishlistItems.length}</div>
          </div>
        </div>

        {filteredProducts.length === 0 ? (
          <div className="rounded-xl border border-dashed border-slate-300 bg-white p-10 text-center">
            <h2 className="text-xl font-semibold mb-2">No products match your search</h2>
            <p className="text-slate-500">Try adjusting your filters or search terms.</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-6">
            {filteredProducts.map((product) => (
              <ProductCard key={product.id} p={product} />
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
