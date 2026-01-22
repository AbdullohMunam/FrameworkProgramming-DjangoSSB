<template>
  <AppLayout>
    <div class="max-w-md mx-auto">
      <BaseCard>
        <div class="text-center mb-8">
          <div class="w-20 h-20 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full mx-auto flex items-center justify-center mb-4">
            <span class="text-white font-bold text-3xl">SSB</span>
          </div>
          <h1 class="text-3xl font-bold text-gray-900 dark:text-white mb-2">Welcome Back</h1>
          <p class="text-gray-600 dark:text-gray-400">Sign in to your account</p>
        </div>

        <form @submit.prevent="handleLogin" class="space-y-6">
          <BaseInput
            id="username"
            v-model="username"
            label="Username"
            placeholder="Enter your username"
            required
            :error="error"
          />

          <BaseInput
            id="password"
            v-model="password"
            type="password"
            label="Password"
            placeholder="Enter your password"
            required
          />

          <BaseButton
            type="submit"
            :loading="loading"
            full-width
          >
            Sign In
          </BaseButton>
        </form>
      </BaseCard>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useToast } from 'vue-toastification'
import AppLayout from '@/components/layout/AppLayout.vue'
import BaseCard from '@/components/common/BaseCard.vue'
import BaseInput from '@/components/common/BaseInput.vue'
import BaseButton from '@/components/common/BaseButton.vue'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()
const toast = useToast()

const username = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

const handleLogin = async () => {
  error.value = ''
  loading.value = true

  try {
    const success = await authStore.login(username.value, password.value)
    
    if (success) {
      toast.success('Login successful!')
      const redirect = route.query.redirect || '/'
      router.push(redirect)
    } else {
      error.value = authStore.error || 'Login failed'
      toast.error(error.value)
    }
  } catch (err) {
    error.value = 'An error occurred during login'
    toast.error(error.value)
  } finally {
    loading.value = false
  }
}
</script>
