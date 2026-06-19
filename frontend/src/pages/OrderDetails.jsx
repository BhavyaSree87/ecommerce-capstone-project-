import React, { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { getOrderById, cancelOrder } from "../services/orderService";
import Loader from "../components/common/Loader";
import imageLoader from "../utils/imageLoader";

const statusSteps = [
  "Order Placed",
  "Confirmed",
  "Packed",
  "Shipped",
  "Out For Delivery",
  "Delivered",
];

export default function OrderDetails() {
  const { id } = useParams();
  const [order, setOrder] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetch = async () => {
      setLoading(true);
      const result = await getOrderById(id);
      setOrder(result);
      setLoading(false);
    };
    fetch();
  }, [id]);

  const handleCancel = async () => {
    await cancelOrder(id);
    const updated = await getOrderById(id);
    setOrder(updated);
  };

  if (loading) {
    return <Loader />;
  }

  if (!order) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="rounded-3xl border border-dashed border-slate-300 bg-white p-10 text-center">
          <h2 className="text-2xl font-semibold">Order not found</h2>
          <p className="text-slate-500">Please check your order details.</p>
        </div>
      </div>
    );
  }

  const currentStepIndex = statusSteps.indexOf(order.status);

  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      <Link to="/orders" className="text-primary text-sm">← Back to orders</Link>
      <div className="mt-4 bg-white rounded-3xl border border-slate-200 p-6 shadow-sm">
        <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
          <div>
            <h1 className="text-3xl font-semibold">Order {order.id}</h1>
            <p className="text-slate-500">{new Date(order.createdAt).toLocaleString()}</p>
          </div>
          <div className="text-slate-700">
            <p><span className="font-semibold">Status:</span> {order.status}</p>
            <p><span className="font-semibold">Total:</span> ₹{order.totals.total}</p>
          </div>
        </div>

        <div className="mt-8 space-y-4">
          <div className="rounded-3xl border border-slate-200 p-5">
            <h2 className="text-xl font-semibold mb-3">Order Timeline</h2>
            <div className="space-y-4">
              {statusSteps.map((step, index) => (
                <div key={step} className="flex items-start gap-4">
                  <div className={`mt-1 h-3 w-3 rounded-full ${index <= currentStepIndex ? "bg-primary" : "bg-slate-300"}`} />
                  <div>
                    <div className="font-medium">{step}</div>
                    <p className="text-sm text-slate-500">{index <= currentStepIndex ? "Completed" : "Upcoming"}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="rounded-3xl border border-slate-200 p-5">
            <h2 className="text-xl font-semibold mb-3">Items</h2>
            <div className="space-y-4">
              {order.items.map((item) => (
                <div key={item.id} className="flex gap-4 items-center">
                  <img src={item.images?.[0] || imageLoader.getProductImage(item.name) || imageLoader.FALLBACK_IMAGE} alt={item.name} className="w-24 h-24 object-cover rounded" />
                  <div>
                    <h3 className="font-semibold">{item.name}</h3>
                    <p className="text-sm text-slate-500">Qty: {item.quantity}</p>
                    <p className="text-sm text-slate-900">₹{item.price}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="rounded-3xl border border-slate-200 p-5">
            <h2 className="text-xl font-semibold mb-3">Delivery & Billing</h2>
            <div className="grid gap-4 md:grid-cols-2">
              <div>
                <h3 className="font-medium mb-2">Shipping Address</h3>
                <p className="text-slate-600 text-sm">{order.shippingAddress.name}</p>
                <p className="text-slate-600 text-sm">{order.shippingAddress.line1}</p>
                <p className="text-slate-600 text-sm">{order.shippingAddress.city}, {order.shippingAddress.state}</p>
                <p className="text-slate-600 text-sm">{order.shippingAddress.pincode}</p>
              </div>
              <div>
                <h3 className="font-medium mb-2">Billing Address</h3>
                <p className="text-slate-600 text-sm">{order.billingAddress.name}</p>
                <p className="text-slate-600 text-sm">{order.billingAddress.line1}</p>
                <p className="text-slate-600 text-sm">{order.billingAddress.city}, {order.billingAddress.state}</p>
                <p className="text-slate-600 text-sm">{order.billingAddress.pincode}</p>
              </div>
            </div>
          </div>

          <div className="flex flex-wrap gap-4 justify-between items-center">
            {order.status !== "Cancelled" && (
              <button onClick={handleCancel} className="bg-rose-500 text-white rounded-2xl px-5 py-3 hover:bg-rose-600 transition">Cancel Order</button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
