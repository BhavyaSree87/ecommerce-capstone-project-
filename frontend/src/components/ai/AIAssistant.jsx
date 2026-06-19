import React, { useState } from "react";
import axios from "axios";

export default function AIAssistant() {
  const [open, setOpen] = useState(false);
  const [query, setQuery] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);

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

      setAnswer(res.data.answer);
    } catch (error) {
      console.error(error);
      setAnswer("Unable to get response from AI Assistant.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <button
        onClick={() => setOpen(true)}
        className="fixed bottom-6 right-6 z-50 bg-gradient-to-br from-primary to-accent text-white p-4 rounded-full shadow-lg hover:scale-105 transition-smooth"
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
        <div className="fixed inset-0 z-50 flex items-end md:items-center justify-center">
          <div
            className="absolute inset-0 bg-black/40"
            onClick={() => setOpen(false)}
          ></div>

          <div className="bg-white rounded-t-lg md:rounded-lg w-full md:w-2/3 lg:w-1/3 p-6 relative z-50">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-lg font-semibold">
                AI Shopping Assistant
              </h3>

              <button
                onClick={() => setOpen(false)}
                className="text-gray-500"
              >
                Close
              </button>
            </div>

            <div className="space-y-4">
              <textarea
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Ask something like: I need clothes for a wedding"
                className="w-full border rounded p-3"
                rows="4"
              />

              <button
                onClick={handleAsk}
                disabled={loading}
                className="w-full bg-blue-600 text-white py-2 rounded"
              >
                {loading ? "Loading..." : "Ask AI"}
              </button>

              {answer && (
                <div className="p-3 bg-gray-100 rounded text-sm whitespace-pre-line">
                  <strong>Assistant:</strong>
                  <br />
                  {answer}
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </>
  );
}