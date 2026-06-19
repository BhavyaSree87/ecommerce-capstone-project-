import React from "react";
import { useLocation } from "react-router-dom";
import AppRoutes from "./routes/AppRoutes";

import Navbar from "./components/common/Navbar";
import Footer from "./components/common/Footer";
import AIAssistant from "./components/ai/AIAssistant";

export default function App() {
  const location = useLocation();
  const isAdminPath = location.pathname.startsWith("/admin");

  return (
    <div className="min-h-screen flex flex-col bg-slate-50 text-slate-900">
      {!isAdminPath && <Navbar />}

      <main className="flex-1">
        <AppRoutes />
      </main>

      {!isAdminPath && <Footer />}
      {!isAdminPath && <AIAssistant />}
    </div>
  );
}