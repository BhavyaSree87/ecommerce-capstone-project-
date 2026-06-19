const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

const request = async (path, options = {}) => {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      "Content-Type": "application/json",
    },
    ...options,
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`API request failed: ${response.status} ${response.statusText} - ${errorText}`);
  }

  return response.json();
};

const get = async (path) => request(path, { method: "GET" });

export default {
  get,
};
