import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authService } from '@/services'

export const useAuthStore = defineStore('auth', () => {
  // Separate storage for admin and user
  const getStorageKey = (key) => {
    const path = window.location.pathname
    const isAdminPath = path.startsWith('/admin')
    return isAdminPath ? `admin_${key}` : `user_${key}`
  }
  
  const token = ref(localStorage.getItem(getStorageKey('token')) || null)
  const user = ref(JSON.parse(localStorage.getItem(getStorageKey('user')) || 'null'))

  const isAuthenticated = computed(() => !!token.value)
  const isAdmin = computed(() => user.value?.is_staff || user.value?.is_superuser || false)

  async function login(username, password) {
    const data = await authService.login(username, password)
    const storagePrefix = (data.is_staff || data.is_superuser) ? 'admin_' : 'user_'
    
    token.value = data.token
    user.value = {
      id: data.user_id,
      username: data.username,
      email: data.email,
      is_staff: data.is_staff,
      is_superuser: data.is_superuser
    }
    localStorage.setItem(storagePrefix + 'token', data.token)
    localStorage.setItem(storagePrefix + 'user', JSON.stringify(user.value))
    return data
  }

  async function register(formData) {
    return await authService.register(formData)
  }

  async function logout() {
    await authService.logout()
    const key = getStorageKey('token')
    const userKey = getStorageKey('user')
    
    token.value = null
    user.value = null
    localStorage.removeItem(key)
    localStorage.removeItem(userKey)
  }

  return {
    token,
    user,
    isAuthenticated,
    isAdmin,
    login,
    register,
    logout
  }
})
