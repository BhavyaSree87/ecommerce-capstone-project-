import React, { useContext } from 'react'
import { useNavigate } from 'react-router-dom'
import HeroCarousel from '../components/HeroCarousel'
import CategoryCard from '../components/CategoryCard'
import ProductCard from '../components/products/ProductCard'
import { ShopContext } from '../context/ShopContext'
import productsData from '../data/products'

export default function Home(){
  const { categories, setSelectedCategory } = useContext(ShopContext)
  const navigate = useNavigate()

  const handleCategoryClick = (title) => {
    setSelectedCategory(title)
    navigate('/products')
  }

  return (
    <div>
      <HeroCarousel />

      <section className="max-w-6xl mx-auto px-4 py-10">
        <div className="flex items-center justify-between mb-6">
          <h3 className="text-xl font-semibold">Top Categories</h3>
          <button
            type="button"
            onClick={() => {
              setSelectedCategory("")
              navigate('/products')
            }}
            className="text-sm text-primary"
          >
            View All
          </button>
        </div>
        <div className="grid grid-cols-2 md:grid-cols-6 gap-4">
          {categories.map((category) => (
            <CategoryCard
              key={category.title}
              item={category}
              onClick={() => handleCategoryClick(category.title)}
            />
          ))}
        </div>
      </section>

      <section className="bg-slate-50 py-8">
        <div className="max-w-6xl mx-auto px-4">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-xl font-semibold">Trending Collections</h3>
            <button
              type="button"
              onClick={() => navigate('/products')}
              className="text-sm text-primary"
            >
              See all products
            </button>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-6">
            {productsData.slice(0, 4).map((product) => (
              <ProductCard key={product.id} p={product} />
            ))}
          </div>
        </div>
      </section>

      <section className="max-w-6xl mx-auto px-4 py-10">
        <h3 className="text-xl font-semibold mb-4">Popular Zones</h3>
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
          {['Casual Wear','Formal Wear','Sportswear','Party Wear','Ethnic Wear'].map((zone) => (
            <button
              type="button"
              key={zone}
              onClick={() => handleCategoryClick(zone)}
              className="p-6 bg-white rounded-lg shadow-sm hover:shadow-md transition-smooth text-left"
            >
              {zone}
            </button>
          ))}
        </div>
      </section>
    </div>
  )
}
