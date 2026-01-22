import api from './api'

export const groupsService = {
  async getGroups(params = {}) {
    const response = await api.get('/groups/', { params })
    return response.data
  },

  async getGroup(id) {
    const response = await api.get(`/groups/${id}/`)
    return response.data
  },

  async createGroup(data) {
    const response = await api.post('/groups/', data)
    return response.data
  },

  async updateGroup(id, data) {
    const response = await api.put(`/groups/${id}/`, data)
    return response.data
  },

  async deleteGroup(id) {
    const response = await api.delete(`/groups/${id}/`)
    return response.data
  }
}
