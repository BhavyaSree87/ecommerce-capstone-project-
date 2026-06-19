import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";

import Home from "../pages/Home";
import Categories from "../pages/Categories";
import Products from "../pages/Products";
import ProductDetails from "../pages/ProductDetails";
import Wishlist from "../pages/Wishlist";
import Cart from "../pages/Cart";
import Login from "../pages/Login";
import Register from "../pages/Register";
import Profile from "../pages/Profile";
import Orders from "../pages/Orders";
import OrderDetails from "../pages/OrderDetails";
import Checkout from "../pages/Checkout";
import Payment from "../pages/Payment";
import OrderSuccess from "../pages/OrderSuccess";
import OrderTracking from "../pages/OrderTracking";
import SearchResults from "../pages/SearchResults";
import NotFound from "../pages/NotFound";
import ProtectedRoute from "../components/common/ProtectedRoute";
import ProtectedAdminRoute from "../components/common/ProtectedAdminRoute";
import AdminRoutes from "../admin/AdminRoutes";

const AppRoutes = () => {
  return (
    <Routes>

      <Route path="/" element={<Home />} />

      <Route path="/products" element={<Products />} />

      <Route path="/categories" element={<Categories />} />

      <Route path="/wishlist" element={<Wishlist />} />
      <Route path="/cart" element={<Cart />} />
      <Route path="/product/:id" element={<ProductDetails />} />
      <Route path="/search" element={<SearchResults />} />
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route path="/profile" element={<ProtectedRoute><Profile /></ProtectedRoute>} />
      <Route path="/orders" element={<ProtectedRoute><Orders /></ProtectedRoute>} />
      <Route path="/order/:id" element={<ProtectedRoute><OrderDetails /></ProtectedRoute>} />
      <Route path="/checkout" element={<ProtectedRoute><Checkout /></ProtectedRoute>} />
      <Route path="/payment" element={<ProtectedRoute><Payment /></ProtectedRoute>} />
      <Route path="/order-success" element={<ProtectedRoute><OrderSuccess /></ProtectedRoute>} />
      <Route path="/track-order/:id" element={<ProtectedRoute><OrderTracking /></ProtectedRoute>} />
      
      {/* Admin Routes */}
      <Route path="/admin/*" element={<ProtectedAdminRoute><AdminRoutes /></ProtectedAdminRoute>} />
      
      <Route path="*" element={<NotFound />} />
    </Routes>
  );
};

export default AppRoutes;