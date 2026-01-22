import api from './api'

export const authService = {
  async login(username, password) {
    const response = await api.post('/auth/login/', { username, password })
    return response.data
  },

  async logout() {
    try {
      await api.post('/auth/logout/')
    } catch (error) {
      console.error('Logout error:', error)
    }
  },

  async getProfile() {
    const response = await api.get('/auth/profile/')
    return response.data
  }
}
