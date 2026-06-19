import React from 'react'
import ProductCard from './ProductCard'

export default function SimilarProducts({items}){
  return (
    <div className="py-6">
      <h3 className="text-lg font-semibold mb-4">Similar Products</h3>
      <div className="flex gap-4 overflow-x-auto pb-2">
        {items.map(it=> (
          <div key={it.id} className="w-56 flex-shrink-0">
            <ProductCard p={it} />
          </div>
        ))}
      </div>
    </div>
  )
}
