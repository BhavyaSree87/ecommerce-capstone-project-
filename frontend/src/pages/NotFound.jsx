import React from "react";
import { Link } from "react-router-dom";

export default function NotFound() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-100 px-4 py-16">
      <div className="max-w-2xl w-full rounded-3xl border border-slate-200 bg-white p-10 text-center shadow-sm">
        <div className="text-8xl font-bold text-primary">404</div>
        <h1 className="text-3xl font-semibold mt-4">Page not found</h1>
        <p className="mt-3 text-slate-500">The page you're looking for doesn’t exist or has been moved.</p>
        <Link to="/" className="mt-8 inline-flex rounded-2xl bg-primary px-6 py-3 text-white font-semibold hover:bg-pink-600 transition">
          Go to homepage
        </Link>
      </div>
    </div>
  );
}
