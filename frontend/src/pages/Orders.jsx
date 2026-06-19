import React, { useContext, useEffect, useState } from "react";
import { AuthContext } from "../context/AuthContext";
import { getOrdersForUser } from "../services/orderService";
import { Link } from "react-router-dom";
import Loader from "../components/common/Loader";

export default function Orders() {
  const { user } = useContext(AuthContext);
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!user) return;
    const fetchOrders = async () => {
      setLoading(true);
      const result = await getOrdersForUser(user.email);
      setOrders(result);
      setLoading(false);
    };
    fetchOrders();
  }, [user]);

  if (loading) {
    return <Loader />;
  }

  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-3xl font-bold">My Orders</h1>
          <p className="text-slate-500">Track your order history and reorder easily.</p>
        </div>
        <Link to="/profile" className="text-primary">My Profile</Link>
      </div>

      {orders.length === 0 ? (
        <div className="rounded-3xl border border-dashed border-slate-300 bg-white p-10 text-center">
          <h2 className="text-2xl font-semibold mb-2">No orders yet</h2>
          <p className="text-slate-500">Place an order and it will appear here.</p>
        </div>
      ) : (
        <div className="space-y-6">
          {orders.map((order) => (
            <div key={order.id} className="bg-white rounded-3xl border border-slate-200 p-6 shadow-sm">
              <div className="flex flex-col md:flex-row gap-4 md:items-center justify-between">
                <div>
                  <h2 className="text-xl font-semibold">Order {order.id}</h2>
                  <p className="text-sm text-slate-500">{new Date(order.createdAt).toLocaleString()}</p>
                </div>
                <div className="text-slate-700">
                  <p>Status: <span className="font-semibold">{order.status}</span></p>
                  <p>Total: ₹{order.totals.total}</p>
                </div>
              </div>
              <div className="mt-4 flex flex-wrap gap-3 text-sm text-slate-600">
                <span>{order.items.length} items</span>
                <span>{order.paymentMethod}</span>
              </div>
              <div className="mt-4 flex flex-wrap gap-3">
                <Link to={`/order/${order.id}`} className="text-primary text-sm">View details</Link>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
