<template>
  <AdminLayout>
    <div class="mb-6 flex justify-between items-center">
      <h1 class="text-3xl font-bold">Groups Management</h1>
      <button @click="showModal = true; editingGroup = null; resetForm()" 
              class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
        + Add Group
      </button>
    </div>

    <div v-if="loading" class="text-center py-8">Loading...</div>

    <div v-else>
      <div class="mb-4 text-sm text-gray-600">
        Showing {{ groups.length }} group(s)
      </div>
      
      <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-for="group in groups" :key="group.id" class="bg-white rounded-lg shadow p-6">
        <h3 class="text-xl font-bold mb-4">{{ group.name }}</h3>
        
        <div class="text-sm text-gray-600 mb-4">
          <p><strong>Coach:</strong> {{ group.coach_name || 'No coach assigned' }}</p>
        </div>
        
        <div class="flex gap-2">
          <button @click="editGroup(group)" class="flex-1 bg-blue-600 text-white py-2 rounded hover:bg-blue-700">
            Edit
          </button>
          <button @click="deleteGroup(group.id)" class="flex-1 bg-red-600 text-white py-2 rounded hover:bg-red-700">
            Delete
          </button>
        </div>
      </div>
      </div>
    </div>

    <!-- Modal -->
    <div v-if="showModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-8 max-w-md w-full">
        <h2 class="text-2xl font-bold mb-4">{{ editingGroup ? 'Edit' : 'Add' }} Group</h2>
        
        <div v-if="error" class="bg-red-100 text-red-700 p-3 rounded mb-4">{{ error }}</div>
        
        <form @submit.prevent="saveGroup" class="space-y-4">
          <div>
            <label class="block text-sm font-medium mb-1">Group Name *</label>
            <input v-model="form.name" type="text" required class="w-full px-3 py-2 border rounded" 
                   placeholder="e.g., U-10, U-12, U-15" />
          </div>
          
          <div>
            <label class="block text-sm font-medium mb-1">Coach</label>
            <select v-model="form.coach" class="w-full px-3 py-2 border rounded">
              <option :value="null">No coach</option>
              <option v-for="coach in coaches" :key="coach.id" :value="coach.id">{{ coach.name }}</option>
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
import { groupsService, coachesService } from '@/services'

const groups = ref([])
const coaches = ref([])
const loading = ref(true)
const showModal = ref(false)
const editingGroup = ref(null)
const saving = ref(false)
const error = ref('')

const form = ref({
  name: '',
  coach: null
})

function resetForm() {
  form.value = { name: '', coach: null }
  error.value = ''
}

async function loadData() {
  try {
    const [groupsData, coachesData] = await Promise.all([
      groupsService.getGroups(),
      coachesService.getCoaches()
    ])
    groups.value = groupsData.results || groupsData || []
    coaches.value = coachesData.results || coachesData || []
  } catch (err) {
    console.error('Failed to load data:', err)
  } finally {
    loading.value = false
  }
}

function editGroup(group) {
  editingGroup.value = group
  form.value = {
    name: group.name,
    coach: group.coach
  }
  showModal.value = true
}

async function saveGroup() {
  error.value = ''
  saving.value = true
  
  try {
    if (editingGroup.value) {
      await groupsService.updateGroup(editingGroup.value.id, form.value)
    } else {
      await groupsService.createGroup(form.value)
    }
    
    showModal.value = false
    await loadData()
  } catch (err) {
    error.value = err.response?.data?.detail || 'Failed to save group'
  } finally {
    saving.value = false
  }
}

async function deleteGroup(id) {
  if (!confirm('Delete this group?')) return
  
  try {
    await groupsService.deleteGroup(id)
    await loadData()
  } catch (err) {
    alert('Failed to delete group')
  }
}

onMounted(loadData)
</script>
