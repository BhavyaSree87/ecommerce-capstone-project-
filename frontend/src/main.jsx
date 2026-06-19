import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter } from "react-router-dom";

import App from "./App";
import "./index.css";

import AuthProvider from "./context/AuthContext";
import ShopProvider from "./context/ShopContext";

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <BrowserRouter>
      <ShopProvider>
        <AuthProvider>
          <App />
        </AuthProvider>
      </ShopProvider>
    </BrowserRouter>
  </React.StrictMode>
);