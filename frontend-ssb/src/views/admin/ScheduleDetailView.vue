<template>
  <AdminLayout>
    <div class="space-y-6">
      <!-- Header -->
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-3xl font-bold text-gray-900">{{ currentGroup?.name }} - Schedules</h1>
          <p class="mt-1 text-sm text-gray-600">Training schedules for {{ currentGroup?.name }}</p>
        </div>
        <router-link 
          to="/admin/schedules" 
          class="px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50"
        >
          Back to All Schedules
        </router-link>
      </div>

      <!-- Stats Cards -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div class="bg-white overflow-hidden shadow rounded-lg">
          <div class="p-5">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <svg class="h-6 w-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-gray-500 truncate">Total Schedules</dt>
                  <dd class="text-3xl font-semibold text-gray-900">{{ schedules.length }}</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div class="bg-white overflow-hidden shadow rounded-lg">
          <div class="p-5">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <svg class="h-6 w-6 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
                </svg>
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-gray-500 truncate">Upcoming</dt>
                  <dd class="text-3xl font-semibold text-blue-600">{{ upcomingSchedules }}</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div class="bg-white overflow-hidden shadow rounded-lg">
          <div class="p-5">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <svg class="h-6 w-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-gray-500 truncate">Completed</dt>
                  <dd class="text-3xl font-semibold text-gray-600">{{ completedSchedules }}</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Schedules Table -->
      <div class="bg-white shadow rounded-lg overflow-hidden">
        <div class="px-6 py-4 border-b border-gray-200">
          <h2 class="text-lg font-medium text-gray-900">Training Schedules</h2>
        </div>
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Time</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Location</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="schedule in sortedSchedules" :key="schedule.id" :class="{ 'bg-gray-50': isPast(schedule.date) }">
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {{ formatDate(schedule.date) }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {{ schedule.time }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {{ schedule.location }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span v-if="isPast(schedule.date)" class="px-2 py-1 text-xs font-semibold rounded-full bg-gray-200 text-gray-800">
                    Completed
                  </span>
                  <span v-else class="px-2 py-1 text-xs font-semibold rounded-full bg-blue-100 text-blue-800">
                    Upcoming
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                  <button
                    @click="editSchedule(schedule)"
                    class="text-blue-600 hover:text-blue-900 mr-3"
                  >
                    Edit
                  </button>
                  <button 
                    @click="deleteSchedule(schedule.id)" 
                    class="text-red-600 hover:text-red-900"
                  >
                    Delete
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
          
          <div v-if="schedules.length === 0" class="px-6 py-12 text-center">
            <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
            <h3 class="mt-2 text-sm font-medium text-gray-900">No schedules</h3>
            <p class="mt-1 text-sm text-gray-500">Get started by creating a new schedule for this group.</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Edit Modal -->
    <div v-if="showEditModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-8 max-w-md w-full">
        <h2 class="text-2xl font-bold mb-4">Edit Schedule</h2>
        
        <div v-if="error" class="bg-red-100 text-red-700 p-3 rounded mb-4">{{ error }}</div>
        
        <form @submit.prevent="saveSchedule" class="space-y-4">
          <div>
            <label class="block text-sm font-medium mb-1">Date *</label>
            <input v-model="editForm.date" type="date" required class="w-full px-3 py-2 border rounded" />
          </div>
          
          <div>
            <label class="block text-sm font-medium mb-1">Time *</label>
            <input v-model="editForm.time" type="time" required class="w-full px-3 py-2 border rounded" />
          </div>
          
          <div>
            <label class="block text-sm font-medium mb-1">Location *</label>
            <input v-model="editForm.location" type="text" required class="w-full px-3 py-2 border rounded" 
                   placeholder="Training location" />
          </div>
          
          <div>
            <label class="block text-sm font-medium mb-1">Group *</label>
            <select v-model="editForm.group" required class="w-full px-3 py-2 border rounded">
              <option value="">Select Group</option>
              <option v-for="group in groups" :key="group.id" :value="group.id">{{ group.name }}</option>
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
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { groupsService, schedulesService } from '@/services'
import AdminLayout from '@/layouts/AdminLayout.vue'

const route = useRoute()
const groups = ref([])
const schedules = ref([])
const showEditModal = ref(false)
const editForm = ref({ date: '', time: '', location: '', group: '' })
const editingSchedule = ref(null)
const error = ref('')
const saving = ref(false)

const groupId = computed(() => parseInt(route.params.id))
const currentGroup = computed(() => groups.value.find(g => g.id === groupId.value))

const upcomingSchedules = computed(() => {
  return schedules.value.filter(s => !isPast(s.date)).length
})

const completedSchedules = computed(() => {
  return schedules.value.filter(s => isPast(s.date)).length
})

const sortedSchedules = computed(() => {
  return [...schedules.value].sort((a, b) => {
    return new Date(b.date) - new Date(a.date)
  })
})

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', { 
    weekday: 'short', 
    year: 'numeric', 
    month: 'short', 
    day: 'numeric' 
  })
}

const isPast = (dateString) => {
  return new Date(dateString) < new Date()
}

const loadData = async () => {
  try {
    const [groupsData, schedulesData] = await Promise.all([
      groupsService.getGroups(),
      schedulesService.getSchedules()
    ])
    
    groups.value = groupsData.results || groupsData
    const allSchedules = schedulesData.results || schedulesData
    
    // Filter schedules by group
    schedules.value = allSchedules.filter(s => s.group === groupId.value)
  } catch (error) {
    console.error('Failed to load data:', error)
  }
}

const deleteSchedule = async (id) => {
  if (!confirm('Are you sure you want to delete this schedule?')) {
    return
  }
  
  try {
    await schedulesService.deleteSchedule(id)
    await loadData()
  } catch (error) {
    console.error('Failed to delete schedule:', error)
    alert('Failed to delete schedule')
  }
}

const editSchedule = (schedule) => {
  editingSchedule.value = schedule
  editForm.value = {
    date: schedule.date,
    time: schedule.time,
    location: schedule.location,
    group: schedule.group
  }
  error.value = ''
  showEditModal.value = true
}

const saveSchedule = async () => {
  error.value = ''
  saving.value = true
  
  try {
    await schedulesService.updateSchedule(editingSchedule.value.id, editForm.value)
    showEditModal.value = false
    await loadData()
  } catch (err) {
    error.value = err.response?.data?.detail || 'Failed to save schedule'
  } finally {
    saving.value = false
  }
}

// Watch for route param changes
watch(() => route.params.id, () => {
  if (route.name === 'admin-schedule-detail') {
    loadData()
  }
})

onMounted(loadData)
</script>
