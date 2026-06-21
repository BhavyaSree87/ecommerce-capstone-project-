import React from "react";
import { useLocation, Link } from "react-router-dom";

export default function OrderSuccess() {
  const { state } = useLocation();
  const order = state?.order;

  if (!order) {
    return (
      <div className="min-h-screen flex items-center justify-center px-4">
        <div className="rounded-3xl border border-dashed border-slate-300 bg-white p-10 text-center">
          <h2 className="text-2xl font-semibold">Order not found</h2>
          <p className="text-slate-500">Your order confirmation page is unavailable.</p>
        </div>
      </div>
    );
  }

  const orderId = order.order_id || order.id;
  const paymentMethod = order.paymentMethod || order.payment_method;
  const totalAmount = order.total_amount || order.totals?.total || order.amount || 0;
  const status = order.status || "Order Placed";
  const deliveryAddress = order.shipping || order.billing || {};

  return (
    <div className="max-w-4xl mx-auto px-4 py-10">
      <div className="bg-white rounded-3xl border border-slate-200 p-8 shadow-sm">
        <div className="text-center">
          <div className="text-5xl mb-4 text-emerald-600">✓</div>
          <h1 className="text-3xl font-semibold mb-2">Order Placed Successfully</h1>
          <p className="text-slate-500 mb-6">Your order is confirmed and will be delivered soon.</p>
        </div>

        <div className="grid gap-6 md:grid-cols-2">
          <div className="rounded-3xl border border-slate-200 bg-slate-50 p-6">
            <h2 className="text-lg font-semibold mb-4">Order Details</h2>
            <div className="space-y-3 text-slate-700">
              <div><span className="font-semibold">Order ID:</span> {orderId}</div>
              <div><span className="font-semibold">Payment:</span> {paymentMethod}</div>
              <div><span className="font-semibold">Amount:</span> ₹{totalAmount}</div>
              <div><span className="font-semibold">Status:</span> {status}</div>
            </div>
          </div>

          <div className="rounded-3xl border border-slate-200 bg-slate-50 p-6">
            <h2 className="text-lg font-semibold mb-4">Delivery Address</h2>
            <div className="text-slate-700 space-y-2 text-sm">
              <div>{deliveryAddress.name || deliveryAddress.fullName || "N/A"}</div>
              <div>{deliveryAddress.line1 || deliveryAddress.addressLine1 || ""}</div>
              <div>{deliveryAddress.city || ""}, {deliveryAddress.state || ""} {deliveryAddress.pincode || ""}</div>
              <div>{deliveryAddress.phone || deliveryAddress.contact || ""}</div>
            </div>
          </div>
        </div>

        <div className="mt-8 flex flex-col gap-4 sm:flex-row sm:justify-center">
          <Link
            to={`/track-order/${order.id}`}
            className="rounded-3xl bg-primary px-6 py-3 text-white font-semibold hover:bg-pink-600 transition"
          >
            Track Order
          </Link>
          <Link
            to="/products"
            className="rounded-3xl border border-slate-300 px-6 py-3 text-slate-700 hover:bg-slate-100 transition"
          >
            Continue Shopping
          </Link>
        </div>
      </div>
    </div>
  );
}
