import React, { useContext } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { ShopContext } from '../../context/ShopContext'
import imageLoader from '../../utils/imageLoader'

export default function ProductCard({ p }){
  const navigate = useNavigate()
  const { toggleWishlist, isInWishlist } = useContext(ShopContext)
  const favorite = isInWishlist(p.id)
  
  // Use local image or fallback
  const imageUrl = p.image_url || p.images?.[0] || imageLoader.getProductImage(p.name) || imageLoader.FALLBACK_IMAGE

  return (
    <div className="bg-white rounded-lg overflow-hidden shadow-sm hover:shadow-md transition-smooth flex flex-col h-full">
      <div className="relative">
        <img src={imageUrl} alt={p.name} className="w-full h-64 object-cover rounded-t-xl" />
        <button
          type="button"
          onClick={() => toggleWishlist(p)}
          className={`absolute top-3 right-3 rounded-full p-2 shadow ${favorite ? 'bg-primary text-white' : 'bg-white text-slate-600'}`}
        >
          {favorite ? '♥' : '♡'}
        </button>
      </div>
      <div className="p-4 flex-1 flex flex-col">
        <div className="text-sm text-slate-500">{p.brand}</div>
        <Link to={`/product/${p.id}`} className="block font-medium mt-1 text-slate-900 hover:text-primary transition">
          {p.name}
        </Link>
        <div className="mt-3 flex items-center justify-between gap-3">
          <div>
            <div className="font-semibold">₹{p.price}</div>
            <div className="text-xs text-emerald-600">{p.discount}% off</div>
          </div>
          <div className="text-sm text-slate-600">{p.rating} ★</div>
        </div>
        <button
          type="button"
          onClick={() => navigate(`/product/${p.id}`)}
          className="mt-4 w-full bg-accent text-white py-2 rounded-md text-sm hover:bg-violet-600 transition"
        >
          Quick View
        </button>
      </div>
    </div>
  )
}
