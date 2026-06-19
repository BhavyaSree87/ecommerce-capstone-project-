import React, { useMemo } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { getOrderById } from "../services/orderService";

const statusSteps = [
  "Order Placed",
  "Confirmed",
  "Packed",
  "Shipped",
  "Out For Delivery",
  "Delivered",
];

export default function OrderTracking() {
  const { id } = useParams();
  const navigate = useNavigate();
  const order = useMemo(() => getOrderById(id), [id]);

  if (!order) {
    return (
      <div className="min-h-screen flex items-center justify-center px-4">
        <div className="rounded-3xl border border-dashed border-slate-300 bg-white p-10 text-center">
          <h2 className="text-2xl font-semibold">Order not found</h2>
          <p className="text-slate-500">We could not find an order matching that tracking ID.</p>
          <button
            onClick={() => navigate("/orders")}
            className="mt-6 rounded-2xl border border-slate-300 px-6 py-3 text-slate-700 hover:bg-slate-100 transition"
          >
            Back to Orders
          </button>
        </div>
      </div>
    );
  }

  const activeIndex = statusSteps.findIndex((step) => step === order.status);

  return (
    <div className="max-w-5xl mx-auto px-4 py-10">
      <div className="bg-white rounded-3xl border border-slate-200 p-8 shadow-sm">
        <div className="flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
          <div>
            <h1 className="text-3xl font-semibold">Track Your Order</h1>
            <p className="text-slate-500 mt-2">Order ID: <span className="font-medium">{order.id}</span></p>
          </div>
          <div className="text-right">
            <p className="text-slate-700">Payment method</p>
            <p className="font-semibold">{order.paymentMethod}</p>
          </div>
        </div>

        <div className="mt-10 space-y-6">
          {statusSteps.map((step, index) => {
            const isComplete = index <= activeIndex;
            return (
              <div key={step} className="flex items-start gap-4">
                <div className="flex flex-col items-center">
                  <div className={`h-5 w-5 rounded-full border-2 ${isComplete ? "border-primary bg-primary" : "border-slate-300 bg-white"}`} />
                  {index < statusSteps.length - 1 && <div className={`mt-1 h-16 w-px ${isComplete ? "bg-primary" : "bg-slate-200"}`} />}
                </div>
                <div>
                  <p className="font-semibold text-slate-900">{step}</p>
                  <p className="text-sm text-slate-500">{isComplete ? "Completed" : "Pending"}</p>
                </div>
              </div>
            );
          })}
        </div>

        <div className="mt-10 flex flex-col sm:flex-row gap-4">
          <button onClick={() => navigate("/orders")} className="rounded-2xl border border-slate-300 px-6 py-3 text-slate-700 hover:bg-slate-100 transition">
            Back to Orders
          </button>
          <button onClick={() => navigate("/products")} className="rounded-2xl bg-primary px-6 py-3 text-white hover:bg-pink-600 transition">
            Continue Shopping
          </button>
        </div>
      </div>
    </div>
  );
}
