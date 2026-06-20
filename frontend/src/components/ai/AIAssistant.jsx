import React, { useState } from "react";
import axios from "axios";

export default function AIAssistant() {
  const [open, setOpen] = useState(false);
  const [query, setQuery] = useState("");
  const [answer, setAnswer] = useState("");
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(false);
  const handleClose = () => {
    setOpen(false);
    setQuery("");
    setAnswer("");
    setProducts([]);
    setLoading(false);
  };
  
  // ensure loading is cleared when closing
  const handleCloseReset = () => {
    handleClose();
  };

  const handleAsk = async () => {
    if (!query.trim()) return;

    try {
      setLoading(true);

      const res = await axios.post(
        "http://127.0.0.1:8000/api/ai/shopping-assistant",
        {
          query: query,
        }
      );

      setAnswer(res.data.answer || res.data.message || "");
      setProducts(res.data.products || []);
    } catch (error) {
      console.error(error);
      setAnswer("Unable to get response from AI Assistant.");
      setProducts([]);
    } finally {
      setLoading(false);
    }
  };

  // ensure loading is cleared when closing
  // include loading reset in handleClose
  // (update the existing handler to also clear loading)
  // modify handleClose above to reset loading

  return (
    <>
      <button
        onClick={() => { setQuery(''); setOpen(true); }}
        className="fixed bottom-6 right-6 z-40 bg-gradient-to-br from-primary to-accent text-white p-4 rounded-full shadow-lg hover:scale-105 transition-smooth"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          className="h-6 w-6"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth="2"
            d="M8 10h.01M12 10h.01M16 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
          />
        </svg>
      </button>

      {open && (
        <div className="fixed bottom-24 right-6 w-[400px] max-h-[80vh] bg-white rounded-xl shadow-2xl z-50 flex flex-col">
          {/* Header */}
          <div className="flex justify-between items-center border-b p-3">
            <h3 className="text-lg font-semibold">AI Assistant</h3>
            <button onClick={handleCloseReset} className="text-gray-500 hover:text-gray-700">✕</button>
          </div>

          {/* Scrollable Content Area */}
          <div className="flex-1 overflow-y-auto p-4 space-y-4">
            {answer && (
              <>
                <div className="p-3 bg-blue-50 rounded text-sm whitespace-pre-line border border-blue-200">
                  <strong className="text-blue-900">Assistant:</strong>
                  <br />
                  <span className="text-gray-800">{answer}</span>
                </div>
                <button
                  onClick={() => {
                    setQuery("");
                    setAnswer("");
                    setProducts([]);
                  }}
                  className="w-full bg-gray-200 text-gray-800 py-2 rounded hover:bg-gray-300 text-sm"
                >
                  New Search
                </button>
              </>
            )}

            {products.length > 0 && (
              <div>
                <h4 className="text-sm font-semibold mb-3 text-gray-800">Suggested Products</h4>
                <div className="grid gap-3">
                  {products.slice(0, 5).map((product) => (
                    <div key={product.product_id} className="rounded-lg border border-gray-200 p-3 bg-gray-50 hover:bg-gray-100 transition">
                      <div className="text-sm font-semibold text-gray-900">{product.product_name}</div>
                      <div className="text-xs text-gray-500 mt-1">{product.brand} • {product.category}</div>
                      {product.rating && <div className="text-xs text-yellow-600 mt-1">⭐ {product.rating.toFixed(1)}</div>}
                      <div className="mt-2 text-sm font-semibold text-gray-900">₹{product.price.toLocaleString()}</div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {!answer && !products.length && (
              <div className="text-center text-gray-400 text-sm py-4">
                Ask me anything about products...
              </div>
            )}
          </div>

          {/* Fixed Input Area */}
          <div className="border-t p-3 bg-white rounded-b-xl space-y-2">
            <textarea
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter' && e.ctrlKey) {
                  handleAsk();
                }
              }}
              placeholder="Ask something like: formal shirt"
              className="w-full border rounded p-2 text-sm resize-none focus:outline-none focus:ring-2 focus:ring-blue-500"
              rows="3"
            />

            <button
              onClick={handleAsk}
              disabled={loading || !query.trim()}
              className="w-full bg-blue-600 text-white py-2 rounded font-medium hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition text-sm"
            >
              {loading ? "Loading..." : "Ask AI"}
            </button>
          </div>
        </div>
      )}
    </>
  );
}