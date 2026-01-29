<template>
  <AdminLayout>
    <div class="coaches-page">
      <div class="page-header">
        <h1 class="page-title">Coaches Management</h1>
        <button @click="showModal = true; editingCoach = null; resetForm()" class="btn-primary">
          + Add Coach
        </button>
      </div>

      <div v-if="loading" class="loading">
        <div class="loading__spinner"></div>
        <p>Loading...</p>
      </div>

      <div v-else>
        <p class="data-count">Showing {{ coaches.length }} coach(es)</p>
        
        <div class="coaches-grid">
          <div v-for="coach in coaches" :key="coach.id" class="coach-card">
            <div class="coach-card__avatar">
              <img v-if="coach.photo" :src="coach.photo" class="coach-card__avatar-img" />
              <span v-else class="coach-card__avatar-placeholder">{{ coach.name?.charAt(0)?.toUpperCase() || '?' }}</span>
            </div>
            <h3 class="coach-card__name">{{ coach.name }}</h3>
            <div class="coach-card__info">
              <p><strong>License:</strong> {{ coach.license_level || '-' }}</p>
              <p><strong>Phone:</strong> {{ coach.phone || '-' }}</p>
            </div>
            <div class="coach-card__actions">
              <button @click="editCoach(coach)" class="action-btn action-btn--edit">Edit</button>
              <button @click="deleteCoach(coach.id)" class="action-btn action-btn--delete">Delete</button>
            </div>
          </div>
        </div>
      </div>

      <!-- Modal -->
      <div v-if="showModal" class="modal-overlay" @click.self="showModal = false">
        <div class="modal">
          <h2 class="modal__title">{{ editingCoach ? 'Edit' : 'Add' }} Coach</h2>
          
          <div v-if="error" class="modal__error">{{ error }}</div>
          
          <form @submit.prevent="saveCoach" class="modal__form">
            <div class="form-group">
              <label class="form-label">Name *</label>
              <input v-model="form.name" type="text" required class="form-input" />
            </div>
            
            <div class="form-group">
              <label class="form-label">License Level</label>
              <input v-model="form.license_level" type="text" class="form-input" placeholder="e.g., A, B, C, D" />
            </div>
            
            <div class="form-group">
              <label class="form-label">Phone</label>
              <input v-model="form.phone" type="text" class="form-input" />
            </div>
            
            <div class="form-group">
              <label class="form-label">Photo</label>
              <input @change="handleFileChange" type="file" accept="image/*" class="form-input form-input--file" />
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

.coaches-grid {
  display: grid;
  gap: 1rem;
  grid-template-columns: repeat(1, 1fr);
}

@media (min-width: 640px) {
  .coaches-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1024px) {
  .coaches-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

.coach-card {
  background: white;
  border-radius: 1rem;
  padding: 1.5rem;
  text-align: center;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  transition: all 0.3s;
}

.coach-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.12);
}

.coach-card__avatar {
  width: 80px;
  height: 80px;
  margin: 0 auto 1rem;
  border-radius: 50%;
  background: linear-gradient(135deg, #1e40af, #2563eb);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  overflow: hidden;
}

.coach-card__avatar-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.coach-card__avatar-placeholder {
  color: white;
  font-weight: 700;
  font-size: 2rem;
}

.coach-card__name {
  font-size: 1.125rem;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 0.75rem;
}

.coach-card__info {
  text-align: left;
  font-size: 0.875rem;
  color: #64748b;
  margin-bottom: 1rem;
  padding: 0.75rem;
  background: #f8fafc;
  border-radius: 0.5rem;
}

.coach-card__info p {
  margin-bottom: 0.25rem;
}

.coach-card__actions {
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
  max-height: 90vh;
  overflow-y: auto;
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

.form-input--file {
  padding: 0.5rem;
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
