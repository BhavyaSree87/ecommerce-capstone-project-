import React from 'react'
import { Link } from 'react-router-dom'

export default function HeroBanner(){
  return (
    <section className="bg-white py-12">
      <div className="max-w-6xl mx-auto px-4 flex flex-col lg:flex-row items-center gap-8">
        <div className="flex-1">
          <h1 className="text-4xl md:text-5xl font-bold mb-4">Discover Your Style</h1>
          <p className="text-slate-600 mb-6">Trendy outfits, handpicked collections and AI-powered suggestions for every occasion.</p>
          <Link to="/products" className="inline-block bg-primary text-white px-6 py-3 rounded-md shadow hover:opacity-95 transition-smooth">Shop Now</Link>
        </div>
        <div className="flex-1">
          <img
            src="https://images.unsplash.com/photo-1441986300917-64674bd600d8"
            alt="Fashion Banner"
            className="w-full h-[450px] object-cover rounded-xl"
          />
        </div>
      </div>
    </section>
  )
}

