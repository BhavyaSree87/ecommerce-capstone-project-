import React from 'react';

export default function Alert({ type = 'info', message, onClose, icon = null }) {
  const colors = {
    success: 'bg-emerald-50 border-emerald-200 text-emerald-700',
    error: 'bg-red-50 border-red-200 text-red-700',
    warning: 'bg-yellow-50 border-yellow-200 text-yellow-700',
    info: 'bg-blue-50 border-blue-200 text-blue-700',
  };

  return (
    <div className={`rounded-lg border p-4 flex items-start justify-between ${colors[type]}`}>
      <div className="flex items-start gap-3">
        {icon && <div className="flex-shrink-0">{icon}</div>}
        <p className="text-sm font-medium">{message}</p>
      </div>
      {onClose && (
        <button onClick={onClose} className="text-current hover:opacity-70 transition">
          ✕
        </button>
      )}
    </div>
  );
}
