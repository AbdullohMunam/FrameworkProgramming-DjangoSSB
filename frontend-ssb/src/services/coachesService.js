import api from './api'

export const coachesService = {
  async getCoaches(params = {}) {
    const response = await api.get('/coaches/', { params })
    return response.data
  },

  async getCoach(id) {
    const response = await api.get(`/coaches/${id}/`)
    return response.data
  },

  async createCoach(data) {
    const formData = new FormData()
    Object.keys(data).forEach(key => {
      if (data[key] !== null && data[key] !== undefined) {
        formData.append(key, data[key])
      }
    })
    const response = await api.post('/coaches/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    return response.data
  },

  async updateCoach(id, data) {
    const formData = new FormData()
    Object.keys(data).forEach(key => {
      if (data[key] !== null && data[key] !== undefined) {
        formData.append(key, data[key])
      }
    })
    const response = await api.put(`/coaches/${id}/`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    return response.data
  },

  async deleteCoach(id) {
    const response = await api.delete(`/coaches/${id}/`)
    return response.data
  }
}
