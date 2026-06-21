import React, { useContext, useEffect, useMemo, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { ShopContext } from "../context/ShopContext";
import SimilarProducts from "../components/products/SimilarProducts";
import Loader from "../components/common/Loader";
import imageLoader from "../utils/imageLoader";
import axios from "axios";
import { API_BASE_URL } from "../services/config";

export default function ProductDetails() {
  const { id } = useParams();
  const {
    products,
    addToCart,
    toggleWishlist,
    isInWishlist,
    loading,
    productsError,
    trackProductView,
    recentlyViewed,
    recommendedProducts,
  } = useContext(ShopContext);
  const navigate = useNavigate();
  const [selectedImage, setSelectedImage] = useState(null);
  const [aiDescription, setAiDescription] = useState("");
  const [descriptionLoading, setDescriptionLoading] = useState(false);

  const product = useMemo(
    () => products.find((item) => item.id === id) || products[0] || null,
    [products, id]
  );

  useEffect(() => {
    if (product) {
      trackProductView(product);
      setSelectedImage(null);
    }
  }, [product, trackProductView]);

  if (loading) {
    return <Loader />;
  }

  if (productsError || !product) {
    return (
      <div className="max-w-6xl mx-auto px-4 py-8">
        <div className="rounded-3xl border border-red-200 bg-red-50 p-8 text-center">
          <h2 className="text-2xl font-semibold text-red-700 mb-2">Unable to load product details</h2>
          <p className="text-slate-600">{productsError || "Product not found."}</p>
          <button
            type="button"
            onClick={() => navigate('/products')}
            className="mt-6 bg-primary text-white px-5 py-3 rounded-2xl"
          >
            Back to Products
          </button>
        </div>
      </div>
    );
  }

  const selectedProduct = selectedImage || product.images[0] || product.image_url || imageLoader.getProductImage(product.name) || imageLoader.FALLBACK_IMAGE;
  const wishlistActive = isInWishlist(product.id);
  const relatedProducts = products.filter(
    (item) => item.category === product.category && item.id !== product.id
  );
  const generateDescription = async () => {
  try {
    setDescriptionLoading(true);

    const response = await axios.post(
      `${API_BASE_URL}/api/ai/generate-description`,
      {
        product_name: product.name,
        category: product.category,
        brand: product.brand,
      }
    );

    setAiDescription(response.data.generated_description);
      } catch (error) {
        console.error(error);
        alert("Failed to generate description");
      } finally {
        setDescriptionLoading(false);
      }
    };

  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <div className="bg-white rounded-3xl overflow-hidden shadow-sm">
            <img src={selectedProduct} alt={product.name} className="w-full h-[420px] object-cover" />
          </div>
          <div className="mt-4 grid grid-cols-4 gap-3">
            {product.images?.map((image, index) => (
              <button
                key={index}
                type="button"
                onClick={() => setSelectedImage(image)}
                className={`rounded-xl overflow-hidden border ${selectedProduct === image ? "border-primary" : "border-slate-200"}`}>
                <img src={image} alt={`${product.name} ${index + 1}`} className="w-full h-20 object-cover" />
              </button>
            ))}
          </div>
        </div>

        <div className="bg-white rounded-3xl p-6 shadow-sm">
          <div className="text-sm text-slate-500">{product.brand}</div>
          <h1 className="text-3xl font-semibold mt-2">{product.name}</h1>
          <div className="mt-4 flex items-center gap-4">
            <span className="text-3xl font-bold">₹{product.price}</span>
            <span className="text-sm text-emerald-600">{product.discount}% off</span>
          </div>
          <div className="mt-4 flex items-center gap-2 text-sm text-slate-600">
            <span>{product.rating} ★</span>
            <span className="h-2 w-2 rounded-full bg-slate-300" />
            <span>{product.category}</span>
          </div>

          <div className="mt-6">
          <div className="font-medium mb-2">Description</div>

          <p className="text-slate-600">
            {aiDescription || product.description}
          </p>

          <button
            onClick={generateDescription}
            className="mt-3 bg-blue-600 text-white px-4 py-2 rounded-lg"
          >
            {descriptionLoading ? "Generating..." : "Generate AI Description"}
          </button>
        </div>

          <div className="mt-6">
            <div className="font-medium mb-2">Available Sizes</div>
            <div className="flex flex-wrap gap-3">
              {product.sizes.map((size) => (
                <span key={size} className="px-3 py-2 border rounded-full text-sm text-slate-700">{size}</span>
              ))}
            </div>
          </div>

          <div className="mt-6">
            <div className="font-medium mb-2">Colors</div>
            <div className="flex gap-3">
              {product.colors.map((color, index) => (
                <span key={index} className="h-8 w-8 rounded-full border" style={{ background: color }} />
              ))}
            </div>
          </div>

          <div className="mt-8 flex flex-col gap-3 sm:flex-row">
            <button
              type="button"
              onClick={() => addToCart(product)}
              className="flex-1 bg-primary text-white px-5 py-3 rounded-2xl font-medium hover:bg-pink-600 transition"
            >
              Add to Cart
            </button>
            <button
              type="button"
              onClick={() => toggleWishlist(product)}
              className="flex-1 border border-slate-300 px-5 py-3 rounded-2xl text-slate-700 hover:border-primary hover:text-primary transition"
            >
              {wishlistActive ? "Remove from Wishlist" : "Add to Wishlist"}
            </button>
          </div>

          <button
            type="button"
            onClick={() => navigate("/products")}
            className="mt-4 text-sm text-slate-500"
          >
            Back to products
          </button>
        </div>
      </div>

      <div className="mt-10 space-y-10">
        <div>
          <h2 className="text-2xl font-semibold mb-4">Similar Products</h2>
          <SimilarProducts items={relatedProducts.slice(0, 6)} />
        </div>
        {recentlyViewed.length > 1 && (
          <div>
            <h2 className="text-2xl font-semibold mb-4">Recently Viewed</h2>
            <SimilarProducts items={recentlyViewed.filter((item) => item.id !== product.id)} />
          </div>
        )}
        {recommendedProducts.length > 0 && (
          <div>
            <h2 className="text-2xl font-semibold mb-4">Recommended For You</h2>
            <SimilarProducts items={recommendedProducts} />
          </div>
        )}
      </div>
    </div>
  );
}
