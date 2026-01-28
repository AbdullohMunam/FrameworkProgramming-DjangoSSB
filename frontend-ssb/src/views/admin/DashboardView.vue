<template>
  <AdminLayout>
    <h1 class="text-3xl font-bold mb-8">Admin Dashboard</h1>
    
    <!-- Stats Cards -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-6 mb-8">
      <div class="bg-gradient-to-r from-yellow-500 to-yellow-600 text-white p-6 rounded-lg shadow">
        <div class="text-4xl font-bold">{{ stats.pending }}</div>
        <div class="text-sm opacity-90">Pending</div>
      </div>
      <div class="bg-gradient-to-r from-blue-500 to-blue-600 text-white p-6 rounded-lg shadow">
        <div class="text-4xl font-bold">{{ stats.players }}</div>
        <div class="text-sm opacity-90">Total Players</div>
      </div>
      <div class="bg-gradient-to-r from-green-500 to-green-600 text-white p-6 rounded-lg shadow">
        <div class="text-4xl font-bold">{{ stats.coaches }}</div>
        <div class="text-sm opacity-90">Total Coaches</div>
      </div>
      <div class="bg-gradient-to-r from-purple-500 to-purple-600 text-white p-6 rounded-lg shadow">
        <div class="text-4xl font-bold">{{ stats.groups }}</div>
        <div class="text-sm opacity-90">Total Groups</div>
      </div>
      <div class="bg-gradient-to-r from-orange-500 to-orange-600 text-white p-6 rounded-lg shadow">
        <div class="text-4xl font-bold">{{ stats.schedules }}</div>
        <div class="text-sm opacity-90">Total Schedules</div>
      </div>
    </div>
    
    <!-- Pending Count -->
    <div v-if="stats.pending > 0" class="bg-yellow-50 border-l-4 border-yellow-400 p-4 mb-8">
      <div class="flex items-center">
        <div class="flex-1">
          <p class="text-yellow-700 font-medium">
            {{ stats.pending }} registrasi menunggu approval
          </p>
        </div>
        <router-link 
          to="/admin/pending"
          class="bg-yellow-500 hover:bg-yellow-600 text-white px-4 py-2 rounded"
        >
          Lihat
        </router-link>
      </div>
    </div>
    
    <!-- Quick Actions -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      <router-link 
        to="/admin/pending"
        class="bg-white p-6 rounded-lg shadow hover:shadow-lg transition"
      >
        <h3 class="font-semibold text-lg mb-2">Pending Registrations</h3>
        <p class="text-gray-600 text-sm">Review dan approve pendaftar baru</p>
      </router-link>
      
      <router-link 
        to="/admin/players"
        class="bg-white p-6 rounded-lg shadow hover:shadow-lg transition"
      >
        <h3 class="font-semibold text-lg mb-2">Manage Players</h3>
        <p class="text-gray-600 text-sm">Kelola data pemain</p>
      </router-link>
      
      <router-link 
        to="/admin/coaches"
        class="bg-white p-6 rounded-lg shadow hover:shadow-lg transition"
      >
        <h3 class="font-semibold text-lg mb-2">Manage Coaches</h3>
        <p class="text-gray-600 text-sm">Kelola data pelatih</p>
      </router-link>
      
      <router-link 
        to="/admin/schedules"
        class="bg-white p-6 rounded-lg shadow hover:shadow-lg transition"
      >
        <h3 class="font-semibold text-lg mb-2">Manage Schedules</h3>
        <p class="text-gray-600 text-sm">Kelola jadwal latihan</p>
      </router-link>
    </div>
  </AdminLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import AdminLayout from '@/layouts/AdminLayout.vue'
import { playersService, coachesService, groupsService, schedulesService } from '@/services'

const stats = ref({
  players: 0,
  coaches: 0,
  groups: 0,
  schedules: 0,
  pending: 0
})

onMounted(async () => {
  try {
    const [playersData, coachesData, groupsData, schedulesData, pendingData] = await Promise.all([
      playersService.getPlayers(),
      coachesService.getCoaches(),
      groupsService.getGroups(),
      schedulesService.getSchedules(),
      playersService.getPending()
    ])
    
    stats.value = {
      players: playersData.results?.length || playersData.length || 0,
      coaches: coachesData.results?.length || coachesData.length || 0,
      groups: groupsData.results?.length || groupsData.length || 0,
      schedules: schedulesData.results?.length || schedulesData.length || 0,
      pending: pendingData.length || 0
    }
  } catch (error) {
    console.error('Failed to load stats:', error)
  }
})
</script>
