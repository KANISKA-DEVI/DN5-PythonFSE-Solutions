// ============================================================
// Centralised Axios API Client
// File: src/api/apiClient.js
// ============================================================
import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'https://jsonplaceholder.typicode.com',
  timeout: 5000,
  headers: { 'Content-Type': 'application/json' }
});

// Request interceptor — attach auth token to every request
apiClient.interceptors.request.use(config => {
  const mockToken = 'mock-jwt-token-12345';
  config.headers['Authorization'] = `Bearer ${mockToken}`;
  console.log(`[API] ${config.method?.toUpperCase()} ${config.baseURL}${config.url}`);
  return config;
});

// Response interceptor — return data directly, standardise errors
apiClient.interceptors.response.use(
  response => response.data,   // Return just the data, not the full Axios wrapper
  error => {
    const message    = error.response?.data?.message || error.message || 'Unknown error';
    const statusCode = error.response?.status || 0;
    throw { message, statusCode };   // Standardised error object
  }
);

export default apiClient;