<template>
  <AdminLayout>
    <div class="groups-page">
      <div class="page-header">
        <h1 class="page-title">Groups Management</h1>
        <button @click="showModal = true; editingGroup = null; resetForm()" class="btn-primary">
          + Add Group
        </button>
      </div>

      <div v-if="loading" class="loading">
        <div class="loading__spinner"></div>
        <p>Loading...</p>
      </div>

      <div v-else>
        <p class="data-count">Showing {{ groups.length }} group(s)</p>
        
        <div class="groups-grid">
          <router-link 
            v-for="group in groups" 
            :key="group.id" 
            :to="`/admin/groups/${group.id}`"
            class="group-card"
          >
            <div class="group-card__icon">📂</div>
            <h3 class="group-card__name">{{ group.name }}</h3>
            <p class="group-card__coach">
              <span class="group-card__coach-label">Coach:</span>
              {{ group.coach_name || 'No coach assigned' }}
            </p>
            <div class="group-card__actions" @click.prevent>
              <button @click="editGroup(group)" class="action-btn action-btn--edit">Edit</button>
              <button @click="deleteGroup(group.id)" class="action-btn action-btn--delete">Delete</button>
            </div>
          </router-link>
        </div>
      </div>

      <!-- Modal -->
      <div v-if="showModal" class="modal-overlay" @click.self="showModal = false">
        <div class="modal">
          <h2 class="modal__title">{{ editingGroup ? 'Edit' : 'Add' }} Group</h2>
          
          <div v-if="error" class="modal__error">{{ error }}</div>
          
          <form @submit.prevent="saveGroup" class="modal__form">
            <div class="form-group">
              <label class="form-label">Group Name *</label>
              <input v-model="form.name" type="text" required class="form-input" placeholder="e.g., U-10, U-12, U-15" />
            </div>
            
            <div class="form-group">
              <label class="form-label">Coach</label>
              <select v-model="form.coach" class="form-input">
                <option :value="null">No coach</option>
                <option v-for="coach in coaches" :key="coach.id" :value="coach.id">{{ coach.name }}</option>
              </select>
            </div>
            
            <div class="modal__actions">
              <button type="submit" :disabled="saving" class="btn-primary">
                {{ saving ? 'Saving...' : 'Save' }}
              </button>
              <button type="button" @click="showModal = false" class="btn-secondary">
                Cancel
              </button>
            </div>
          </form>
        </div>
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

<style scoped>
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.page-title {
  font-size: 1.5rem;
  font-weight: 800;
  color: #1e293b;
}

.btn-primary {
  background: linear-gradient(135deg, #1e40af, #2563eb);
  color: white;
  padding: 0.625rem 1.25rem;
  border-radius: 0.5rem;
  font-weight: 600;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(30, 64, 175, 0.4);
}

.btn-primary:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.btn-secondary {
  background: #e2e8f0;
  color: #475569;
  padding: 0.625rem 1.25rem;
  border-radius: 0.5rem;
  font-weight: 600;
  border: none;
  cursor: pointer;
}

.btn-secondary:hover {
  background: #cbd5e1;
}

.loading {
  text-align: center;
  padding: 3rem;
  color: #64748b;
}

.loading__spinner {
  width: 40px;
  height: 40px;
  border: 3px solid #e2e8f0;
  border-top-color: #2563eb;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.data-count {
  color: #64748b;
  font-size: 0.875rem;
  margin-bottom: 1rem;
}

.groups-grid {
  display: grid;
  gap: 1rem;
  grid-template-columns: repeat(1, 1fr);
}

@media (min-width: 640px) {
  .groups-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1024px) {
  .groups-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

.group-card {
  background: white;
  border-radius: 1rem;
  padding: 1.5rem;
  text-decoration: none;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  transition: all 0.3s;
  border: 2px solid transparent;
}

.group-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.12);
  border-color: #2563eb;
}

.group-card__icon {
  font-size: 2.5rem;
  margin-bottom: 0.75rem;
}

.group-card__name {
  font-size: 1.25rem;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 0.5rem;
}

.group-card__coach {
  font-size: 0.875rem;
  color: #64748b;
  margin-bottom: 1rem;
}

.group-card__coach-label {
  font-weight: 600;
}

.group-card__actions {
  display: flex;
  gap: 0.5rem;
}

.action-btn {
  flex: 1;
  padding: 0.5rem 0.75rem;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  font-weight: 600;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
}

.action-btn--edit {
  background: #dbeafe;
  color: #1e40af;
}

.action-btn--edit:hover {
  background: #bfdbfe;
}

.action-btn--delete {
  background: #fee2e2;
  color: #dc2626;
}

.action-btn--delete:hover {
  background: #fecaca;
}

/* Modal */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
}

.modal {
  background: white;
  border-radius: 1rem;
  padding: 1.5rem;
  max-width: 450px;
  width: 100%;
}

.modal__title {
  font-size: 1.25rem;
  font-weight: 800;
  color: #1e293b;
  margin-bottom: 1.25rem;
}

.modal__error {
  background: #fef2f2;
  border: 1px solid #fecaca;
  color: #dc2626;
  padding: 0.75rem;
  border-radius: 0.5rem;
  margin-bottom: 1rem;
  font-size: 0.875rem;
}

.form-group {
  margin-bottom: 1rem;
}

.form-label {
  display: block;
  font-weight: 600;
  color: #374151;
  margin-bottom: 0.375rem;
  font-size: 0.875rem;
}

.form-input {
  width: 100%;
  padding: 0.625rem 0.875rem;
  border: 2px solid #e5e7eb;
  border-radius: 0.5rem;
  font-size: 0.9rem;
  transition: all 0.2s;
}

.form-input:focus {
  outline: none;
  border-color: #2563eb;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
}

.modal__actions {
  display: flex;
  gap: 0.75rem;
  margin-top: 1.5rem;
}

.modal__actions .btn-primary,
.modal__actions .btn-secondary {
  flex: 1;
}
</style>
