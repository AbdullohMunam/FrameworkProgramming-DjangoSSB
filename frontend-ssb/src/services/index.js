import api from './api'

export const authService = {
  async register(data) {
    const response = await api.post('/auth/register/', data)
    return response.data
  },

  async login(username, password) {
    const response = await api.post('/auth/login/', { username, password })
    return response.data
  },

  async logout() {
    await api.post('/auth/logout/')
    // Don't remove storage here, let auth store handle it
  }
}

export const playersService = {
  async getPlayers() {
    const response = await api.get('/players/')
    return response.data
  },

  async getPending() {
    const response = await api.get('/players/pending/')
    return response.data
  },

  async approve(id, groupId) {
    const response = await api.post(`/players/${id}/approve/`, { group: groupId })
    return response.data
  },

  async reject(id) {
    const response = await api.post(`/players/${id}/reject/`)
    return response.data
  },

  async getMyProfile() {
    const response = await api.get('/players/me/')
    return response.data
  },

  async updateProfile(data) {
    const formData = new FormData()
    Object.keys(data).forEach(key => {
      if (data[key] !== null && data[key] !== undefined) {
        formData.append(key, data[key])
      }
    })
    const response = await api.put('/players/me/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    return response.data
  },

  async updatePlayer(id, data) {
    const response = await api.patch(`/players/${id}/`, data)
    return response.data
  },

  async deletePlayer(id) {
    const response = await api.delete(`/players/${id}/`)
    return response.data
  }
}

export const coachesService = {
  async getCoaches() {
    const response = await api.get('/coaches/')
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
      if (data[key] !== null && data[key] !== undefined && data[key] !== '') {
        formData.append(key, data[key])
      }
    })
    const response = await api.patch(`/coaches/${id}/`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    return response.data
  },

  async deleteCoach(id) {
    const response = await api.delete(`/coaches/${id}/`)
    return response.data
  }
}

export const groupsService = {
  async getGroups() {
    const response = await api.get('/groups/')
    return response.data
  },

  async createGroup(data) {
    const response = await api.post('/groups/', data)
    return response.data
  },

  async updateGroup(id, data) {
    const response = await api.patch(`/groups/${id}/`, data)
    return response.data
  },

  async deleteGroup(id) {
    const response = await api.delete(`/groups/${id}/`)
    return response.data
  }
}

export const schedulesService = {
  async getSchedules() {
    const response = await api.get('/schedules/')
    return response.data
  },

  async createSchedule(data) {
    const response = await api.post('/schedules/', data)
    return response.data
  },

  async updateSchedule(id, data) {
    const response = await api.patch(`/schedules/${id}/`, data)
    return response.data
  },

  async deleteSchedule(id) {
    const response = await api.delete(`/schedules/${id}/`)
    return response.data
  }
}
