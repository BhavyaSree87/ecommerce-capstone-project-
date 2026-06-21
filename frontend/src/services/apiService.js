import httpClient from "./httpClient";

const get = async (path, params = {}) => {
  const response = await httpClient.get(path, { params });
  return response.data;
};

const post = async (path, body, options = {}) => {
  const response = await httpClient.post(path, body, options);
  return response.data;
};

const put = async (path, body, options = {}) => {
  const response = await httpClient.put(path, body, options);
  return response.data;
};

const del = async (path, options = {}) => {
  const response = await httpClient.delete(path, options);
  return response.data;
};

export default {
  get,
  post,
  put,
  delete: del,
};
