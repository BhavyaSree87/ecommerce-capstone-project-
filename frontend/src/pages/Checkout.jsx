import React, { useContext, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import { ShopContext } from "../context/ShopContext";
import { calculateCartTotals } from "../services/cartService";

const initialAddress = {
  name: "",
  line1: "",
  city: "",
  state: "",
  pincode: "",
  phone: "",
};

export default function Checkout() {
  const { cartItems } = useContext(ShopContext);
  const navigate = useNavigate();
  const [shipping, setShipping] = useState(initialAddress);
  const [billing, setBilling] = useState(initialAddress);
  const [sameBilling, setSameBilling] = useState(true);
  const [coupon, setCoupon] = useState("");
  const [selectedMethod, setSelectedMethod] = useState("Cash On Delivery");

  const totals = useMemo(() => calculateCartTotals(cartItems), [cartItems]);

  const handleSubmit = (e) => {
    e.preventDefault();
    navigate("/payment", {
      state: {
        shipping,
        billing,
        sameBilling,
        coupon,
        paymentMethod: selectedMethod,
        totals,
      },
    });
  };

  if (cartItems.length === 0) {
    return (
      <div className="min-h-screen flex items-center justify-center px-4">
        <div className="rounded-3xl border border-dashed border-slate-300 bg-white p-10 text-center max-w-md">
          <h2 className="text-2xl font-semibold mb-2">Your checkout cart is empty</h2>
          <p className="text-slate-500">Add items to your cart before proceeding to checkout.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-6">Checkout</h1>
      <div className="grid gap-6 lg:grid-cols-[1.5fr_0.9fr]">
        <form onSubmit={handleSubmit} className="space-y-6 bg-white rounded-3xl border border-slate-200 p-6 shadow-sm">
          <section className="space-y-4">
            <h2 className="text-xl font-semibold">Shipping Address</h2>
            {Object.keys(shipping).map((field) => (
              <div key={field}>
                <label className="block text-sm font-medium text-slate-700 capitalize">{field}</label>
                <input
                  name={field}
                  value={shipping[field]}
                  onChange={(e) => setShipping((prev) => ({ ...prev, [field]: e.target.value }))}
                  className="w-full border rounded-xl px-4 py-3 mt-2"
                />
              </div>
            ))}
          </section>

          <section className="space-y-4">
            <div className="flex items-center gap-3">
              <input type="checkbox" checked={sameBilling} onChange={() => setSameBilling(!sameBilling)} className="h-4 w-4" />
              <label className="text-sm text-slate-700">Billing address same as shipping</label>
            </div>
            {!sameBilling && (
              <div className="grid gap-4 md:grid-cols-2">
                {Object.keys(billing).map((field) => (
                  <div key={field}>
                    <label className="block text-sm font-medium text-slate-700 capitalize">{field}</label>
                    <input
                      name={field}
                      value={billing[field]}
                      onChange={(e) => setBilling((prev) => ({ ...prev, [field]: e.target.value }))}
                      className="w-full border rounded-xl px-4 py-3 mt-2"
                    />
                  </div>
                ))}
              </div>
            )}
          </section>

          <section className="space-y-4">
            <h2 className="text-xl font-semibold">Delivery Options</h2>
            <div className="space-y-2 text-sm text-slate-600">
              <p>Standard delivery charges: ₹99</p>
              <p>Orders above ₹5000 qualify for free delivery.</p>
            </div>
          </section>

          <section className="space-y-4">
            <h2 className="text-xl font-semibold">Coupon</h2>
            <div className="flex gap-3">
              <input value={coupon} onChange={(e) => setCoupon(e.target.value)} placeholder="Enter coupon code" className="w-full border rounded-xl px-4 py-3" />
              <button type="button" className="rounded-2xl bg-slate-100 px-5 py-3 text-sm text-slate-700">Apply</button>
            </div>
          </section>

          <section className="space-y-4">
            <h2 className="text-xl font-semibold">Payment Method</h2>
            <div className="space-y-3">
              {['Cash On Delivery', 'UPI', 'Credit Card', 'Debit Card', 'Net Banking'].map((method) => (
                <label key={method} className="flex items-center gap-3 rounded-2xl border border-slate-200 bg-slate-50 p-4 cursor-pointer">
                  <input
                    type="radio"
                    name="paymentMethod"
                    value={method}
                    checked={selectedMethod === method}
                    onChange={() => setSelectedMethod(method)}
                    className="h-4 w-4 text-primary focus:ring-primary"
                  />
                  <div>
                    <div className="font-medium">{method}</div>
                    <div className="text-slate-500 text-sm">
                      {method === 'Cash On Delivery'
                        ? 'Pay when your order is delivered.'
                        : method === 'UPI'
                        ? 'Pay securely using your UPI ID.'
                        : method === 'Net Banking'
                        ? 'Choose your bank to complete payment.'
                        : 'Enter your card details to pay securely.'}
                    </div>
                  </div>
                </label>
              ))}
            </div>
          </section>

          <button className="w-full bg-primary text-white rounded-3xl py-4 font-semibold hover:bg-pink-600 transition">Continue to Payment</button>
        </form>

        <aside className="space-y-6">
          <div className="bg-white rounded-3xl border border-slate-200 p-6 shadow-sm">
            <h2 className="text-xl font-semibold mb-4">Order Summary</h2>
            <div className="space-y-3 text-sm">
              <div className="flex justify-between"><span>Items</span><span>{cartItems.length}</span></div>
              <div className="flex justify-between"><span>Subtotal</span><span>₹{totals.subtotal}</span></div>
              <div className="flex justify-between"><span>Discount</span><span>- ₹{totals.discount}</span></div>
              <div className="flex justify-between"><span>Tax</span><span>₹{totals.tax}</span></div>
              <div className="flex justify-between"><span>Delivery</span><span>₹{totals.shipping}</span></div>
            </div>
            <div className="border-t border-slate-200 mt-5 pt-4 flex justify-between text-lg font-semibold">
              <span>Total</span>
              <span>₹{totals.total}</span>
            </div>
          </div>
        </aside>
      </div>
    </div>
  );
}
