<template>
  <div class="min-h-screen bg-gray-50 flex items-center justify-center px-4 py-8">
    <div class="bg-white p-8 rounded-lg shadow-lg max-w-2xl w-full">
      <h2 class="text-3xl font-bold text-center mb-8">Daftar SSB Academy</h2>
      
      <div v-if="success" class="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded mb-4">
        {{ successMessage }}
      </div>
      
      <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
        {{ error }}
      </div>
      
      <form v-if="!success" @submit.prevent="handleRegister" class="space-y-4">
        <div class="grid md:grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium mb-1">Nama Lengkap *</label>
            <input v-model="form.name" type="text" required class="w-full px-3 py-2 border rounded-lg" 
                   placeholder="Nama lengkap" />
          </div>
          
          <div>
            <label class="block text-sm font-medium mb-1">Umur *</label>
            <input v-model.number="form.age" type="number" required min="5" max="50" 
                   class="w-full px-3 py-2 border rounded-lg" placeholder="Umur" />
          </div>
        </div>
        
        <div>
          <label class="block text-sm font-medium mb-1">Posisi *</label>
          <select v-model="form.position" required class="w-full px-3 py-2 border rounded-lg">
            <option value="">Pilih Posisi</option>
            <option value="Goalkeeper">Goalkeeper</option>
            <option value="Defender">Defender</option>
            <option value="Midfielder">Midfielder</option>
            <option value="Forward">Forward</option>
          </select>
        </div>
        
        <div>
          <label class="block text-sm font-medium mb-1">Foto (Opsional)</label>
          <input @change="handleFileChange" type="file" accept="image/*" 
                 class="w-full px-3 py-2 border rounded-lg" />
          <p class="text-xs text-gray-500 mt-1">Format: JPG, PNG. Max 2MB</p>
        </div>
        
        <div class="border-t pt-4 mt-4">
          <h3 class="font-semibold mb-3">Akun Login</h3>
          
          <div class="grid md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium mb-1">Username *</label>
              <input v-model="form.username" type="text" required class="w-full px-3 py-2 border rounded-lg" 
                     placeholder="Username untuk login" />
            </div>
            
            <div>
              <label class="block text-sm font-medium mb-1">Email *</label>
              <input v-model="form.email" type="email" required class="w-full px-3 py-2 border rounded-lg" 
                     placeholder="Email untuk notifikasi" />
            </div>
          </div>
          
          <div class="grid md:grid-cols-2 gap-4 mt-4">
            <div>
              <label class="block text-sm font-medium mb-1">Password *</label>
              <input v-model="form.password" type="password" required minlength="6" 
                     class="w-full px-3 py-2 border rounded-lg" placeholder="Minimal 6 karakter" />
            </div>
            
            <div>
              <label class="block text-sm font-medium mb-1">Konfirmasi Password *</label>
              <input v-model="form.password_confirm" type="password" required minlength="6" 
                     class="w-full px-3 py-2 border rounded-lg" placeholder="Ulangi password" />
            </div>
          </div>
        </div>
        
        <button 
          type="submit"
          :disabled="loading"
          class="w-full bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700 disabled:opacity-50 mt-6"
        >
          {{ loading ? 'Mendaftar...' : 'Daftar Sekarang' }}
        </button>
      </form>
      
      <p class="text-center mt-4 text-sm">
        Sudah punya akun? 
        <router-link to="/login" class="text-blue-600 hover:underline">Login</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { authService } from '@/services'

const form = ref({
  name: '',
  age: '',
  position: '',
  photo: null,
  username: '',
  email: '',
  password: '',
  password_confirm: ''
})

const loading = ref(false)
const error = ref('')
const success = ref(false)
const successMessage = ref('')

function handleFileChange(event) {
  const file = event.target.files[0]
  if (file) {
    if (file.size > 2 * 1024 * 1024) {
      error.value = 'Ukuran file maksimal 2MB'
      event.target.value = ''
      return
    }
    form.value.photo = file
  }
}

async function handleRegister() {
  error.value = ''
  
  if (form.value.password !== form.value.password_confirm) {
    error.value = 'Password tidak cocok'
    return
  }
  
  loading.value = true
  
  try {
    const formData = new FormData()
    formData.append('name', form.value.name)
    formData.append('age', form.value.age)
    formData.append('position', form.value.position)
    formData.append('username', form.value.username)
    formData.append('email', form.value.email)
    formData.append('password', form.value.password)
    formData.append('password_confirm', form.value.password_confirm)
    
    if (form.value.photo) {
      formData.append('photo', form.value.photo)
    }
    
    await authService.register(formData)
    success.value = true
    successMessage.value = 'Pendaftaran berhasil! Mohon tunggu persetujuan admin. Email notifikasi akan dikirim setelah disetujui.'
    form.value = { 
      name: '', age: '', position: '', photo: null,
      username: '', email: '', password: '', password_confirm: '' 
    }
  } catch (err) {
    const errorData = err.response?.data
    if (errorData) {
      error.value = errorData.detail || 
                    errorData.email?.[0] || 
                    errorData.username?.[0] || 
                    errorData.password?.[0] ||
                    errorData.age?.[0] ||
                    errorData.position?.[0] ||
                    errorData.name?.[0] ||
                    'Pendaftaran gagal. Periksa data Anda.'
    } else {
      error.value = 'Pendaftaran gagal. Periksa koneksi Anda.'
    }
  } finally {
    loading.value = false
  }
}
</script>
