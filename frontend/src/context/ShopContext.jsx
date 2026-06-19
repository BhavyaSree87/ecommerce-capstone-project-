import React, { createContext, useEffect, useMemo, useState } from "react";
import productService from "../services/productService";
import { categories as categoriesData } from "../data/products";

export const ShopContext = createContext();

const STORAGE_CART_KEY = "shop_cart_items";
const STORAGE_WISHLIST_KEY = "shop_wishlist_items";
const STORAGE_VIEWED_KEY = "shop_recently_viewed";

const parseStorage = (key) => {
  try {
    const stored = window.localStorage.getItem(key);
    return stored ? JSON.parse(stored) : [];
  } catch (error) {
    return [];
  }
};

const ShopProvider = ({ children }) => {
  const [loading, setLoading] = useState(true);
  const [products, setProducts] = useState([]);
  const [categories, setCategories] = useState(categoriesData);
  const [productsError, setProductsError] = useState(null);
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedCategory, setSelectedCategory] = useState("");
  const [selectedBrands, setSelectedBrands] = useState([]);
  const [selectedSizes, setSelectedSizes] = useState([]);
  const [selectedColors, setSelectedColors] = useState([]);
  const [selectedRating, setSelectedRating] = useState(0);
  const [sortOrder, setSortOrder] = useState("popular");
  const [priceRange, setPriceRange] = useState([0, 10000]);
  const [cartItems, setCartItems] = useState(() => parseStorage(STORAGE_CART_KEY));
  const [wishlistItems, setWishlistItems] = useState(() => parseStorage(STORAGE_WISHLIST_KEY));
  const [recentlyViewed, setRecentlyViewed] = useState(() => parseStorage(STORAGE_VIEWED_KEY));

  useEffect(() => {
    const fetchProducts = async () => {
      setLoading(true);
      try {
        const fetchedProducts = await productService.getProducts();
        setProducts(fetchedProducts);
        setProductsError(null);
      } catch (error) {
        setProductsError(error.message || "Unable to load products.");
      } finally {
        setLoading(false);
      }
    };

    fetchProducts();
  }, []);

  useEffect(() => {
    const categoryCounts = categoriesData.map((category) => ({
      ...category,
      count: products.filter((product) => product.category === category.title).length,
    }));
    setCategories(categoryCounts);
  }, [products]);

  useEffect(() => {
    window.localStorage.setItem(STORAGE_CART_KEY, JSON.stringify(cartItems));
  }, [cartItems]);

  useEffect(() => {
    window.localStorage.setItem(STORAGE_WISHLIST_KEY, JSON.stringify(wishlistItems));
  }, [wishlistItems]);

  useEffect(() => {
    window.localStorage.setItem(STORAGE_VIEWED_KEY, JSON.stringify(recentlyViewed));
  }, [recentlyViewed]);

  const brands = useMemo(
    () => [...new Set(products.map((product) => product.brand || ""))],
    [products]
  );
  const sizes = useMemo(
    () => [...new Set(products.flatMap((product) => product.sizes || []))],
    [products]
  );
  const colors = useMemo(
    () => [...new Set(products.flatMap((product) => product.colors || []))],
    [products]
  );

  const featuredProducts = useMemo(() => products.slice(0, 8), [products]);

  const addToCart = (product) => {
    setCartItems((prev) => {
      const existing = prev.find((item) => item.id === product.id);
      if (existing) {
        return prev.map((item) =>
          item.id === product.id
            ? { ...item, quantity: item.quantity + 1 }
            : item
        );
      }
      return [...prev, { ...product, quantity: 1 }];
    });
  };

  const removeFromCart = (productId) => {
    setCartItems((prev) => prev.filter((item) => item.id !== productId));
  };

  const increaseQty = (productId) => {
    setCartItems((prev) =>
      prev.map((item) =>
        item.id === productId
          ? { ...item, quantity: item.quantity + 1 }
          : item
      )
    );
  };

  const decreaseQty = (productId) => {
    setCartItems((prev) =>
      prev
        .map((item) =>
          item.id === productId
            ? { ...item, quantity: Math.max(item.quantity - 1, 1) }
            : item
        )
        .filter((item) => item.quantity > 0)
    );
  };

  const isInWishlist = (productId) => {
    return wishlistItems.some((item) => item.id === productId);
  };

  const toggleWishlist = (product) => {
    setWishlistItems((prev) => {
      const exists = prev.some((item) => item.id === product.id);
      if (exists) {
        return prev.filter((item) => item.id !== product.id);
      }
      return [...prev, product];
    });
  };

  const trackProductView = (product) => {
    setRecentlyViewed((prev) => {
      const filtered = prev.filter((item) => item.id !== product.id);
      const next = [product, ...filtered].slice(0, 6);
      return next;
    });
  };

  const clearFilters = () => {
    setSearchQuery("");
    setSelectedCategory("");
    setSelectedBrands([]);
    setSelectedSizes([]);
    setSelectedColors([]);
    setSelectedRating(0);
    setSortOrder("popular");
    setPriceRange([0, 10000]);
  };

  const filteredProducts = useMemo(() => {
    let result = [...products];

    if (selectedCategory) {
      result = result.filter(
        (product) =>
          product.category.toLowerCase() === selectedCategory.toLowerCase()
      );
    }

    if (selectedBrands.length) {
      result = result.filter((product) => selectedBrands.includes(product.brand));
    }

    if (selectedSizes.length) {
      result = result.filter((product) =>
        product.sizes.some((size) => selectedSizes.includes(size))
      );
    }

    if (selectedColors.length) {
      result = result.filter((product) =>
        product.colors.some((color) => selectedColors.includes(color))
      );
    }

    if (selectedRating) {
      result = result.filter((product) => product.rating >= selectedRating);
    }

    if (searchQuery) {
      const query = searchQuery.toLowerCase();
      result = result.filter(
        (product) =>
          product.name.toLowerCase().includes(query) ||
          product.brand.toLowerCase().includes(query) ||
          product.category.toLowerCase().includes(query) ||
          product.zone.toLowerCase().includes(query)
      );
    }

    result = result.filter(
      (product) =>
        product.price >= priceRange[0] && product.price <= priceRange[1]
    );

    if (sortOrder === "low") {
      result.sort((a, b) => a.price - b.price);
    } else if (sortOrder === "high") {
      result.sort((a, b) => b.price - a.price);
    } else if (sortOrder === "rating") {
      result.sort((a, b) => b.rating - a.rating);
    }

    return result;
  }, [products, selectedCategory, selectedBrands, selectedSizes, selectedColors, selectedRating, searchQuery, sortOrder, priceRange]);

  const cartCount = useMemo(
    () => cartItems.reduce((sum, item) => sum + item.quantity, 0),
    [cartItems]
  );

  const cartTotal = useMemo(
    () =>
      cartItems.reduce((sum, item) => sum + item.price * item.quantity, 0),
    [cartItems]
  );

  const recommendedProducts = useMemo(() => {
    if (recentlyViewed.length > 0) {
      const latest = recentlyViewed[0];
      return products
        .filter((product) => product.category === latest.category && product.id !== latest.id)
        .slice(0, 6);
    }
    return products.slice(0, 6);
  }, [products, recentlyViewed]);

  const value = {
    loading,
    products,
    categories,
    productsError,
    brands,
    sizes,
    colors,
    recentlyViewed,
    recommendedProducts,
    featuredProducts,
    filteredProducts,
    searchQuery,
    setSearchQuery,
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
    sortOrder,
    setSortOrder,
    priceRange,
    setPriceRange,
    clearFilters,
    cartItems,
    addToCart,
    removeFromCart,
    increaseQty,
    decreaseQty,
    cartCount,
    cartTotal,
    wishlistItems,
    toggleWishlist,
    isInWishlist,
    wishlistCount: wishlistItems.length,
    trackProductView,
  };

  return (
    <ShopContext.Provider value={value}>{children}</ShopContext.Provider>
  );
};

export default ShopProvider;
