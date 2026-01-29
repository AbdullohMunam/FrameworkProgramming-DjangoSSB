<template>
  <div class="admin-login">
    <div class="admin-login__bg"></div>
    
    <div class="login-card animate-fade-in-up">
      <div class="login-card__header">
        <span class="login-card__icon">🛡️</span>
        <h2 class="login-card__title">Admin Login</h2>
        <p class="login-card__subtitle">SSB Academy Management System</p>
      </div>
      
      <div v-if="error" class="login-card__error">
        <svg class="login-card__error-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        {{ error }}
      </div>
      
      <form @submit.prevent="handleLogin" class="login-form">
        <div class="login-form__group">
          <label class="login-form__label">Username</label>
          <div class="login-form__input-wrapper">
            <svg class="login-form__icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
            </svg>
            <input v-model="username" type="text" required class="login-form__input" placeholder="Enter admin username" />
          </div>
        </div>
        
        <div class="login-form__group">
          <label class="login-form__label">Password</label>
          <div class="login-form__input-wrapper">
            <svg class="login-form__icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
            </svg>
            <input v-model="password" type="password" required class="login-form__input" placeholder="Enter password" />
          </div>
        </div>
        
        <button type="submit" :disabled="loading" class="login-form__submit">
          <span v-if="loading" class="login-form__spinner"></span>
          {{ loading ? 'Signing in...' : 'Sign in as Admin' }}
        </button>
      </form>
      
      <div class="login-card__footer">
        <router-link to="/login" class="login-card__link">
          ← Login sebagai User
        </router-link>
      </div>
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
    
    console.log('Login success, user data:', authStore.user)
    console.log('isAdmin:', authStore.isAdmin)
    
    if (!authStore.isAdmin) {
      error.value = 'Access denied. Admin credentials required.'
      await authStore.logout()
      return
    }
    
    router.push('/admin')
  } catch (err) {
    error.value = err.response?.data?.detail || 'Login gagal'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.admin-login {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1.5rem;
  position: relative;
}

.admin-login__bg {
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 50%, #1e3a8a 100%);
  background-size: 200% 200%;
  animation: gradientMove 8s ease infinite;
}

.admin-login__bg::before {
  content: '';
  position: absolute;
  inset: 0;
  background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.03'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
}

@keyframes gradientMove {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

.login-card {
  position: relative;
  background: white;
  padding: 2.5rem;
  border-radius: 1.5rem;
  box-shadow: 0 25px 80px rgba(0, 0, 0, 0.4);
  max-width: 420px;
  width: 100%;
}

.login-card__header {
  text-align: center;
  margin-bottom: 2rem;
}

.login-card__icon {
  font-size: 3rem;
  display: block;
  margin-bottom: 1rem;
}

.login-card__title {
  font-size: 1.75rem;
  font-weight: 800;
  color: #1e3a8a;
  margin-bottom: 0.25rem;
}

.login-card__subtitle {
  color: #64748b;
  font-size: 0.9rem;
}

.login-card__error {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: #fef2f2;
  border: 1px solid #fecaca;
  color: #dc2626;
  padding: 0.75rem 1rem;
  border-radius: 0.75rem;
  margin-bottom: 1.5rem;
  font-size: 0.9rem;
}

.login-card__error-icon {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
}

.login-form__group {
  margin-bottom: 1.25rem;
}

.login-form__label {
  display: block;
  font-weight: 600;
  color: #374151;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
}

.login-form__input-wrapper {
  position: relative;
}

.login-form__icon {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  width: 20px;
  height: 20px;
  color: #9ca3af;
}

.login-form__input {
  width: 100%;
  padding: 0.875rem 1rem 0.875rem 3rem;
  border: 2px solid #e5e7eb;
  border-radius: 0.75rem;
  font-size: 1rem;
  transition: all 0.3s;
  background: #f9fafb;
}

.login-form__input:focus {
  outline: none;
  border-color: #1e40af;
  background: white;
  box-shadow: 0 0 0 4px rgba(30, 64, 175, 0.1);
}

.login-form__submit {
  width: 100%;
  padding: 1rem;
  background: linear-gradient(135deg, #1e3a8a, #1e40af);
  color: white;
  border: none;
  border-radius: 0.75rem;
  font-size: 1rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  margin-top: 1.5rem;
}

.login-form__submit:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(30, 58, 138, 0.4);
}

.login-form__submit:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.login-form__spinner {
  width: 20px;
  height: 20px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.login-card__footer {
  text-align: center;
  margin-top: 1.5rem;
}

.login-card__link {
  color: #64748b;
  font-size: 0.9rem;
  text-decoration: none;
}

.login-card__link:hover {
  color: #1e40af;
}
</style>
