const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

const getAuthHeaders = () => {
  const session = localStorage.getItem("ecom_auth_session");
  const tokenFromSession = session ? JSON.parse(session).token : null;
  const token = tokenFromSession || localStorage.getItem("ecom_jwt_token") || localStorage.getItem("token");

  if (!token) {
    return { "Content-Type": "application/json" };
  }

  return {
    "Authorization": `Bearer ${token}`,
    "Content-Type": "application/json",
  };
};

const normalizeListResponse = (response) => {
  if (Array.isArray(response)) return response;
  if (!response) return [];
  if (Array.isArray(response.items)) return response.items;
  if (Array.isArray(response.data)) return response.data;
  if (Array.isArray(response.results)) return response.results;
  return [];
};

const request = async (path, options = {}) => {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      ...getAuthHeaders(),
      ...options.headers,
    },
    ...options,
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`API request failed: ${response.status} - ${errorText}`);
  }

  return response.json();
};


const getDashboardStats = async () => {
  try {
    return await request("/api/dashboard/stats");
  } catch (error) {
    console.error("Dashboard stats error:", error);
    throw error;
  }
};


const getAllProducts = async (page = 1, pageSize = 100) => {
  try {
    const response = await request(`/api/products/all?page=${page}&page_size=${pageSize}`);
    return normalizeListResponse(response);
  } catch (error) {
    console.error("Get products error:", error);
    throw error;
  }
};

const getProductById = async (id) => {
  try {
    return await request(`/api/products/${id}`);
  } catch (error) {
    console.error("Get product error:", error);
    throw error;
  }
};

const createProduct = async (productData) => {
  try {
    return await request("/api/products/add", {
      method: "POST",
      body: JSON.stringify(productData),
    });
  } catch (error) {
    console.error("Create product error:", error);
    throw error;
  }
};

const updateProduct = async (id, productData) => {
  try {
    return await request(`/api/products/${id}`, {
      method: "PUT",
      body: JSON.stringify(productData),
    });
  } catch (error) {
    console.error("Update product error:", error);
    throw error;
  }
};

const deleteProduct = async (id) => {
  try {
    return await request(`/api/products/${id}`, {
      method: "DELETE",
    });
  } catch (error) {
    console.error("Delete product error:", error);
    throw error;
  }
};


const getAllCategories = async () => {
  try {
    const response = await request("/api/categories/all");
    return normalizeListResponse(response);
  } catch (error) {
    console.error("Get categories error:", error);
    throw error;
  }
};

const createCategory = async (categoryData) => {
  try {
    return await request("/api/categories/add", {
      method: "POST",
      body: JSON.stringify(categoryData),
    });
  } catch (error) {
    console.error("Create category error:", error);
    throw error;
  }
};

const updateCategory = async (id, categoryData) => {
  try {
    return await request(`/api/categories/${id}`, {
      method: "PUT",
      body: JSON.stringify(categoryData),
    });
  } catch (error) {
    console.error("Update category error:", error);
    throw error;
  }
};

const deleteCategory = async (id) => {
  try {
    return await request(`/api/categories/${id}`, {
      method: "DELETE",
    });
  } catch (error) {
    console.error("Delete category error:", error);
    throw error;
  }
};


const getAllOrders = async () => {
  try {
    const response = await request("/api/orders/all");
    return normalizeListResponse(response);
  } catch (error) {
    console.error("Get orders error:", error);
    throw error;
  }
};

const getOrderById = async (id) => {
  try {
    return await request(`/api/orders/${id}`);
  } catch (error) {
    console.error("Get order error:", error);
    throw error;
  }
};

const updateOrderStatus = async (id, status) => {
  try {
    return await request(`/api/orders/${id}/status`, {
      method: "PUT",
      body: JSON.stringify({ status }),
    });
  } catch (error) {
    console.error("Update order status error:", error);
    throw error;
  }
};


const getAllUsers = async () => {
  try {
    const response = await request("/api/users/all");
    return normalizeListResponse(response);
  } catch (error) {
    console.error("Get users error:", error);
    throw error;
  }
};

const getUserById = async (id) => {
  try {
    return await request(`/api/users/${id}`);
  } catch (error) {
    console.error("Get user error:", error);
    throw error;
  }
};

const deleteUser = async (id) => {
  try {
    return await request(`/api/users/${id}`, {
      method: "DELETE",
    });
  } catch (error) {
    console.error("Delete user error:", error);
    throw error;
  }
};

export default {
  
  getDashboardStats,
  
  
  getAllProducts,
  getProductById,
  createProduct,
  updateProduct,
  deleteProduct,
  
  
  getAllCategories,
  createCategory,
  updateCategory,
  deleteCategory,
  
  
  getAllOrders,
  getOrderById,
  updateOrderStatus,
  
  
  getAllUsers,
  getUserById,
  deleteUser,
};
