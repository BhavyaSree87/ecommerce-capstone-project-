import axios from "axios";
import { getToken } from "./authService";
import { API_BASE_URL } from "./config";

const httpClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

httpClient.interceptors.request.use(
  (config) => {
    const token = getToken();
    if (token) {
      config.headers = config.headers || {};
      config.headers.Authorization = `Bearer ${token}`;
      console.debug("[httpClient] Attaching Authorization header", config.headers.Authorization?.slice(0, 30) + "...");
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

httpClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      console.error("[httpClient] Response error", error.response.status, error.response.data);
    } else {
      console.error("[httpClient] Network or unknown error", error.message);
    }
    return Promise.reject(error);
  }
);

export default httpClient;
