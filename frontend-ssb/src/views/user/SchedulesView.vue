<template>
  <div class="min-h-screen bg-gray-50">
    <nav class="bg-white shadow">
      <div class="container mx-auto px-4 py-4 flex justify-between items-center">
        <h1 class="text-2xl font-bold text-blue-600">SSB Academy</h1>
        <div class="flex items-center gap-4">
          <router-link to="/profile" class="hover:text-blue-600">Profile</router-link>
          <router-link to="/schedules" class="text-blue-600 font-semibold">Schedules</router-link>
          <router-link to="/team" class="hover:text-blue-600">My Team</router-link>
          <button @click="handleLogout" class="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700">
            Logout
          </button>
        </div>
      </div>
    </nav>
    
    <div class="container mx-auto px-4 py-8">
      <div class="mb-6">
        <h2 class="text-3xl font-bold">Training Schedules</h2>
        <p v-if="userGroup" class="text-gray-600 mt-2">Jadwal untuk kelompok: <span class="font-semibold">{{ userGroup }}</span></p>
        <p v-else class="text-red-600 mt-2">Anda belum ditugaskan ke kelompok manapun</p>
      </div>
      
      <div v-if="loading" class="text-center py-8">
        <p>Loading schedules...</p>
      </div>
      
      <div v-else-if="schedules.length === 0" class="bg-white p-8 rounded-lg shadow text-center">
        <svg class="w-16 h-16 mx-auto text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
        </svg>
        <p class="text-gray-600 text-lg">{{ userGroup ? 'Belum ada jadwal latihan untuk kelompok Anda' : 'Anda belum ditugaskan ke kelompok' }}</p>
      </div>
      
      <div v-else class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div v-for="schedule in schedules" :key="schedule.id" class="bg-white p-6 rounded-lg shadow">
          <h3 class="text-xl font-semibold mb-2">{{ schedule.group_name }}</h3>
          <div class="text-gray-600 space-y-1">
            <p><span class="font-medium">Date:</span> {{ formatDate(schedule.date) }}</p>
            <p><span class="font-medium">Time:</span> {{ schedule.time }}</p>
          </div>
        </div>
        
        <div v-if="schedules.length === 0" class="col-span-full text-center py-8 text-gray-500">
          No schedules available
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { schedulesService, playersService } from '@/services'

const router = useRouter()
const authStore = useAuthStore()
const schedules = ref([])
const loading = ref(true)
const userGroup = ref(null)

async function loadSchedules() {
  try {
    // Get user's profile to know their group
    const profile = await playersService.getMyProfile()
    userGroup.value = profile.group_name
    
    // Get all schedules
    const response = await schedulesService.getSchedules()
    const allSchedules = response.results || response || []
    
    // Filter schedules by user's group
    if (profile.group) {
      schedules.value = allSchedules.filter(schedule => schedule.group === profile.group)
    } else {
      schedules.value = [] // No group assigned
    }
  } catch (error) {
    console.error('Failed to load schedules:', error)
    schedules.value = []
  } finally {
    loading.value = false
  }
}

function formatDate(dateStr) {
  return new Date(dateStr).toLocaleDateString('id-ID', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

async function handleLogout() {
  await authStore.logout()
  router.push('/login')
}

onMounted(loadSchedules)
</script>
