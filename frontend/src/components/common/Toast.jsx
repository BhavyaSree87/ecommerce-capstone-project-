import React from "react";

export default function Toast({ message, type = "success", onClose }) {
  return (
    <div className={`fixed bottom-6 right-6 z-50 rounded-2xl px-5 py-4 shadow-lg ${type === "error" ? "bg-rose-500 text-white" : "bg-slate-900 text-white"}`}>
      <div className="flex items-start gap-3">
        <div className="text-xl">{type === "error" ? "⚠️" : "✅"}</div>
        <div className="space-y-1">
          <div className="font-semibold">{type === "error" ? "Error" : "Success"}</div>
          <div className="text-sm leading-relaxed">{message}</div>
        </div>
        <button onClick={onClose} className="ml-auto text-sm opacity-70 hover:opacity-100">Close</button>
      </div>
    </div>
  );
}
