import React from 'react'

export default function CategoryCard({ item, onClick }){
  return (
    <button
      type="button"
      onClick={onClick}
      className="w-full text-left bg-white rounded-lg overflow-hidden shadow-sm hover:shadow-lg transition-smooth cursor-pointer"
    >
      <div className="h-40 overflow-hidden bg-slate-100">
        <img src={item.image} alt={item.title} className="w-full h-full object-cover" />
      </div>
      <div className="p-4">
        <h4 className="font-semibold">{item.title}</h4>
        <p className="text-sm text-slate-500">{item.count} items</p>
      </div>
    </button>
  )
}

