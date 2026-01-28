<template>
  <AdminLayout>
    <div v-if="loading" class="text-center py-8">Loading...</div>
    
    <div v-else-if="group">
      <!-- Group Header -->
      <div class="mb-6 flex justify-between items-center">
        <div>
          <h1 class="text-3xl font-bold">{{ group.name }}</h1>
          <p class="text-gray-600 mt-1">Pelatih: {{ group.coach_name || 'Belum ada pelatih' }}</p>
        </div>
        <div class="flex gap-2">
          <button
            @click="openEditModal"
            class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
          >
            Edit Group
          </button>
          <router-link 
            to="/admin/groups"
            class="bg-gray-500 text-white px-4 py-2 rounded hover:bg-gray-600"
          >
            ← Back
          </router-link>
        </div>
      </div>

      <!-- Stats Cards -->
      <div class="grid md:grid-cols-2 gap-6 mb-6">
        <div class="bg-white p-6 rounded-lg shadow">
          <h3 class="text-gray-500 text-sm font-medium mb-2">Total Players</h3>
          <p class="text-3xl font-bold text-blue-600">{{ players.length }}</p>
        </div>
        <div class="bg-white p-6 rounded-lg shadow">
          <h3 class="text-gray-500 text-sm font-medium mb-2">Average Age</h3>
          <p class="text-3xl font-bold text-purple-600">{{ averageAge }}</p>
        </div>
      </div>

      <!-- Position Distribution -->
      <div class="bg-white p-6 rounded-lg shadow mb-6">
        <h3 class="text-xl font-bold mb-4">Position Distribution</h3>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div class="text-center p-4 bg-green-50 rounded-lg">
            <p class="text-2xl font-bold text-green-600">{{ positionCounts.Goalkeeper || 0 }}</p>
            <p class="text-sm text-gray-600">Goalkeeper</p>
          </div>
          <div class="text-center p-4 bg-blue-50 rounded-lg">
            <p class="text-2xl font-bold text-blue-600">{{ positionCounts.Defender || 0 }}</p>
            <p class="text-sm text-gray-600">Defender</p>
          </div>
          <div class="text-center p-4 bg-yellow-50 rounded-lg">
            <p class="text-2xl font-bold text-yellow-600">{{ positionCounts.Midfielder || 0 }}</p>
            <p class="text-sm text-gray-600">Midfielder</p>
          </div>
          <div class="text-center p-4 bg-red-50 rounded-lg">
            <p class="text-2xl font-bold text-red-600">{{ positionCounts.Forward || 0 }}</p>
            <p class="text-sm text-gray-600">Forward</p>
          </div>
        </div>
      </div>

      <!-- Players List -->
      <div class="bg-white rounded-lg shadow mb-6">
        <div class="p-6 border-b">
          <h3 class="text-xl font-bold">Players in {{ group.name }}</h3>
        </div>
        
        <div v-if="players.length === 0" class="p-6 text-center text-gray-500">
          No players in this group yet
        </div>
        
        <div v-else class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Photo</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Name</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Age</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Position</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="player in players" :key="player.id">
                <td class="px-6 py-4">
                  <img v-if="player.photo" :src="player.photo" class="w-10 h-10 rounded-full object-cover" />
                  <div v-else class="w-10 h-10 rounded-full bg-gray-200 flex items-center justify-center">
                    <svg class="w-6 h-6 text-gray-400" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clip-rule="evenodd" />
                    </svg>
                  </div>
                </td>
                <td class="px-6 py-4">{{ player.name || player.username }}</td>
                <td class="px-6 py-4">{{ player.age || '-' }}</td>
                <td class="px-6 py-4">{{ player.position || '-' }}</td>
                <td class="px-6 py-4">
                  <span :class="{
                    'bg-yellow-100 text-yellow-800': player.status === 'pending',
                    'bg-green-100 text-green-800': player.status === 'approved',
                    'bg-red-100 text-red-800': player.status === 'rejected'
                  }" class="px-2 py-1 rounded-full text-xs font-semibold">
                    {{ player.status }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

    </div>

    <div v-else class="text-center py-8">
      <p class="text-gray-600">Group not found</p>
    </div>

    <!-- Edit Modal -->
    <div v-if="showEditModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-8 max-w-md w-full">
        <h2 class="text-2xl font-bold mb-4">Edit Group</h2>
        
        <div v-if="error" class="bg-red-100 text-red-700 p-3 rounded mb-4">{{ error }}</div>
        
        <form @submit.prevent="saveGroup" class="space-y-4">
          <div>
            <label class="block text-sm font-medium mb-1">Group Name *</label>
            <input v-model="editForm.name" type="text" required class="w-full px-3 py-2 border rounded" 
                   placeholder="e.g., U-10, U-12, U-15" />
          </div>
          
          <div>
            <label class="block text-sm font-medium mb-1">Coach (Optional)</label>
            <select v-model="editForm.coach" class="w-full px-3 py-2 border rounded">
              <option :value="null">No coach assigned</option>
              <option v-for="coach in coaches" :key="coach.id" :value="coach.id">
                {{ coach.name }}
              </option>
            </select>
          </div>
          
          <div class="flex gap-2">
            <button type="submit" :disabled="saving" 
                    class="flex-1 bg-blue-600 text-white py-2 rounded hover:bg-blue-700 disabled:opacity-50">
              {{ saving ? 'Saving...' : 'Save' }}
            </button>
            <button type="button" @click="showEditModal = false" 
                    class="flex-1 bg-gray-300 text-gray-700 py-2 rounded hover:bg-gray-400">
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  </AdminLayout>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { useRoute } from 'vue-router'
import AdminLayout from '@/layouts/AdminLayout.vue'
import { groupsService, playersService, coachesService } from '@/services'

const route = useRoute()
const loading = ref(true)
const group = ref(null)
const players = ref([])
const coaches = ref([])
const showEditModal = ref(false)
const editForm = ref({ name: '', coach: null })
const error = ref('')
const saving = ref(false)

const groupId = computed(() => parseInt(route.params.id))

// Watch for route changes to reload data when switching between groups
watch(() => route.params.id, () => {
  if (route.name === 'admin-group-detail') {
    loadData()
  }
})

const positionCounts = computed(() => {
  const counts = {}
  players.value.forEach(player => {
    if (player.position) {
      counts[player.position] = (counts[player.position] || 0) + 1
    }
  })
  return counts
})

const averageAge = computed(() => {
  const ages = players.value.filter(p => p.age).map(p => p.age)
  if (ages.length === 0) return '-'
  return (ages.reduce((a, b) => a + b, 0) / ages.length).toFixed(1)
})

async function loadData() {
  try {
    // Load group details
    const groupsResponse = await groupsService.getGroups()
    const allGroups = groupsResponse.results || groupsResponse || []
    group.value = allGroups.find(g => g.id === groupId.value)
    
    if (!group.value) {
      loading.value = false
      return
    }
    
    // Load players in this group
    const playersResponse = await playersService.getPlayers()
    const allPlayers = playersResponse.results || playersResponse || []
    players.value = allPlayers.filter(p => p.group === groupId.value)
    
    // Load coaches for edit modal
    const coachesResponse = await coachesService.getCoaches()
    coaches.value = coachesResponse.results || coachesResponse || []
    
  } catch (error) {
    console.error('Failed to load data:', error)
  } finally {
    loading.value = false
  }
}

function openEditModal() {
  editForm.value = {
    name: group.value.name,
    coach: group.value.coach
  }
  error.value = ''
  showEditModal.value = true
}

async function saveGroup() {
  error.value = ''
  saving.value = true
  
  try {
    await groupsService.updateGroup(group.value.id, editForm.value)
    showEditModal.value = false
    await loadData()
  } catch (err) {
    error.value = err.response?.data?.detail || 'Failed to save group'
  } finally {
    saving.value = false
  }
}

onMounted(loadData)
</script>
