<template>
  <AdminLayout>
    <div class="mb-6 flex justify-between items-center">
      <h1 class="text-3xl font-bold">Training Schedules Management</h1>
      <button @click="showModal = true; editingSchedule = null; resetForm()" 
              class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
        + Add Schedule
      </button>
    </div>

    <div v-if="loading" class="text-center py-8">Loading...</div>

    <div v-else>
      <div class="mb-4 text-sm text-gray-600">
        Showing {{ schedules.length }} schedule(s)
      </div>
      
      <div class="bg-white rounded-lg shadow overflow-hidden">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Date</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Time</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Group</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="schedule in schedules" :key="schedule.id">
            <td class="px-6 py-4">{{ formatDate(schedule.date) }}</td>
            <td class="px-6 py-4">{{ schedule.time }}</td>
            <td class="px-6 py-4">{{ schedule.group_name || '-' }}</td>
            <td class="px-6 py-4 space-x-2">
              <button @click="editSchedule(schedule)" class="text-blue-600 hover:underline">Edit</button>
              <button @click="deleteSchedule(schedule.id)" class="text-red-600 hover:underline">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
      </div>
    </div>

    <!-- Modal -->
    <div v-if="showModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-8 max-w-md w-full">
        <h2 class="text-2xl font-bold mb-4">{{ editingSchedule ? 'Edit' : 'Add' }} Schedule</h2>
        
        <div v-if="error" class="bg-red-100 text-red-700 p-3 rounded mb-4">{{ error }}</div>
        
        <form @submit.prevent="saveSchedule" class="space-y-4">
          <div>
            <label class="block text-sm font-medium mb-1">Date *</label>
            <input v-model="form.date" type="date" required class="w-full px-3 py-2 border rounded" />
          </div>
          
          <div>
            <label class="block text-sm font-medium mb-1">Time *</label>
            <input v-model="form.time" type="time" required class="w-full px-3 py-2 border rounded" />
          </div>
          
          <div>
            <label class="block text-sm font-medium mb-1">Group *</label>
            <select v-model="form.group" required class="w-full px-3 py-2 border rounded">
              <option value="">Select Group</option>
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
import { schedulesService, groupsService } from '@/services'

const schedules = ref([])
const groups = ref([])
const loading = ref(true)
const showModal = ref(false)
const editingSchedule = ref(null)
const saving = ref(false)
const error = ref('')

const form = ref({
  date: '',
  time: '',
  group: ''
})

function resetForm() {
  form.value = { date: '', time: '', group: '' }
  error.value = ''
}

function formatDate(dateStr) {
  return new Date(dateStr).toLocaleDateString('id-ID', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

async function loadData() {
  try {
    const [schedulesData, groupsData] = await Promise.all([
      schedulesService.getSchedules(),
      groupsService.getGroups()
    ])
    schedules.value = schedulesData.results || schedulesData || []
    groups.value = groupsData.results || groupsData || []
  } catch (err) {
    console.error('Failed to load data:', err)
  } finally {
    loading.value = false
  }
}

function editSchedule(schedule) {
  editingSchedule.value = schedule
  form.value = {
    date: schedule.date,
    time: schedule.time,
    group: schedule.group
  }
  showModal.value = true
}

async function saveSchedule() {
  error.value = ''
  saving.value = true
  
  try {
    if (editingSchedule.value) {
      await schedulesService.updateSchedule(editingSchedule.value.id, form.value)
    } else {
      await schedulesService.createSchedule(form.value)
    }
    
    showModal.value = false
    await loadData()
  } catch (err) {
    error.value = err.response?.data?.detail || 'Failed to save schedule'
  } finally {
    saving.value = false
  }
}

async function deleteSchedule(id) {
  if (!confirm('Delete this schedule?')) return
  
  try {
    await schedulesService.deleteSchedule(id)
    await loadData()
  } catch (err) {
    alert('Failed to delete schedule')
  }
}

onMounted(loadData)
</script>
