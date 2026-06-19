import apiService from "./apiService";
import imageLoader from "../utils/imageLoader";

const buildProduct = (product) => {
  const productName = product.product_name || "";
  const localImage = imageLoader.getProductImage(productName);
  const images = imageLoader.getProductImages(productName);

  return {
    id: product.product_id?.toString() || "",
    product_id: product.product_id,
    product_name: productName,
    name: productName,
    description: product.description || "",
    category: product.category || "",
    brand: product.brand || "",
    price: Number(product.price) || 0,
    stock: Number(product.stock) || 0,
    rating: Number(product.rating) || 0,
    image_url: localImage,
    image: localImage,
    images: images,
    discount: Number(product.discount) || 0,
    sizes: product.sizes || [],
    colors: product.colors || [],
    zone: product.zone || product.category || "",
  };
};

const getProducts = async () => {
  const response = await apiService.get("/api/products/all?page=1&page_size=100");
  const products = response.items || [];
  return Array.isArray(products) ? products.map(buildProduct) : [];
};

const getProductById = async (id) => {
  const products = await getProducts();
  return products.find((product) => product.id === id.toString()) || null;
};

const getSearchSuggestions = async (query) => {
  if (!query) return [];
  const normalized = query.toLowerCase();
  const products = await getProducts();
  const results = products.filter((product) =>
    product.name.toLowerCase().includes(normalized) ||
    product.brand.toLowerCase().includes(normalized) ||
    product.category.toLowerCase().includes(normalized)
  );
  return results.slice(0, 6).map((product) => ({
    id: product.id,
    name: product.name,
    brand: product.brand,
    image: product.image_url || product.images[0] || "",
  }));
};

const getRecommendedProducts = async (category, excludeId) => {
  const products = await getProducts();
  return products
    .filter((product) => product.category === category && product.id !== excludeId)
    .slice(0, 6);
};

const getRelatedProducts = async (product) => {
  const products = await getProducts();
  return products
    .filter((item) => item.category === product.category && item.id !== product.id)
    .slice(0, 6);
};

export default {
  getProducts,
  getProductById,
  getSearchSuggestions,
  getRecommendedProducts,
  getRelatedProducts,
};
