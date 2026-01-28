<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Hero Section -->
    <div class="bg-gradient-to-r from-blue-600 to-purple-600 text-white">
      <div class="container mx-auto px-4 py-20">
        <h1 class="text-5xl font-bold mb-4">SSB Academy</h1>
        <p class="text-xl mb-8">Sekolah Sepak Bola Terbaik untuk Generasi Juara</p>
        <div class="space-x-4">
          <router-link 
            to="/register"
            class="bg-white text-blue-600 px-8 py-3 rounded-lg font-semibold hover:bg-gray-100 inline-block"
          >
            Daftar Sekarang
          </router-link>
          <router-link 
            to="/login"
            class="border-2 border-white px-8 py-3 rounded-lg font-semibold hover:bg-white hover:text-blue-600 inline-block"
          >
            Login
          </router-link>
        </div>
      </div>
    </div>

    <!-- Stats Section -->
    <div class="container mx-auto px-4 py-16">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div class="bg-white p-6 rounded-lg shadow text-center">
          <div class="text-4xl font-bold text-blue-600">{{ stats.players }}</div>
          <div class="text-gray-600">Pemain</div>
        </div>
        <div class="bg-white p-6 rounded-lg shadow text-center">
          <div class="text-4xl font-bold text-green-600">{{ stats.coaches }}</div>
          <div class="text-gray-600">Pelatih</div>
        </div>
        <div class="bg-white p-6 rounded-lg shadow text-center">
          <div class="text-4xl font-bold text-purple-600">{{ stats.groups }}</div>
          <div class="text-gray-600">Kelompok</div>
        </div>
        <div class="bg-white p-6 rounded-lg shadow text-center">
          <div class="text-4xl font-bold text-orange-600">{{ stats.schedules }}</div>
          <div class="text-gray-600">Jadwal</div>
        </div>
      </div>
    </div>

    <!-- Featured Coaches -->
    <div class="container mx-auto px-4 py-16">
      <h2 class="text-3xl font-bold mb-8">Pelatih Unggulan</h2>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div v-for="coach in featuredCoaches" :key="coach.id" class="bg-white p-6 rounded-lg shadow">
          <h3 class="text-xl font-bold mb-2">{{ coach.name }}</h3>
          <p class="text-gray-600">{{ coach.license_level }}</p>
        </div>
      </div>
    </div>

    <!-- Footer -->
    <footer class="bg-gray-800 text-white py-8 mt-16">
      <div class="container mx-auto px-4 text-center">
        <p>&copy; 2026 SSB Academy. All rights reserved.</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { playersService, coachesService, groupsService, schedulesService } from '@/services'

const stats = ref({
  players: 0,
  coaches: 0,
  groups: 0,
  schedules: 0
})

const featuredCoaches = ref([])

onMounted(async () => {
  try {
    const [playersData, coachesData, groupsData, schedulesData] = await Promise.all([
      playersService.getPlayers(),
      coachesService.getCoaches(),
      groupsService.getGroups(),
      schedulesService.getSchedules()
    ])
    
    stats.value = {
      players: playersData.results?.length || playersData.length || 0,
      coaches: coachesData.results?.length || coachesData.length || 0,
      groups: groupsData.results?.length || groupsData.length || 0,
      schedules: schedulesData.results?.length || schedulesData.length || 0
    }
    
    const allCoaches = coachesData.results || coachesData
    featuredCoaches.value = allCoaches.slice(0, 3)
  } catch (error) {
    console.error('Failed to load data:', error)
  }
})
</script>
