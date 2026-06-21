import { API_BASE_URL } from "./config";
import { getToken } from "./authService";

const getAuthHeaders = () => {
  const token = getToken();

  if (!token) {
    return { "Content-Type": "application/json" };
  }

  return {
    "Authorization": `Bearer ${token}`,
    "Content-Type": "application/json",
  };
};

const normalizeEntity = (entity) => {
  if (!entity || Array.isArray(entity) || typeof entity !== 'object') return entity;
  const normalized = { ...entity };
  if (normalized.product_id !== undefined) normalized.id = normalized.product_id;
  if (normalized.category_id !== undefined) normalized.id = normalized.category_id;
  if (normalized.order_id !== undefined && normalized.id === undefined) normalized.id = normalized.order_id;
  if (normalized.user_id !== undefined && normalized.id === undefined && normalized.username) normalized.id = normalized.user_id;
  if (normalized.created_at !== undefined) {
    if (normalized.order_date === undefined) normalized.order_date = normalized.created_at;
    if (normalized.createdAt === undefined) normalized.createdAt = normalized.created_at;
  }
  if (normalized.product_name !== undefined && normalized.name === undefined) {
    normalized.name = normalized.product_name;
  }
  if (normalized.category_name !== undefined && normalized.name === undefined) {
    normalized.name = normalized.category_name;
  }
  return normalized;
};

const normalizeListResponse = (response) => {
  let items = [];
  if (Array.isArray(response)) items = response;
  else if (response?.items && Array.isArray(response.items)) items = response.items;
  else if (response?.data && Array.isArray(response.data)) items = response.data;
  else if (response?.results && Array.isArray(response.results)) items = response.results;
  return items.map(normalizeEntity);
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
    const payload = {
      product_name: productData.product_name,
      description: productData.description,
      category: productData.category,
      brand: productData.brand,
      price: parseFloat(productData.price) || 0,
      stock: parseInt(productData.stock) || 0,
      rating: productData.rating ? parseFloat(productData.rating) : null,
      discount: productData.discount ? parseFloat(productData.discount) : 0,
      image_url: productData.image_url || null,
    };

    return await request("/api/products/add", {
      method: "POST",
      body: JSON.stringify(payload),
    });
  } catch (error) {
    console.error("Create product error:", error);
    throw error;
  }
};

const updateProduct = async (id, productData) => {
  try {
    const payload = {
      product_name: productData.product_name,
      description: productData.description,
      category: productData.category,
      brand: productData.brand,
      price: parseFloat(productData.price) || 0,
      stock: parseInt(productData.stock) || 0,
      rating: productData.rating ? parseFloat(productData.rating) : null,
      discount: productData.discount ? parseFloat(productData.discount) : 0,
      image_url: productData.image_url || null,
    };

    return await request(`/api/products/update/${id}`, {
      method: "PUT",
      body: JSON.stringify(payload),
    });
  } catch (error) {
    console.error("Update product error:", error);
    throw error;
  }
};

const deleteProduct = async (id) => {
  try {
    return await request(`/api/products/delete/${id}`, {
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
    return await request(`/api/categories/update/${id}`, {
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
    return await request(`/api/categories/delete/${id}`, {
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
    return await request(`/api/orders/status/${id}`, {
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
    return await request(`/api/users/delete/${id}`, {
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
