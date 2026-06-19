import React, { useContext } from 'react'
import { useNavigate } from 'react-router-dom'
import CategoryCard from '../components/CategoryCard'
import { ShopContext } from '../context/ShopContext'

export default function Categories(){
  const { categories, setSelectedCategory } = useContext(ShopContext)
  const navigate = useNavigate()

  const handleClick = (title) => {
    setSelectedCategory(title)
    navigate('/products')
  }

  return (
    <div className="max-w-6xl mx-auto px-4 py-10">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-semibold">All Categories</h2>
        <button
          type="button"
          onClick={() => {
            setSelectedCategory("")
            navigate('/products')
          }}
          className="text-sm text-primary"
        >
          Browse products
        </button>
      </div>
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
        {categories.map((item) => (
          <CategoryCard
            key={item.title}
            item={item}
            onClick={() => handleClick(item.title)}
          />
        ))}
      </div>
    </div>
  )
}
