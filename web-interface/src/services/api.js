import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para manejar errores
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error);
    throw new Error(error.response?.data?.message || error.message || 'Error de conexión');
  }
);

export const executeCommand = async (command) => {
  try {
    const response = await api.post('/api/execute', { command });
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const getKeystrokesData = async () => {
  try {
    const response = await api.get('/api/keystrokes');
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const getOptimizedLayout = async () => {
  try {
    const response = await api.get('/api/layout');
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const getSystemStatus = async () => {
  try {
    const response = await api.get('/api/status');
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const uploadFile = async (file) => {
  try {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await api.post('/api/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  } catch (error) {
    throw error;
  }
};

export default api; 