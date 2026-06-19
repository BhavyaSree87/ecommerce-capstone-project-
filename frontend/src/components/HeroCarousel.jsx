import React, { useEffect, useMemo, useState } from 'react'
import { Link } from 'react-router-dom'

const banners = [
  {
    title: 'Refresh Your Wardrobe',
    subtitle: 'Discover the latest styles for every season with premium fashion picks.',
    image: 'https://images.unsplash.com/photo-1441986300917-64674bd600d8',
  },
  {
    title: 'Bold Street Style',
    subtitle: 'Iconic looks that turn heads on the city streets and beyond.',
    image: 'https://images.unsplash.com/photo-1483985988355-763728e1935b',
  },
  {
    title: 'Elegant Evening Wear',
    subtitle: 'Beautiful silhouettes and luxe textures for your next night out.',
    image: 'https://images.unsplash.com/photo-1490481651871-ab68de25d43d',
  },
  {
    title: 'Fresh Fashion Finds',
    subtitle: 'New arrivals in curated trends, ready to elevate your closet.',
    image: 'https://images.unsplash.com/photo-1529139574466-a303027c1d8b',
  },
]

export default function HeroCarousel() {
  const [activeIndex, setActiveIndex] = useState(0)

  useEffect(() => {
    const interval = setInterval(() => {
      setActiveIndex((current) => (current + 1) % banners.length)
    }, 4000)
    return () => clearInterval(interval)
  }, [])

  const activeBanner = useMemo(() => banners[activeIndex], [activeIndex])

  return (
    <section className="bg-white py-8">
      <div className="max-w-7xl mx-auto px-4">
        <div className="relative overflow-hidden rounded-[32px] bg-slate-100 shadow-lg">
          <img
            src={`${activeBanner.image}?auto=format&fit=crop&w=1400&q=80`}
            alt={activeBanner.title}
            className="w-full h-[520px] object-cover transition duration-700 ease-out"
          />
          <div className="absolute inset-0 bg-gradient-to-r from-slate-900/80 via-slate-900/30 to-slate-900/0" />
          <div className="absolute inset-y-0 left-0 flex items-center px-6 md:px-10">
            <div className="max-w-xl text-white">
              <p className="text-sm uppercase tracking-[0.25em] text-amber-300 mb-3">New Arrivals</p>
              <h1 className="text-4xl md:text-5xl font-bold leading-tight mb-4">{activeBanner.title}</h1>
              <p className="text-sm md:text-base text-slate-100 max-w-lg mb-6">{activeBanner.subtitle}</p>
              <Link
                to="/products"
                className="inline-flex items-center justify-center rounded-full bg-primary px-6 py-3 text-sm font-semibold text-white shadow-lg shadow-primary/20 hover:bg-pink-600 transition"
              >
                Shop Collections
              </Link>
            </div>
          </div>

          <button
            type="button"
            aria-label="Previous slide"
            onClick={() => setActiveIndex((current) => (current - 1 + banners.length) % banners.length)}
            className="absolute left-4 top-1/2 -translate-y-1/2 rounded-full bg-white/90 p-3 shadow-md hover:bg-white"
          >
            ‹
          </button>
          <button
            type="button"
            aria-label="Next slide"
            onClick={() => setActiveIndex((current) => (current + 1) % banners.length)}
            className="absolute right-4 top-1/2 -translate-y-1/2 rounded-full bg-white/90 p-3 shadow-md hover:bg-white"
          >
            ›
          </button>

          <div className="absolute left-1/2 bottom-5 flex -translate-x-1/2 items-center gap-3">
            {banners.map((banner, index) => (
              <button
                key={banner.image}
                type="button"
                aria-label={`Slide ${index + 1}`}
                onClick={() => setActiveIndex(index)}
                className={`h-3 w-3 rounded-full transition ${index === activeIndex ? 'bg-white' : 'bg-white/50'}`}
              />
            ))}
          </div>
        </div>
      </div>
    </section>
  )
}
