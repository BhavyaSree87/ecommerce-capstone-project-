import React, { useContext } from 'react'
import { Link } from 'react-router-dom'
import { ShopContext } from '../context/ShopContext'
import Loader from '../components/common/Loader'
import imageLoader from '../utils/imageLoader'

export default function Wishlist() {
  const { wishlistItems, toggleWishlist, addToCart, loading } = useContext(ShopContext)

  if (loading) {
    return <Loader />
  }

  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-3xl font-bold">Wishlist</h1>
          <p className="text-slate-500">Your favorite items saved for later.</p>
        </div>
        <Link to="/products" className="text-sm text-primary">Continue shopping</Link>
      </div>

      {wishlistItems.length === 0 ? (
        <div className="rounded-3xl border border-dashed border-slate-300 bg-white p-10 text-center">
          <h2 className="text-2xl font-semibold mb-2">No saved items yet</h2>
          <p className="text-slate-500">Add products to your wishlist to view them here.</p>
        </div>
      ) : (
        <div className="grid gap-6 lg:grid-cols-2 xl:grid-cols-3">
          {wishlistItems.map((product) => (
            <div key={product.id} className="bg-white rounded-3xl border border-slate-200 overflow-hidden shadow-sm">
              <img src={product.images?.[0] || imageLoader.getProductImage(product.name) || imageLoader.FALLBACK_IMAGE} alt={product.name} className="w-full h-64 object-cover" />
              <div className="p-5">
                <div className="text-sm text-slate-500">{product.brand}</div>
                <h2 className="mt-2 text-lg font-semibold">{product.name}</h2>
                <div className="mt-3 flex items-center justify-between text-slate-900">
                  <span className="text-xl font-bold">₹{product.price}</span>
                  <span className="text-sm text-emerald-600">{product.discount}% off</span>
                </div>
                <div className="mt-4 flex items-center gap-2">
                  <button
                    type="button"
                    onClick={() => addToCart(product)}
                    className="flex-1 bg-primary text-white py-2 rounded-2xl text-sm hover:bg-pink-600 transition"
                  >
                    Add to Cart
                  </button>
                  <button
                    type="button"
                    onClick={() => toggleWishlist(product)}
                    className="flex-1 border border-slate-300 py-2 rounded-2xl text-sm text-slate-700 hover:border-primary hover:text-primary transition"
                  >
                    Remove
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
