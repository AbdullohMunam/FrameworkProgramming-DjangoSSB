<template>
  <div class="min-h-screen bg-gray-50">
    <nav class="bg-white shadow">
      <div class="container mx-auto px-4 py-4 flex justify-between items-center">
        <h1 class="text-2xl font-bold text-blue-600">SSB Academy</h1>
        <div class="flex items-center gap-4">
          <router-link to="/profile" class="hover:text-blue-600">Profile</router-link>
          <router-link to="/schedules" class="hover:text-blue-600">Schedules</router-link>
          <router-link to="/team" class="text-blue-600 font-semibold">My Team</router-link>
          <button @click="handleLogout" class="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700">
            Logout
          </button>
        </div>
      </div>
    </nav>
    
    <div class="container mx-auto px-4 py-8">
      <div class="mb-6">
        <h2 class="text-3xl font-bold">My Team</h2>
        <p v-if="groupName" class="text-gray-600 mt-2">Kelompok: <span class="font-semibold">{{ groupName }}</span></p>
      </div>
      
      <div v-if="loading" class="text-center py-8">
        <p>Loading team members...</p>
      </div>
      
      <div v-else-if="!groupName" class="bg-white p-8 rounded-lg shadow text-center">
        <svg class="w-16 h-16 mx-auto text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
        </svg>
        <p class="text-gray-600 text-lg">Anda belum ditugaskan ke kelompok manapun</p>
      </div>
      
      <div v-else>
        <!-- Coach Info -->
        <div v-if="coach" class="bg-white p-6 rounded-lg shadow mb-6">
          <h3 class="text-xl font-bold mb-4 text-gray-700">Pelatih</h3>
          <div class="flex items-center gap-4">
            <img v-if="coach.photo" :src="coach.photo" class="w-16 h-16 rounded-full object-cover" />
            <div v-else class="w-16 h-16 rounded-full bg-gray-200 flex items-center justify-center">
              <span class="text-2xl">👤</span>
            </div>
            <div>
              <p class="font-semibold text-lg">{{ coach.name }}</p>
              <p class="text-sm text-gray-600">Lisensi: {{ coach.license_level || '-' }}</p>
              <p class="text-sm text-gray-600">{{ coach.phone || '-' }}</p>
            </div>
          </div>
        </div>
        
        <!-- Team Members -->
        <div class="bg-white p-6 rounded-lg shadow">
          <h3 class="text-xl font-bold mb-4 text-gray-700">
            Anggota Tim ({{ teammates.length }} pemain)
          </h3>
          
          <div v-if="teammates.length === 0" class="text-center py-8 text-gray-500">
            Belum ada anggota tim lainnya
          </div>
          
          <div v-else class="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
            <div v-for="player in teammates" :key="player.id" 
                 class="border rounded-lg p-4 hover:shadow-md transition-shadow"
                 :class="{ 'bg-blue-50 border-blue-300': player.id === myId }">
              <div class="flex items-center gap-3 mb-3">
                <img v-if="player.photo" :src="player.photo" class="w-12 h-12 rounded-full object-cover" />
                <div v-else class="w-12 h-12 rounded-full bg-gray-200 flex items-center justify-center">
                  <svg class="w-6 h-6 text-gray-400" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clip-rule="evenodd" />
                  </svg>
                </div>
                <div class="flex-1">
                  <p class="font-semibold">
                    {{ player.name }}
                    <span v-if="player.id === myId" class="text-blue-600 text-sm">(Anda)</span>
                  </p>
                  <p class="text-sm text-gray-600">{{ player.position }}</p>
                </div>
              </div>
              <div class="text-sm text-gray-600">
                <p>Umur: {{ player.age }} tahun</p>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Position Summary -->
        <div class="bg-white p-6 rounded-lg shadow mt-6">
          <h3 class="text-xl font-bold mb-4 text-gray-700">Komposisi Tim</h3>
          <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div class="text-center p-4 bg-green-50 rounded-lg">
              <p class="text-3xl font-bold text-green-600">{{ positionCounts.Goalkeeper || 0 }}</p>
              <p class="text-sm text-gray-600">Goalkeeper</p>
            </div>
            <div class="text-center p-4 bg-blue-50 rounded-lg">
              <p class="text-3xl font-bold text-blue-600">{{ positionCounts.Defender || 0 }}</p>
              <p class="text-sm text-gray-600">Defender</p>
            </div>
            <div class="text-center p-4 bg-yellow-50 rounded-lg">
              <p class="text-3xl font-bold text-yellow-600">{{ positionCounts.Midfielder || 0 }}</p>
              <p class="text-sm text-gray-600">Midfielder</p>
            </div>
            <div class="text-center p-4 bg-red-50 rounded-lg">
              <p class="text-3xl font-bold text-red-600">{{ positionCounts.Forward || 0 }}</p>
              <p class="text-sm text-gray-600">Forward</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { playersService, coachesService, groupsService } from '@/services'

const router = useRouter()
const authStore = useAuthStore()
const loading = ref(true)
const groupName = ref(null)
const groupId = ref(null)
const coach = ref(null)
const teammates = ref([])
const myId = ref(null)

const positionCounts = computed(() => {
  const counts = {}
  teammates.value.forEach(player => {
    if (player.position) {
      counts[player.position] = (counts[player.position] || 0) + 1
    }
  })
  return counts
})

async function loadTeamData() {
  try {
    // Get user's profile to know their group
    const profile = await playersService.getMyProfile()
    myId.value = profile.id
    groupName.value = profile.group_name
    groupId.value = profile.group
    
    if (!groupId.value) {
      loading.value = false
      return
    }
    
    // Get all players and filter by group
    const playersResponse = await playersService.getPlayers()
    const allPlayers = playersResponse.results || playersResponse || []
    teammates.value = allPlayers
      .filter(p => p.group === groupId.value && p.status === 'approved')
      .sort((a, b) => {
        // Sort: current user first, then by position, then by name
        if (a.id === myId.value) return -1
        if (b.id === myId.value) return 1
        
        const positionOrder = { 'Goalkeeper': 1, 'Defender': 2, 'Midfielder': 3, 'Forward': 4 }
        const posA = positionOrder[a.position] || 5
        const posB = positionOrder[b.position] || 5
        
        if (posA !== posB) return posA - posB
        return (a.name || '').localeCompare(b.name || '')
      })
    
    // Get group details to find coach
    const groupsResponse = await groupsService.getGroups()
    const allGroups = groupsResponse.results || groupsResponse || []
    const myGroup = allGroups.find(g => g.id === groupId.value)
    
    // Get coach info if group has a coach
    if (myGroup && myGroup.coach) {
      const coachesResponse = await coachesService.getCoaches()
      const allCoaches = coachesResponse.results || coachesResponse || []
      coach.value = allCoaches.find(c => c.id === myGroup.coach)
    }
  } catch (error) {
    console.error('Failed to load team data:', error)
  } finally {
    loading.value = false
  }
}

async function handleLogout() {
  await authStore.logout()
  router.push('/login')
}

onMounted(loadTeamData)
</script>
