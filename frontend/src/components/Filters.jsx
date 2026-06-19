import React, { useContext, useMemo } from "react";
import { ShopContext } from "../context/ShopContext";

export default function Filters() {
  const {
    categories,
    brands,
    sizes,
    colors,
    selectedCategory,
    setSelectedCategory,
    selectedBrands,
    setSelectedBrands,
    selectedSizes,
    setSelectedSizes,
    selectedColors,
    setSelectedColors,
    selectedRating,
    setSelectedRating,
    searchQuery,
    setSearchQuery,
    sortOrder,
    setSortOrder,
    priceRange,
    setPriceRange,
    clearFilters,
  } = useContext(ShopContext);

  const priceLabel = useMemo(
    () => `₹${priceRange[0]} - ₹${priceRange[1]}`,
    [priceRange]
  );

  const toggleOption = (value, list, setter) => {
    if (list.includes(value)) {
      setter(list.filter((item) => item !== value));
    } else {
      setter([...list, value]);
    }
  };

  return (
    <aside className="w-full md:w-72 p-4 bg-white rounded-lg shadow-sm sticky top-24">
      <h4 className="font-semibold mb-4">Filters</h4>

      <div className="space-y-4 text-sm text-slate-700">
        <div>
          <label className="block font-medium mb-2">Search</label>
          <input
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search products"
            className="w-full border rounded-md px-3 py-2"
          />
        </div>

        <div>
          <div className="font-medium mb-2">Category</div>
          <div className="grid grid-cols-2 gap-2">
            <button
              type="button"
              onClick={() => setSelectedCategory("")}
              className={`px-2 py-2 rounded-md border ${selectedCategory === "" ? "bg-primary text-white border-primary" : "bg-white text-slate-700"}`}>
              All
            </button>
            {categories.slice(0, 6).map((category) => (
              <button
                type="button"
                key={category.title}
                onClick={() => setSelectedCategory(category.title)}
                className={`px-2 py-2 rounded-md border ${selectedCategory === category.title ? "bg-primary text-white border-primary" : "bg-white text-slate-700"}`}>
                {category.title}
              </button>
            ))}
          </div>
        </div>

        <div>
          <div className="font-medium mb-2">Brand</div>
          <div className="grid grid-cols-2 gap-2">
            {brands.map((brand) => (
              <button
                key={brand}
                type="button"
                onClick={() => toggleOption(brand, selectedBrands, setSelectedBrands)}
                className={`px-2 py-2 rounded-md border ${selectedBrands.includes(brand) ? "bg-primary text-white border-primary" : "bg-white text-slate-700"}`}>
                {brand}
              </button>
            ))}
          </div>
        </div>

        <div>
          <div className="font-medium mb-2">Size</div>
          <div className="flex flex-wrap gap-2">
            {sizes.map((size) => (
              <button
                key={size}
                type="button"
                onClick={() => toggleOption(size, selectedSizes, setSelectedSizes)}
                className={`px-3 py-2 rounded-full border ${selectedSizes.includes(size) ? "bg-primary text-white border-primary" : "bg-white text-slate-700"}`}>
                {size}
              </button>
            ))}
          </div>
        </div>

        <div>
          <div className="font-medium mb-2">Color</div>
          <div className="flex flex-wrap gap-2">
            {colors.map((color) => (
              <button
                key={color}
                type="button"
                onClick={() => toggleOption(color, selectedColors, setSelectedColors)}
                className={`h-9 w-9 rounded-full border ${selectedColors.includes(color) ? "ring-2 ring-primary" : "border-slate-300"}`}
                style={{ backgroundColor: color }}
              />
            ))}
          </div>
        </div>

        <div>
          <div className="font-medium mb-2">Rating</div>
          <div className="flex flex-wrap gap-2">
            {[4, 3, 2, 1].map((rating) => (
              <button
                key={rating}
                type="button"
                onClick={() => setSelectedRating(selectedRating === rating ? 0 : rating)}
                className={`px-3 py-2 rounded-full border ${selectedRating === rating ? "bg-primary text-white border-primary" : "bg-white text-slate-700"}`}>
                {rating}★ & up
              </button>
            ))}
          </div>
        </div>

        <div>
          <div className="font-medium mb-2">Price Range</div>
          <div className="flex items-center justify-between text-xs text-slate-500 mb-2">
            <span>{priceLabel}</span>
            <button type="button" onClick={() => setPriceRange([0, 10000])} className="text-primary">Reset</button>
          </div>
          <input
            type="range"
            min="0"
            max="10000"
            value={priceRange[1]}
            onChange={(e) => setPriceRange([0, Number(e.target.value)])}
            className="w-full"
          />
        </div>

        <div>
          <div className="font-medium mb-2">Sort</div>
          <select
            value={sortOrder}
            onChange={(e) => setSortOrder(e.target.value)}
            className="w-full border rounded-md px-3 py-2"
          >
            <option value="popular">Popular</option>
            <option value="low">Price: Low to High</option>
            <option value="high">Price: High to Low</option>
            <option value="rating">Top Rated</option>
          </select>
        </div>

        <button
          type="button"
          onClick={clearFilters}
          className="w-full bg-slate-100 text-slate-700 py-2 rounded-md font-medium hover:bg-slate-200 transition"
        >
          Clear Filters
        </button>
      </div>
    </aside>
  );
}

