import apiService from "./apiService";
import { getToken } from "./authService";
import { RAZORPAY_KEY_ID } from "./config";

const RAZORPAY_SCRIPT_SRC = "https://checkout.razorpay.com/v1/checkout.js";

const loadRazorpayScript = () =>
  new Promise((resolve, reject) => {
    if (window.Razorpay) {
      return resolve(true);
    }

    const script = document.createElement("script");
    script.src = RAZORPAY_SCRIPT_SRC;
    script.onload = () => resolve(true);
    script.onerror = () => reject(new Error("Failed to load Razorpay checkout script."));
    document.body.appendChild(script);
  });

const getAuthHeaders = () => {
  const token = getToken();
  return token ? { Authorization: `Bearer ${token}` } : {};
};

const mapPaymentMethod = (method) => {
  switch (method) {
    case "Cash On Delivery":
      return "COD";
    case "Credit Card":
      return "CREDIT_CARD";
    case "Debit Card":
      return "DEBIT_CARD";
    case "Net Banking":
      return "NET_BANKING";
    case "UPI":
      return "UPI";
    default:
      return method.toUpperCase().replace(/\s+/g, "_");
  }
};

const createAddressString = (address) =>
  `${address.name}, ${address.line1}, ${address.city}, ${address.state} ${address.pincode}, ${address.phone}`;

const createOrderPayload = ({ cartItems, shipping, billing, sameBilling, coupon, paymentMethod }) => ({
  items: cartItems.map((item) => ({
    product_id: Number(item.product_id || item.id),
    quantity: Number(item.quantity),
    price: Number(item.price),
  })),
  shipping_address: createAddressString(shipping),
  billing_address: createAddressString(sameBilling ? shipping : billing),
  payment_method: mapPaymentMethod(paymentMethod),
  notes: coupon ? `Coupon: ${coupon}` : null,
});

const createRazorpayOrder = async ({ amount, paymentMethod, receipt, notes }) =>
  apiService.post(
    "/api/payments/razorpay/create-order",
    {
      amount,
      currency: "INR",
      receipt,
      notes: { ...notes, payment_method: paymentMethod },
    },
    { headers: getAuthHeaders() }
  );

const verifyRazorpayPayment = async (payload) =>
  apiService.post("/api/payments/razorpay/verify", payload, { headers: getAuthHeaders() });

const savePayment = async (paymentData) =>
  apiService.post("/api/payments/save", paymentData, { headers: getAuthHeaders() });

const createOrder = async (orderData) =>
  apiService.post("/api/orders/create", orderData, { headers: getAuthHeaders() });

const openRazorpayCheckout = async ({ razorpayOrder, paymentMethod, paymentDetails, orderInfo, user }) => {
  await loadRazorpayScript();

  if (!window.Razorpay) {
    throw new Error("Razorpay checkout failed to initialize.");
  }

  return new Promise((resolve, reject) => {
    const uiPaymentMethod = mapPaymentMethod(paymentMethod);
    const method = paymentMethod === "UPI" ? "upi" : paymentMethod === "Net Banking" ? "netbanking" : "card";

    const options = {
      key: RAZORPAY_KEY_ID,
      amount: Math.round(razorpayOrder.amount),
      currency: razorpayOrder.currency,
      name: "E-Commerce Platform",
      description: "Order payment",
      order_id: razorpayOrder.razorpay_order_id,
      prefill: {
        name: user?.name || "",
        email: user?.email || "",
        contact: orderInfo.shipping.phone || "",
        ...(paymentMethod === "UPI" && paymentDetails.upiId ? { vpa: paymentDetails.upiId } : {}),
      },
      notes: {
        payment_method: uiPaymentMethod,
        selected_bank: paymentDetails.bank || "",
        coupon: orderInfo.coupon || "",
      },
      method,
      ...(paymentMethod === "Net Banking" && paymentDetails.bank
        ? { netbanking: { bank: paymentDetails.bank } }
        : {}),
      handler: (response) => {
        resolve(response);
      },
      modal: {
        escape: false,
      },
      theme: {
        color: "#fb7185",
      },
    };

    const checkout = new window.Razorpay(options);
    checkout.on("payment.failed", (failure) => {
      reject(new Error(failure.error?.description || "Razorpay payment failed."));
    });
    checkout.open();
  });
};

const processCODCheckout = async ({ paymentMethod, paymentState, cartItems }) => {
  const orderPayload = createOrderPayload({
    cartItems,
    shipping: paymentState.shipping,
    billing: paymentState.billing,
    sameBilling: paymentState.sameBilling,
    coupon: paymentState.coupon,
    paymentMethod,
  });

  const order = await createOrder(orderPayload);

  await savePayment({
    order_id: order.order_id,
    payment_method: mapPaymentMethod(paymentMethod),
    payment_status: "PENDING",
    amount: order.total_amount,
    transaction_id: null,
  });

  return {
    ...order,
    id: order.order_id,
    paymentMethod,
    totals: paymentState.totals,
    shipping: paymentState.shipping,
    billing: paymentState.billing,
  };
};

const processRazorpayCheckout = async ({ paymentMethod, paymentDetails, paymentState, cartItems, user }) => {
  const backendMethod = mapPaymentMethod(paymentMethod);
  const razorpayOrder = await createRazorpayOrder({
    amount: paymentState.totals.total,
    paymentMethod: backendMethod,
    receipt: `order_${Date.now()}`,
    notes: { user_id: user?.user_id || user?.id },
  });

  const paymentResponse = await openRazorpayCheckout({
    razorpayOrder,
    paymentMethod,
    paymentDetails,
    orderInfo: paymentState,
    user,
  });

  await verifyRazorpayPayment({
    razorpay_order_id: paymentResponse.razorpay_order_id,
    razorpay_payment_id: paymentResponse.razorpay_payment_id,
    razorpay_signature: paymentResponse.razorpay_signature,
  });

  const order = await createOrder(
    createOrderPayload({
      cartItems,
      shipping: paymentState.shipping,
      billing: paymentState.billing,
      sameBilling: paymentState.sameBilling,
      coupon: paymentState.coupon,
      paymentMethod,
    })
  );

  await savePayment({
    order_id: order.order_id,
    payment_method: backendMethod,
    payment_status: "PAID",
    amount: order.total_amount,
    transaction_id: paymentResponse.razorpay_payment_id,
    razorpay_order_id: paymentResponse.razorpay_order_id,
    razorpay_payment_id: paymentResponse.razorpay_payment_id,
  });

  return {
    ...order,
    id: order.order_id,
    paymentMethod,
    totals: paymentState.totals,
    shipping: paymentState.shipping,
    billing: paymentState.billing,
  };
};

const processCheckout = async ({ paymentMethod, paymentDetails, paymentState, cartItems, user }) => {
  if (!paymentState) {
    throw new Error("Checkout information is missing.");
  }

  if (paymentMethod === "Cash On Delivery") {
    return processCODCheckout({ paymentMethod, paymentState, cartItems });
  }

  if (paymentMethod === "UPI" && !paymentDetails.upiId) {
    throw new Error("Please enter your UPI ID.");
  }

  if (paymentMethod === "Net Banking" && !paymentDetails.bank) {
    throw new Error("Please select your bank.");
  }

  return processRazorpayCheckout({ paymentMethod, paymentDetails, paymentState, cartItems, user });
};

export default {
  processCheckout,
};
