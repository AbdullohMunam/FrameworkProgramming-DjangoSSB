import api from './api'

export const playersService = {
  async getPlayers(params = {}) {
    const response = await api.get('/players/', { params })
    return response.data
  },

  async getPlayer(id) {
    const response = await api.get(`/players/${id}/`)
    return response.data
  },

  async createPlayer(data) {
    const formData = new FormData()
    Object.keys(data).forEach(key => {
      if (data[key] !== null && data[key] !== undefined) {
        formData.append(key, data[key])
      }
    })
    const response = await api.post('/players/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    return response.data
  },

  async updatePlayer(id, data) {
    const formData = new FormData()
    Object.keys(data).forEach(key => {
      if (data[key] !== null && data[key] !== undefined) {
        formData.append(key, data[key])
      }
    })
    const response = await api.put(`/players/${id}/`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    return response.data
  },

  async deletePlayer(id) {
    const response = await api.delete(`/players/${id}/`)
    return response.data
  }
}
