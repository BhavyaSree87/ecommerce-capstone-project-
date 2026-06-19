const CART_KEY = "ecom_cart_items";

const parseStorage = (key) => {
  try {
    const json = window.localStorage.getItem(key);
    return json ? JSON.parse(json) : [];
  } catch {
    return [];
  }
};

const saveStorage = (key, value) => {
  window.localStorage.setItem(key, JSON.stringify(value));
};

export const loadCart = () => parseStorage(CART_KEY);

export const saveCart = (items) => saveStorage(CART_KEY, items);

export const calculateCartTotals = (items) => {
  const subtotal = items.reduce((sum, item) => sum + item.price * item.quantity, 0);
  const discount = Math.round(subtotal * 0.04);
  const tax = Math.round((subtotal - discount) * 0.12);
  const shipping = subtotal > 0 ? 99 : 0;
  const total = subtotal - discount + tax + shipping;

  return { subtotal, discount, tax, shipping, total };
};
