import React from 'react';
import AdminButton from '../common/AdminButton';

export default function DataTable({ 
  columns, 
  data, 
  onEdit, 
  onDelete, 
  loading = false,
  emptyMessage = 'No data available',
}) {
  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="w-10 h-10 rounded-full border-4 border-slate-200 border-t-primary animate-spin" />
      </div>
    );
  }

  if (!data || data.length === 0) {
    return (
      <div className="rounded-lg border border-slate-200 bg-white p-8 text-center">
        <p className="text-slate-500">{emptyMessage}</p>
      </div>
    );
  }

  return (
    <div className="overflow-x-auto rounded-lg border border-slate-200 bg-white">
      <table className="w-full text-sm">
        <thead>
          <tr className="border-b border-slate-200 bg-slate-50">
            {columns.map((col) => (
              <th
                key={col.key}
                className={`px-6 py-3 text-left font-semibold text-slate-700 ${col.width || ''}`}
              >
                {col.label}
              </th>
            ))}
            {(onEdit || onDelete) && (
              <th className="px-6 py-3 text-left font-semibold text-slate-700">Actions</th>
            )}
          </tr>
        </thead>
        <tbody>
          {data.map((row, idx) => (
            <tr
              key={row.id || idx}
              className="border-b border-slate-200 hover:bg-slate-50 transition"
            >
              {columns.map((col) => (
                <td key={`${row.id}-${col.key}`} className="px-6 py-4">
                  {col.render ? col.render(row[col.key], row) : row[col.key]}
                </td>
              ))}
              {(onEdit || onDelete) && (
                <td className="px-6 py-4">
                  <div className="flex items-center gap-2">
                    {onEdit && (
                      <AdminButton
                        variant="secondary"
                        size="sm"
                        onClick={() => onEdit(row)}
                      >
                        Edit
                      </AdminButton>
                    )}
                    {onDelete && (
                      <AdminButton
                        variant="danger"
                        size="sm"
                        onClick={() => {
                          if (confirm('Are you sure you want to delete this item?')) {
                            onDelete(row.id);
                          }
                        }}
                      >
                        Delete
                      </AdminButton>
                    )}
                  </div>
                </td>
              )}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
