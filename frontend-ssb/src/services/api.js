import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Request interceptor - add token
api.interceptors.request.use(
  (config) => {
    // Get token based on current path
    const isAdminPath = window.location.pathname.startsWith('/admin')
    const tokenKey = isAdminPath ? 'admin_token' : 'user_token'
    const token = localStorage.getItem(tokenKey)
    
    if (token) {
      config.headers.Authorization = `Token ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

// Response interceptor - handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Clear both storages on 401
      localStorage.removeItem('admin_token')
      localStorage.removeItem('admin_user')
      localStorage.removeItem('user_token')
      localStorage.removeItem('user_user')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default api
