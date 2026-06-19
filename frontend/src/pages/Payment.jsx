import React, { useContext, useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";
import { ShopContext } from "../context/ShopContext";
import paymentService from "../services/paymentService";
import { placeOrder } from "../services/orderService";

const availableBanks = [
  "HDFC Bank",
  "State Bank of India",
  "ICICI Bank",
  "Axis Bank",
  "Kotak Mahindra Bank",
  "Punjab National Bank",
];

export default function Payment() {
  const location = useLocation();
  const navigate = useNavigate();
  const { user } = useContext(AuthContext);
  const { cartItems } = useContext(ShopContext);
  const [paymentState, setPaymentState] = useState(null);
  const [paymentMethod, setPaymentMethod] = useState("Cash On Delivery");
  const [paymentDetails, setPaymentDetails] = useState({
    upiId: "",
    cardNumber: "",
    cardHolder: "",
    expiry: "",
    cvv: "",
    bank: "",
  });
  const [error, setError] = useState(null);
  const [processing, setProcessing] = useState(false);

  useEffect(() => {
    if (!location.state || !user) {
      navigate("/cart", { replace: true });
      return;
    }

    setPaymentState(location.state);
    setPaymentMethod(location.state.paymentMethod || "Cash On Delivery");
  }, [location.state, navigate, user]);

  const handleInput = (field, value) => {
    setPaymentDetails((prev) => ({ ...prev, [field]: value }));
    setError(null);
  };

  const handlePayment = async () => {
    if (!paymentState) return;

    setProcessing(true);
    setError(null);

    try {
      await paymentService.simulatePayment({
        method: paymentMethod,
        details: paymentDetails,
        amount: paymentState.totals.total,
      });

      const order = await placeOrder({
        user,
        items: cartItems,
        shippingAddress: paymentState.shipping,
        billingAddress: paymentState.sameBilling ? paymentState.shipping : paymentState.billing,
        paymentMethod,
        totals: paymentState.totals,
        coupon: paymentState.coupon,
      });

      navigate("/order-success", { state: { order } });
    } catch (err) {
      setError(err.message || "Unable to complete payment. Please try again.");
    } finally {
      setProcessing(false);
    }
  };

  if (!paymentState) {
    return null;
  }

  const isCOD = paymentMethod === "Cash On Delivery";
  const isUPI = paymentMethod === "UPI";
  const isCard = paymentMethod === "Credit Card" || paymentMethod === "Debit Card";
  const isNetBanking = paymentMethod === "Net Banking";
  const buttonLabel = isCOD ? "Place Order" : "Pay Now";

  return (
    <div className="max-w-5xl mx-auto px-4 py-8">
      <div className="bg-white rounded-3xl border border-slate-200 p-6 shadow-sm">
        <h1 className="text-3xl font-bold mb-4">Payment</h1>

        <div className="grid gap-6 lg:grid-cols-[1.2fr_0.8fr]">
          <section className="space-y-6">
            <div className="rounded-3xl border border-slate-200 bg-slate-50 p-5">
              <h2 className="text-xl font-semibold mb-4">Select Payment Method</h2>
              <div className="space-y-3">
                {["Cash On Delivery", "UPI", "Credit Card", "Debit Card", "Net Banking"].map((method) => (
                  <label key={method} className="flex items-center gap-3 rounded-2xl border border-slate-200 bg-white px-4 py-4 cursor-pointer">
                    <input
                      type="radio"
                      name="paymentMethod"
                      value={method}
                      checked={paymentMethod === method}
                      onChange={() => setPaymentMethod(method)}
                      className="h-4 w-4 text-primary"
                    />
                    <div>
                      <div className="font-medium">{method}</div>
                      <p className="text-sm text-slate-500">
                        {method === "Cash On Delivery"
                          ? "Pay when your order is delivered."
                          : method === "UPI"
                          ? "Secure payment using your UPI ID."
                          : method === "Net Banking"
                          ? "Select your bank to finish checkout."
                          : "Enter your card details for a secure payment."}
                      </p>
                    </div>
                  </label>
                ))}
              </div>
            </div>

            <div className="rounded-3xl border border-slate-200 bg-slate-50 p-5">
              <h2 className="text-xl font-semibold mb-4">Payment Details</h2>
              {isCOD && (
                <div className="rounded-3xl bg-white border border-slate-200 p-5 text-slate-700">
                  <p className="font-semibold mb-2">Cash On Delivery</p>
                  <p>Pay when your order is delivered.</p>
                </div>
              )}

              {isUPI && (
                <div className="space-y-4">
                  <label className="block text-sm font-medium text-slate-700">UPI ID</label>
                  <input
                    value={paymentDetails.upiId}
                    onChange={(e) => handleInput("upiId", e.target.value)}
                    placeholder="example@bank"
                    className="w-full rounded-2xl border border-slate-300 px-4 py-3"
                  />
                </div>
              )}

              {isCard && (
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-slate-700">Card Number</label>
                    <input
                      value={paymentDetails.cardNumber}
                      onChange={(e) => handleInput("cardNumber", e.target.value)}
                      placeholder="1234 5678 9012 3456"
                      className="w-full rounded-2xl border border-slate-300 px-4 py-3"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-slate-700">Card Holder Name</label>
                    <input
                      value={paymentDetails.cardHolder}
                      onChange={(e) => handleInput("cardHolder", e.target.value)}
                      placeholder="Name on card"
                      className="w-full rounded-2xl border border-slate-300 px-4 py-3"
                    />
                  </div>
                  <div className="grid gap-4 md:grid-cols-2">
                    <div>
                      <label className="block text-sm font-medium text-slate-700">Expiry Date</label>
                      <input
                        value={paymentDetails.expiry}
                        onChange={(e) => handleInput("expiry", e.target.value)}
                        placeholder="MM/YY"
                        className="w-full rounded-2xl border border-slate-300 px-4 py-3"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-slate-700">CVV</label>
                      <input
                        value={paymentDetails.cvv}
                        onChange={(e) => handleInput("cvv", e.target.value)}
                        placeholder="123"
                        type="password"
                        className="w-full rounded-2xl border border-slate-300 px-4 py-3"
                      />
                    </div>
                  </div>
                </div>
              )}

              {isNetBanking && (
                <div className="space-y-4">
                  <label className="block text-sm font-medium text-slate-700">Select Bank</label>
                  <select
                    value={paymentDetails.bank}
                    onChange={(e) => handleInput("bank", e.target.value)}
                    className="w-full rounded-2xl border border-slate-300 px-4 py-3"
                  >
                    <option value="">Choose your bank</option>
                    {availableBanks.map((bank) => (
                      <option key={bank} value={bank}>{bank}</option>
                    ))}
                  </select>
                </div>
              )}
            </div>

            {error && <div className="rounded-2xl bg-rose-100 border border-rose-200 p-4 text-rose-700">{error}</div>}

            <button
              type="button"
              onClick={handlePayment}
              disabled={processing}
              className="w-full rounded-3xl bg-primary py-4 text-white font-semibold hover:bg-pink-600 transition disabled:opacity-70"
            >
              {processing ? `${buttonLabel}...` : buttonLabel}
            </button>
          </section>

          <aside className="rounded-3xl border border-slate-200 bg-slate-50 p-6 text-slate-700">
            <h2 className="text-xl font-semibold mb-4">Order Summary</h2>
            <div className="space-y-3 text-sm">
              <div className="flex justify-between"><span>Items</span><span>{cartItems.length}</span></div>
              <div className="flex justify-between"><span>Delivery Address</span><span>{paymentState.shipping.city}</span></div>
              <div className="flex justify-between"><span>Payment Method</span><span>{paymentMethod}</span></div>
              <div className="flex justify-between"><span>Total</span><span className="font-semibold">₹{paymentState.totals.total}</span></div>
            </div>
          </aside>
        </div>
      </div>
    </div>
  );
}
