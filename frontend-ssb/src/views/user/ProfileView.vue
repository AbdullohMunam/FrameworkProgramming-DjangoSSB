<template>
  <div class="min-h-screen bg-gray-50">
    <nav class="bg-white shadow">
      <div class="container mx-auto px-4 py-4 flex justify-between items-center">
        <h1 class="text-2xl font-bold text-blue-600">SSB Academy</h1>
        <div class="flex items-center gap-4">
          <router-link to="/profile" class="text-blue-600 font-semibold">Profile</router-link>
          <router-link to="/schedules" class="hover:text-blue-600">Schedules</router-link>
          <router-link to="/team" class="hover:text-blue-600">My Team</router-link>
          <button @click="handleLogout" class="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700">
            Logout
          </button>
        </div>
      </div>
    </nav>
    
    <div class="container mx-auto px-4 py-8">
      <h2 class="text-3xl font-bold mb-8">My Profile</h2>
      
      <div v-if="loading" class="text-center py-8">
        <p>Loading...</p>
      </div>
      
      <div v-else-if="profile" class="bg-white p-8 rounded-lg shadow max-w-2xl">
        <div class="mb-6 flex justify-center">
          <img v-if="profile.photo" :src="profile.photo" class="w-32 h-32 rounded-full object-cover" />
          <div v-else class="w-32 h-32 rounded-full bg-gray-200 flex items-center justify-center">
            <svg class="w-16 h-16 text-gray-400" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clip-rule="evenodd" />
            </svg>
          </div>
        </div>
        
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-1">Username</label>
          <p class="text-lg">{{ profile.username }}</p>
        </div>
        
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-1">Email</label>
          <p class="text-lg">{{ profile.email }}</p>
        </div>
        
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-1">Nama</label>
          <p class="text-lg">{{ profile.name || '-' }}</p>
        </div>
        
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-1">Umur</label>
          <p class="text-lg">{{ profile.age || '-' }}</p>
        </div>
        
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-1">Posisi</label>
          <p class="text-lg">{{ profile.position || '-' }}</p>
        </div>
        
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-1">Kelompok</label>
          <p class="text-lg">{{ profile.group_name || 'Belum ada kelompok' }}</p>
        </div>
        
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-1">Status</label>
          <span 
            :class="{
              'bg-yellow-100 text-yellow-800': profile.status === 'pending',
              'bg-green-100 text-green-800': profile.status === 'approved',
              'bg-red-100 text-red-800': profile.status === 'rejected'
            }"
            class="inline-block px-3 py-1 rounded-full text-sm font-semibold"
          >
            {{ profile.status }}
          </span>
        </div>
        
        <button 
          @click="openEditModal" 
          class="w-full bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700 mt-6"
        >
          Edit Profile
        </button>
      </div>
    </div>
    
    <!-- Edit Modal -->
    <div v-if="showEditModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 px-4">
      <div class="bg-white p-8 rounded-lg shadow-lg max-w-md w-full max-h-[90vh] overflow-y-auto">
        <h2 class="text-2xl font-bold mb-4">Edit Profile</h2>
        
        <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {{ error }}
        </div>
        
        <form @submit.prevent="handleSave" class="space-y-4">
          <div>
            <label class="block text-sm font-medium mb-1">Nama Lengkap *</label>
            <input v-model="form.name" type="text" required class="w-full px-3 py-2 border rounded-lg" />
          </div>
          
          <div>
            <label class="block text-sm font-medium mb-1">Umur *</label>
            <input v-model.number="form.age" type="number" required min="5" max="50" class="w-full px-3 py-2 border rounded-lg" />
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
            <input @change="handleFileChange" type="file" accept="image/*" class="w-full px-3 py-2 border rounded-lg" />
            <p v-if="profile.photo" class="text-xs text-gray-500 mt-1">Kosongkan jika tidak ingin mengubah foto</p>
          </div>
          
          <div class="flex gap-2">
            <button 
              type="submit"
              :disabled="saving"
              class="flex-1 bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700"
            >
              {{ saving ? 'Menyimpan...' : 'Simpan' }}
            </button>
            <button 
              type="button"
              @click="closeEditModal"
              class="flex-1 bg-gray-300 py-3 rounded-lg font-semibold hover:bg-gray-400"
            >
              Batal
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { playersService } from '@/services'

const router = useRouter()
const authStore = useAuthStore()
const profile = ref(null)
const loading = ref(true)
const showEditModal = ref(false)
const saving = ref(false)
const error = ref('')

const form = ref({
  name: '',
  age: '',
  position: '',
  photo: null
})

async function loadProfile() {
  try {
    profile.value = await playersService.getMyProfile()
  } catch (error) {
    console.error('Failed to load profile:', error)
  } finally {
    loading.value = false
  }
}

function openEditModal() {
  form.value = {
    name: profile.value.name || '',
    age: profile.value.age || '',
    position: profile.value.position || '',
    photo: null
  }
  error.value = ''
  showEditModal.value = true
}

function closeEditModal() {
  showEditModal.value = false
  form.value = { name: '', age: '', position: '', photo: null }
  error.value = ''
}

function handleFileChange(event) {
  const file = event.target.files[0]
  form.value.photo = file || null
}

async function handleSave() {
  error.value = ''
  saving.value = true
  
  try {
    await playersService.updateProfile(form.value)
    showEditModal.value = false
    await loadProfile() // Reload profile to show updated data
  } catch (err) {
    const errorData = err.response?.data
    if (errorData) {
      error.value = errorData.detail || 
                    errorData.name?.[0] || 
                    errorData.age?.[0] || 
                    errorData.position?.[0] || 
                    'Gagal menyimpan profil. Periksa data Anda.'
    } else {
      error.value = 'Gagal menyimpan profil. Periksa koneksi Anda.'
    }
  } finally {
    saving.value = false
  }
}

async function handleLogout() {
  await authStore.logout()
  router.push('/login')
}

onMounted(loadProfile)
</script>
