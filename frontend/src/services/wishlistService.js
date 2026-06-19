const WISHLIST_KEY = "ecom_wishlist_items";

const parseStorage = (key) => {
  try {
    const stored = window.localStorage.getItem(key);
    return stored ? JSON.parse(stored) : [];
  } catch {
    return [];
  }
};

const saveStorage = (key, value) => {
  window.localStorage.setItem(key, JSON.stringify(value));
};

export const loadWishlist = () => parseStorage(WISHLIST_KEY);
export const saveWishlist = (items) => saveStorage(WISHLIST_KEY, items);
