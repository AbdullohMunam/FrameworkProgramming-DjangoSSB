<template>
  <AdminLayout>
    <div class="mb-6 flex justify-between items-center">
      <h1 class="text-3xl font-bold">Coaches Management</h1>
      <button @click="showModal = true; editingCoach = null; resetForm()" 
              class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
        + Add Coach
      </button>
    </div>

    <div v-if="loading" class="text-center py-8">Loading...</div>

    <div v-else>
      <div class="mb-4 text-sm text-gray-600">
        Showing {{ coaches.length }} coach(es)
      </div>
      
      <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-for="coach in coaches" :key="coach.id" class="bg-white rounded-lg shadow p-6">
        <div class="text-center mb-4">
          <img v-if="coach.photo" :src="coach.photo" class="w-24 h-24 rounded-full mx-auto object-cover mb-2" />
          <div v-else class="w-24 h-24 rounded-full mx-auto bg-gray-200 flex items-center justify-center mb-2">
            <span class="text-3xl">👤</span>
          </div>
          <h3 class="text-xl font-bold">{{ coach.name }}</h3>
        </div>
        
        <div class="space-y-2 text-sm text-gray-600">
          <p><strong>License:</strong> {{ coach.license_level || '-' }}</p>
          <p><strong>Phone:</strong> {{ coach.phone || '-' }}</p>
        </div>
        
        <div class="mt-4 flex gap-2">
          <button @click="editCoach(coach)" class="flex-1 bg-blue-600 text-white py-2 rounded hover:bg-blue-700">
            Edit
          </button>
          <button @click="deleteCoach(coach.id)" class="flex-1 bg-red-600 text-white py-2 rounded hover:bg-red-700">
            Delete
          </button>
        </div>
      </div>
      </div>
    </div>

    <!-- Modal -->
    <div v-if="showModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-8 max-w-md w-full">
        <h2 class="text-2xl font-bold mb-4">{{ editingCoach ? 'Edit' : 'Add' }} Coach</h2>
        
        <div v-if="error" class="bg-red-100 text-red-700 p-3 rounded mb-4">{{ error }}</div>
        
        <form @submit.prevent="saveCoach" class="space-y-4">
          <div>
            <label class="block text-sm font-medium mb-1">Name *</label>
            <input v-model="form.name" type="text" required class="w-full px-3 py-2 border rounded" />
          </div>
          
          <div>
            <label class="block text-sm font-medium mb-1">License Level</label>
            <input v-model="form.license_level" type="text" class="w-full px-3 py-2 border rounded" 
                   placeholder="e.g., A, B, C, D" />
          </div>
          
          <div>
            <label class="block text-sm font-medium mb-1">Phone</label>
            <input v-model="form.phone" type="text" class="w-full px-3 py-2 border rounded" />
          </div>
          
          <div>
            <label class="block text-sm font-medium mb-1">Photo</label>
            <input @change="handleFileChange" type="file" accept="image/*" class="w-full px-3 py-2 border rounded" />
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
import { coachesService } from '@/services'

const coaches = ref([])
const loading = ref(true)
const showModal = ref(false)
const editingCoach = ref(null)
const saving = ref(false)
const error = ref('')

const form = ref({
  name: '',
  license_level: '',
  phone: '',
  photo: null
})

function resetForm() {
  form.value = { name: '', license_level: '', phone: '', photo: null }
  error.value = ''
}

function handleFileChange(event) {
  form.value.photo = event.target.files[0] || null
}

async function loadCoaches() {
  try {
    const data = await coachesService.getCoaches()
    coaches.value = data.results || data || []
  } catch (err) {
    console.error('Failed to load coaches:', err)
  } finally {
    loading.value = false
  }
}

function editCoach(coach) {
  editingCoach.value = coach
  form.value = {
    name: coach.name,
    license_level: coach.license_level || '',
    phone: coach.phone || '',
    photo: null
  }
  showModal.value = true
}

async function saveCoach() {
  error.value = ''
  saving.value = true
  
  try {
    if (editingCoach.value) {
      await coachesService.updateCoach(editingCoach.value.id, form.value)
    } else {
      await coachesService.createCoach(form.value)
    }
    
    showModal.value = false
    await loadCoaches()
  } catch (err) {
    error.value = err.response?.data?.detail || 'Failed to save coach'
  } finally {
    saving.value = false
  }
}

async function deleteCoach(id) {
  if (!confirm('Delete this coach?')) return
  
  try {
    await coachesService.deleteCoach(id)
    await loadCoaches()
  } catch (err) {
    alert('Failed to delete coach')
  }
}

onMounted(loadCoaches)
</script>
