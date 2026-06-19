import React, { useContext, useMemo } from "react";
import { useNavigate } from "react-router-dom";
import CartItem from "../components/cart/CartItem";
import { ShopContext } from "../context/ShopContext";
import { calculateCartTotals } from "../services/cartService";
import Loader from "../components/common/Loader";

export default function Cart() {
  const {
    cartItems,
    increaseQty,
    decreaseQty,
    removeFromCart,
    loading,
  } = useContext(ShopContext);
  const navigate = useNavigate();

  const totals = useMemo(() => calculateCartTotals(cartItems), [cartItems]);

  if (loading) {
    return <Loader />;
  }

  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-6">Shopping Cart</h1>

      {cartItems.length === 0 ? (
        <div className="rounded-3xl border border-dashed border-slate-300 bg-white p-10 text-center">
          <h2 className="text-2xl font-semibold mb-2">Your cart is empty</h2>
          <p className="text-slate-500">Add products from the store to begin shopping.</p>
        </div>
      ) : (
        <div className="grid gap-6 lg:grid-cols-[1fr_360px]">
          <div className="space-y-4">
            {cartItems.map((item) => (
              <CartItem
                key={item.id}
                item={item}
                increaseQty={increaseQty}
                decreaseQty={decreaseQty}
                removeItem={removeFromCart}
              />
            ))}
          </div>

          <div className="bg-white rounded-3xl border border-slate-200 p-6 shadow-sm">
            <h2 className="text-xl font-semibold mb-4">Order Summary</h2>
            <div className="space-y-3 text-sm text-slate-600">
              <div className="flex justify-between">
                <span>Subtotal</span>
                <span>₹{totals.subtotal}</span>
              </div>
              <div className="flex justify-between">
                <span>Discount</span>
                <span>- ₹{totals.discount}</span>
              </div>
              <div className="flex justify-between">
                <span>Tax</span>
                <span>₹{totals.tax}</span>
              </div>
              <div className="flex justify-between">
                <span>Delivery</span>
                <span>₹{totals.shipping}</span>
              </div>
            </div>
            <div className="border-t border-slate-200 my-4" />
            <div className="flex items-center justify-between text-2xl font-bold">
              <span>Total</span>
              <span>₹{totals.total}</span>
            </div>
            <button
              type="button"
              onClick={() => navigate("/checkout")}
              className="mt-6 w-full bg-primary text-white py-3 rounded-2xl font-medium hover:bg-pink-600 transition"
            >
              Proceed to Checkout
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
