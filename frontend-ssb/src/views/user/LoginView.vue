<template>
  <div class="min-h-screen bg-gray-50 flex items-center justify-center px-4">
    <div class="bg-white p-8 rounded-lg shadow-lg max-w-md w-full">
      <h2 class="text-3xl font-bold text-center mb-8">Login User</h2>
      
      <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
        {{ error }}
      </div>
      
      <form @submit.prevent="handleLogin" class="space-y-4">
        <div>
          <label class="block text-sm font-medium mb-1">Username</label>
          <input v-model="username" type="text" required class="w-full px-3 py-2 border rounded-lg" />
        </div>
        
        <div>
          <label class="block text-sm font-medium mb-1">Password</label>
          <input v-model="password" type="password" required class="w-full px-3 py-2 border rounded-lg" />
        </div>
        
        <button 
          type="submit"
          :disabled="loading"
          class="w-full bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700"
        >
          {{ loading ? 'Loading...' : 'Login' }}
        </button>
      </form>
      
      <p class="text-center mt-4 text-sm">
        Belum punya akun? 
        <router-link to="/register" class="text-blue-600 hover:underline">Daftar</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const username = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

async function handleLogin() {
  error.value = ''
  loading.value = true
  
  try {
    await authStore.login(username.value, password.value)
    router.push('/profile')
  } catch (err) {
    error.value = err.response?.data?.detail || 'Login gagal. Periksa username dan password Anda.'
  } finally {
    loading.value = false
  }
}
</script>
