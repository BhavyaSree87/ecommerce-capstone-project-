import { API_PREFIX } from "./config";

const USERS_KEY = "ecom_users";
const SESSION_KEY = "ecom_auth_session";
const TOKEN_KEY = "ecom_jwt_token";
const ROLE_KEY = "ecom_user_role";

const API_BASE_URL = API_PREFIX; // API_PREFIX includes the /api path, e.g., http://127.0.0.1:8000/api

const parseStorage = (key) => {
  try {
    const value = window.localStorage.getItem(key);
    if (!value) return null;
    try {
      return JSON.parse(value);
    } catch {
      return value;
    }
  } catch {
    return null;
  }
};

const saveStorage = (key, value) => {
  if (typeof value === 'string') {
    window.localStorage.setItem(key, value);
  } else {
    window.localStorage.setItem(key, JSON.stringify(value));
  }
};

const formatApiError = async (response) => {
  try {
    const error = await response.json();
    const detail = error?.detail;

    if (typeof detail === 'string') {
      return detail;
    }

    if (Array.isArray(detail)) {
      const messages = detail.map((item) => {
        if (typeof item === 'string') return item;
        if (item?.msg) return item.msg;
        if (item?.message) return item.message;
        return JSON.stringify(item);
      }).filter(Boolean);

      if (messages.length > 0) {
        return messages.join(', ');
      }
    }

    if (typeof error.message === 'string') {
      return error.message;
    }

    return JSON.stringify(error);
  } catch {
    return response.statusText || 'Registration failed';
  }
};

const normalizeRole = (role) => {
  return typeof role === 'string' ? role.toLowerCase() : role;
};

const createToken = (user) => {
  return btoa(JSON.stringify({ email: user.email, issued: Date.now() }));
};

const loadUsers = () => parseStorage(USERS_KEY) || [];
const saveUsers = (users) => saveStorage(USERS_KEY, users);

export const register = async ({
  name,
  email,
  mobile,
  password,
  address,
  city,
  state,
  pincode
}) => {
  console.log("REGISTER PAYLOAD =", {
  name,
  email,
  mobile,
  password,
  address,
  city,
  state,
  pincode
});
  try {
    const response = await fetch(`${API_BASE_URL}/auth/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, email, mobile, password, address, city, state, pincode }),
    });

    if (!response.ok) {
      const message = await formatApiError(response);
      throw new Error(message || "Registration failed");
    }

    const data = await response.json();
    console.log("[AUTH SERVICE] Register response:", data);
    console.log("[AUTH SERVICE] User role:", data.user?.role);

    // Store JWT token and role
    saveStorage(TOKEN_KEY, data.access_token);
    window.localStorage.setItem('token', data.access_token);
    saveStorage(ROLE_KEY, normalizeRole(data.user?.role || "user"));
    window.localStorage.setItem('role', normalizeRole(data.user?.role || "user"));
    saveStorage(SESSION_KEY, { token: data.access_token, user: data.user });

    return { user: data.user, token: data.access_token };
  } catch (error) {
    console.error("[AUTH SERVICE] Register error:", error.message);
    throw error;
  }
};

export const login = async ({ email, password }) => {
  try {
    const response = await fetch(`${API_BASE_URL}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });

    if (!response.ok) {
      const message = await formatApiError(response);
      throw new Error(message || "Invalid email or password");
    }

    const data = await response.json();
    console.log("[AUTH SERVICE] Login response:", data);
    console.log("[AUTH SERVICE] User role from backend:", data.user?.role);
    console.log("[AUTH SERVICE] Storing token:", data.access_token?.substring(0, 20) + "...");
    console.log("[AUTH SERVICE] Storing role:", data.user?.role);

    // Store JWT token and role
    saveStorage(TOKEN_KEY, data.access_token);
    window.localStorage.setItem('token', data.access_token);
    saveStorage(ROLE_KEY, normalizeRole(data.user?.role || "user"));
    window.localStorage.setItem('role', normalizeRole(data.user?.role || "user"));
    saveStorage(SESSION_KEY, { token: data.access_token, user: data.user });

    console.log("[AUTH SERVICE] Token stored in localStorage:", window.localStorage.getItem('token')?.substring(0, 20));
    console.log("[AUTH SERVICE] Role stored in localStorage:", window.localStorage.getItem('role'));

    return { user: data.user, token: data.access_token };
  } catch (error) {
    console.error("[AUTH SERVICE] Login error:", error.message);
    throw error;
  }
};

export const logout = async () => {
  window.localStorage.removeItem(SESSION_KEY);
  window.localStorage.removeItem(TOKEN_KEY);
  window.localStorage.removeItem("token");
  window.localStorage.removeItem(ROLE_KEY);
  window.localStorage.removeItem("role");
  console.log("[AUTH SERVICE] Logout successful - cleared all tokens and role");
};

export const loadSession = () => {
  let session = parseStorage(SESSION_KEY);
  let token = parseStorage(TOKEN_KEY);
  let role = parseStorage(ROLE_KEY);

  if (!session && token) {
    session = { token, user: { role } };
  }

  if (!token && session?.token) {
    token = session.token;
  }

  if (!role) {
    role = parseStorage("role");
  }

  console.log("[AUTH SERVICE] Loading session - token exists:", !!token, "role:", role);

  if (session && session.user && role) {
    session.user.role = role;
  }

  if (token && !session) {
    session = { token, user: { role } };
  }

  return session;
};

export const updateProfile = async (updatedProfile) => {
  try {
    const token = parseStorage(TOKEN_KEY);
    if (!token) {
      throw new Error("No authentication token found");
    }

    const response = await fetch(`${API_BASE_URL}/users/profile`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`,
      },
      body: JSON.stringify(updatedProfile),
    });

    if (!response.ok) {
      const message = await formatApiError(response);
      throw new Error(message || "Failed to update profile");
    }

    const data = await response.json();
    const session = loadSession();
    saveStorage(SESSION_KEY, { ...session, user: data });
    
    return data;
  } catch (error) {
    console.error("[AUTH SERVICE] Update profile error:", error.message);
    throw error;
  }
};

export const changePassword = async ({ email, oldPassword, newPassword }) => {
  try {
    const token = parseStorage(TOKEN_KEY);
    if (!token) {
      throw new Error("No authentication token found");
    }

    const response = await fetch(`${API_BASE_URL}/users/change-password`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`,
      },
      body: JSON.stringify({ email, oldPassword, newPassword }),
    });

    if (!response.ok) {
      const message = await formatApiError(response);
      throw new Error(message || "Failed to change password");
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error("[AUTH SERVICE] Change password error:", error.message);
    throw error;
  }
};

export const saveSession = (user, token) => {
  saveStorage(SESSION_KEY, { token, user });
  saveStorage(TOKEN_KEY, token);
  window.localStorage.setItem('token', token);
  saveStorage(ROLE_KEY, normalizeRole(user?.role || "user"));
  window.localStorage.setItem('role', normalizeRole(user?.role || "user"));
};

export const getToken = () => {
  return parseStorage(TOKEN_KEY) || window.localStorage.getItem('token') || null;
};

export const getRole = () => {
  return normalizeRole(parseStorage(ROLE_KEY));
};

export const isAdmin = () => {
  const role = parseStorage(ROLE_KEY);
  console.log("[AUTH SERVICE] Checking if admin - role:", role);
  return role === "admin";
};
