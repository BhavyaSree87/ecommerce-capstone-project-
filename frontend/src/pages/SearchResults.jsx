import React, { useContext, useState } from "react";
import { Link } from "react-router-dom";
import { ShopContext } from "../context/ShopContext";
import imageLoader from "../utils/imageLoader";
import productPlaceholder from "../assets/images/product-placeholder.svg";
import axios from "axios";

export default function SearchResults() {
  const { filteredProducts, searchQuery, loading, clearFilters } = useContext(ShopContext);
  const [aiResults, setAiResults] = useState([]);
  const [searchLoading, setSearchLoading] = useState(false);
  const searchWithAI = async () => {
  try {
    setSearchLoading(true);

    const response = await axios.post(
      "http://127.0.0.1:8000/api/ai/product-search",
      {
        query: searchQuery || "clothing"
      }
    );

    setAiResults(response.data.products || []);
    } catch (error) {
      console.error(error);
      alert("AI Product Search Failed");
    } finally {
      setSearchLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center px-4">
        <div className="rounded-full border-4 border-primary border-t-transparent w-12 h-12 animate-spin" />
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6">
        <div>
          <h1 className="text-3xl font-bold">Search Results</h1>
          <button
            onClick={searchWithAI}
            className="mt-3 bg-blue-600 text-white px-4 py-2 rounded-lg"
          >
            {searchLoading ? "Searching..." : "AI Product Search"}
          </button>
          <p className="text-slate-500 mt-2">Showing results for "{searchQuery || "all products"}"</p>
        </div>
        <button onClick={clearFilters} className="rounded-2xl bg-slate-100 px-5 py-3 text-sm text-slate-700 hover:bg-slate-200 transition">
          Clear filters
        </button>
      </div>

      {filteredProducts.length === 0 ? (
        <div className="rounded-3xl border border-dashed border-slate-300 bg-white p-10 text-center">
          <h2 className="text-2xl font-semibold mb-2">No products found</h2>
          <p className="text-slate-500">Try changing your filters or search term.</p>
          <Link to="/products" className="inline-flex mt-4 rounded-2xl bg-primary px-6 py-3 text-white hover:bg-pink-600 transition">
            Browse all products
          </Link>
        </div>
      ) : (
        <div className="grid gap-6 sm:grid-cols-2 xl:grid-cols-3">
          {(aiResults.length > 0 ? aiResults : filteredProducts).map((product) => (
            <Link key={product.id} to={`/product/${product.id}`} className="group block overflow-hidden rounded-3xl border border-slate-200 bg-white shadow-sm transition hover:-translate-y-1 hover:shadow-md">
              <img src={product.images?.[0] || product.image_url || productPlaceholder} alt={product.name} className="h-56 w-full object-cover transition duration-300 group-hover:scale-105" />
              <div className="p-5">
                <div className="text-sm text-slate-500 mb-2">{product.brand}</div>
                <h2 className="text-lg font-semibold mb-2">{product.name}</h2>
                <div className="flex items-center justify-between">
                  <span className="text-xl font-bold">₹{product.price}</span>
                  <span className="rounded-full bg-primary/10 text-primary px-3 py-1 text-xs font-semibold">{product.rating}★</span>
                </div>
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}