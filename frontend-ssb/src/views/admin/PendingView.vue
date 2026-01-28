<template>
  <AdminLayout>
    <h1 class="text-3xl font-bold mb-8">Pending Registrations</h1>
    
    <div v-if="loading" class="text-center py-8">Loading...</div>
    
    <div v-else-if="pendingPlayers.length === 0" class="bg-white p-8 rounded-lg shadow text-center">
      <p class="text-gray-600">Tidak ada pendaftaran yang menunggu approval</p>
    </div>
    
    <div v-else class="grid grid-cols-1 gap-4">
      <div 
        v-for="player in pendingPlayers" 
        :key="player.id"
        class="bg-white p-6 rounded-lg shadow"
      >
        <div class="flex items-start gap-4">
          <img v-if="player.photo" :src="player.photo" class="w-20 h-20 rounded-full object-cover" />
          <div v-else class="w-20 h-20 rounded-full bg-gray-200 flex items-center justify-center">
            <svg class="w-12 h-12 text-gray-400" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clip-rule="evenodd" />
            </svg>
          </div>
          
          <div class="flex-1">
            <h3 class="text-xl font-bold mb-2">{{ player.name }}</h3>
            <div class="grid grid-cols-2 gap-4 text-sm text-gray-600">
              <div>
                <p><strong>Username:</strong> {{ player.username }}</p>
                <p><strong>Email:</strong> {{ player.email }}</p>
              </div>
              <div>
                <p><strong>Umur:</strong> {{ player.age }} tahun</p>
                <p><strong>Posisi:</strong> {{ player.position }}</p>
              </div>
            </div>
            <p class="text-xs text-gray-500 mt-2">
              Registered: {{ new Date(player.registered_at).toLocaleString('id-ID') }}
            </p>
          </div>
          
          <div class="flex flex-col gap-2 ml-4 min-w-[200px]">
            <select 
              v-model="selectedGroups[player.id]" 
              class="px-3 py-2 border rounded"
              :disabled="processing === player.id"
            >
              <option value="">Pilih Grup</option>
              <option v-for="group in groups" :key="group.id" :value="group.id">
                {{ group.name }}
              </option>
            </select>
            
            <button 
              @click="approve(player.id)"
              :disabled="processing === player.id || !selectedGroups[player.id]"
              class="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded disabled:opacity-50"
            >
              {{ processing === player.id ? 'Processing...' : 'Approve' }}
            </button>
            <button 
              @click="reject(player.id)"
              :disabled="processing === player.id"
              class="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded disabled:opacity-50"
            >
              Reject
            </button>
          </div>
        </div>
      </div>
    </div>
  </AdminLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import AdminLayout from '@/layouts/AdminLayout.vue'
import { playersService, groupsService } from '@/services'

const pendingPlayers = ref([])
const groups = ref([])
const selectedGroups = ref({})
const loading = ref(true)
const processing = ref(null)

async function loadData() {
  try {
    loading.value = true
    const [players, groupsData] = await Promise.all([
      playersService.getPending(),
      groupsService.getGroups()
    ])
    pendingPlayers.value = players
    groups.value = groupsData.results || groupsData
  } catch (error) {
    console.error('Failed to load data:', error)
  } finally {
    loading.value = false
  }
}

async function approve(id) {
  const groupId = selectedGroups.value[id]
  if (!groupId) {
    alert('Pilih grup terlebih dahulu!')
    return
  }
  
  if (!confirm('Approve registrasi ini dan tempatkan di grup yang dipilih?')) return
  
  processing.value = id
  try {
    await playersService.approve(id, groupId)
    alert('Player approved successfully!')
    await loadData()
  } catch (error) {
    alert('Failed to approve: ' + (error.response?.data?.detail || error.message))
  } finally {
    processing.value = null
  }
}

async function reject(id) {
  if (!confirm('Reject registrasi ini?')) return
  
  processing.value = id
  try {
    await playersService.reject(id)
    alert('Player rejected')
    await loadData()
  } catch (error) {
    alert('Failed to reject: ' + (error.response?.data?.detail || error.message))
  } finally {
    processing.value = null
  }
}

onMounted(loadData)
</script>
