import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authService } from '@/services/authService'
import { TOKEN_KEY, USER_KEY } from '@/utils/constants'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem(TOKEN_KEY))
  const userStr = localStorage.getItem(USER_KEY)
  const user = ref(userStr && userStr !== 'undefined' ? JSON.parse(userStr) : null)
  const loading = ref(false)
  const error = ref(null)

  const isAuthenticated = computed(() => !!token.value)

  async function login(username, password) {
    loading.value = true
    error.value = null
    try {
      const data = await authService.login(username, password)
      token.value = data.token
      // Backend returns user_id, username, email separately, not as user object
      user.value = {
        id: data.user_id,
        username: data.username,
        email: data.email || ''
      }
      localStorage.setItem(TOKEN_KEY, data.token)
      localStorage.setItem(USER_KEY, JSON.stringify(user.value))
      return true
    } catch (err) {
      error.value = err.response?.data?.detail || 'Login failed'
      return false
    } finally {
      loading.value = false
    }
  }

  async function logout() {
    loading.value = true
    try {
      await authService.logout()
    } catch (err) {
      console.error('Logout error:', err)
    } finally {
      token.value = null
      user.value = null
      localStorage.removeItem(TOKEN_KEY)
      localStorage.removeItem(USER_KEY)
      loading.value = false
    }
  }

  async function checkAuth() {
    if (!token.value) return false
    
    try {
      const data = await authService.getProfile()
      user.value = data
      localStorage.setItem(USER_KEY, JSON.stringify(data))
      return true
    } catch (err) {
      token.value = null
      user.value = null
      localStorage.removeItem(TOKEN_KEY)
      localStorage.removeItem(USER_KEY)
      return false
    }
  }

  return {
    token,
    user,
    loading,
    error,
    isAuthenticated,
    login,
    logout,
    checkAuth
  }
})
