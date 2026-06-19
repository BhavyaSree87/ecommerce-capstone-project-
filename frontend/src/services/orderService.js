const ORDERS_KEY = "ecom_orders";

const parseStorage = (key) => {
  try {
    const raw = window.localStorage.getItem(key);
    return raw ? JSON.parse(raw) : [];
  } catch {
    return [];
  }
};

const saveStorage = (key, value) => {
  window.localStorage.setItem(key, JSON.stringify(value));
};

const generateOrderId = () => `ORD-${Date.now()}-${Math.floor(Math.random() * 900 + 100)}`;

export const loadOrders = () => parseStorage(ORDERS_KEY);

export const saveOrders = (orders) => saveStorage(ORDERS_KEY, orders);

export const placeOrder = async ({ user, items, shippingAddress, billingAddress, paymentMethod, totals, coupon }) => {
  const orders = loadOrders();
  const newOrder = {
    id: generateOrderId(),
    userEmail: user.email,
    items,
    shippingAddress,
    billingAddress,
    paymentMethod,
    totals,
    coupon: coupon || null,
    status: "Order Placed",
    createdAt: new Date().toISOString(),
    history: [
      { status: "Order Placed", timestamp: new Date().toISOString() },
    ],
  };

  orders.unshift(newOrder);
  saveOrders(orders);
  return newOrder;
};

export const getOrdersForUser = async (email) => {
  const orders = loadOrders();
  return orders.filter((order) => order.userEmail === email);
};

export const getOrderById = async (orderId) => {
  const orders = loadOrders();
  return orders.find((order) => order.id === orderId) || null;
};

export const cancelOrder = async (orderId) => {
  const orders = loadOrders();
  const updated = orders.map((order) =>
    order.id === orderId
      ? { ...order, status: "Cancelled", history: [...order.history, { status: "Cancelled", timestamp: new Date().toISOString() }] }
      : order
  );
  saveOrders(updated);
  return updated.find((order) => order.id === orderId);
};
