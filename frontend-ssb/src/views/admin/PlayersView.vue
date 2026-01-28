<template>
  <AdminLayout>
    <div class="mb-6 flex justify-between items-center">
      <h1 class="text-3xl font-bold">Players Management</h1>
      <button @click="showModal = true; editingPlayer = null; resetForm()" 
              class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
        + Add Player
      </button>
    </div>

    <div v-if="loading" class="text-center py-8">Loading...</div>

    <div v-else>
      <div class="mb-4 text-sm text-gray-600">
        Showing {{ players.length }} player(s)
      </div>
      
      <div class="bg-white rounded-lg shadow overflow-hidden">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Photo</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Name</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Age</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Position</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Group</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
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
            <td class="px-6 py-4">{{ player.group_name || '-' }}</td>
            <td class="px-6 py-4">
              <span :class="{
                'bg-yellow-100 text-yellow-800': player.status === 'pending',
                'bg-green-100 text-green-800': player.status === 'approved',
                'bg-red-100 text-red-800': player.status === 'rejected'
              }" class="px-2 py-1 rounded-full text-xs font-semibold">
                {{ player.status }}
              </span>
            </td>
            <td class="px-6 py-4 space-x-2">
              <button @click="editPlayer(player)" class="text-blue-600 hover:underline">Edit</button>
              <button @click="deletePlayer(player.id)" class="text-red-600 hover:underline">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
      </div>
    </div>

    <!-- Modal -->
    <div v-if="showModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-8 max-w-md w-full">
        <h2 class="text-2xl font-bold mb-4">{{ editingPlayer ? 'Edit' : 'Add' }} Player</h2>
        
        <div v-if="error" class="bg-red-100 text-red-700 p-3 rounded mb-4">{{ error }}</div>
        
        <form @submit.prevent="savePlayer" class="space-y-4">
          <div>
            <label class="block text-sm font-medium mb-1">Name</label>
            <input v-model="form.name" type="text" required class="w-full px-3 py-2 border rounded" />
          </div>
          
          <div>
            <label class="block text-sm font-medium mb-1">Age</label>
            <input v-model.number="form.age" type="number" required min="5" max="50" class="w-full px-3 py-2 border rounded" />
          </div>
          
          <div>
            <label class="block text-sm font-medium mb-1">Position</label>
            <select v-model="form.position" required class="w-full px-3 py-2 border rounded">
              <option value="">Select Position</option>
              <option value="Goalkeeper">Goalkeeper</option>
              <option value="Defender">Defender</option>
              <option value="Midfielder">Midfielder</option>
              <option value="Forward">Forward</option>
            </select>
          </div>
          
          <div>
            <label class="block text-sm font-medium mb-1">Group</label>
            <select v-model="form.group" class="w-full px-3 py-2 border rounded">
              <option :value="null">No Group</option>
              <option v-for="group in groups" :key="group.id" :value="group.id">{{ group.name }}</option>
            </select>
          </div>
          
          <div class="flex gap-2">
            <button type="submit" :disabled="saving" 
                    class="flex-1 bg-blue-600 text-white py-2 rounded hover:bg-blue-700">
              {{ saving ? 'Saving...' : 'Save' }}
            </button>
            <button type="button" @click="showModal = false" 
                    class="flex-1 bg-gray-300 py-2 rounded hover:bg-gray-400">
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  </AdminLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import AdminLayout from '@/layouts/AdminLayout.vue'
import { playersService, groupsService } from '@/services'

const players = ref([])
const groups = ref([])
const loading = ref(true)
const showModal = ref(false)
const editingPlayer = ref(null)
const saving = ref(false)
const error = ref('')

const form = ref({
  name: '',
  age: '',
  position: '',
  group: null
})

function resetForm() {
  form.value = { name: '', age: '', position: '', group: null }
  error.value = ''
}

async function loadData() {
  try {
    const [playersData, groupsData] = await Promise.all([
      playersService.getPlayers(),
      groupsService.getGroups()
    ])
    players.value = playersData.results || playersData || []
    groups.value = groupsData.results || groupsData || []
  } catch (err) {
    console.error('Failed to load data:', err)
  } finally {
    loading.value = false
  }
}

function editPlayer(player) {
  editingPlayer.value = player
  form.value = {
    name: player.name || '',
    age: player.age || '',
    position: player.position || '',
    group: player.group || null
  }
  showModal.value = true
}

async function savePlayer() {
  error.value = ''
  saving.value = true
  
  try {
    if (editingPlayer.value) {
      await playersService.updatePlayer(editingPlayer.value.id, form.value)
    } else {
      // For admin adding player, we need user field - skip for now or implement properly
      error.value = 'Use registration form to add new players'
      return
    }
    
    showModal.value = false
    await loadData()
  } catch (err) {
    error.value = err.response?.data?.detail || 'Failed to save player'
  } finally {
    saving.value = false
  }
}

async function deletePlayer(id) {
  if (!confirm('Delete this player?')) return
  
  try {
    await playersService.deletePlayer(id)
    await loadData()
  } catch (err) {
    alert('Failed to delete player')
  }
}

onMounted(loadData)
</script>
