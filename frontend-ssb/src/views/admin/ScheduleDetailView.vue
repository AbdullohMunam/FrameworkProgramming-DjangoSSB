<template>
  <AdminLayout>
    <div class="schedule-detail">
      <!-- Header -->
      <div class="page-header">
        <div>
          <h1 class="page-title">{{ currentGroup?.name }} - Schedules</h1>
          <p class="page-subtitle">Training schedules for {{ currentGroup?.name }}</p>
        </div>
        <router-link to="/admin/schedules" class="btn-secondary">
          ← Back to All Schedules
        </router-link>
      </div>

      <!-- Stats Cards -->
      <div class="stats-grid">
        <div class="stat-card">
          <span class="stat-card__icon">📅</span>
          <div class="stat-card__content">
            <span class="stat-card__value">{{ schedules.length }}</span>
            <span class="stat-card__label">Total Schedules</span>
          </div>
        </div>
        <div class="stat-card">
          <span class="stat-card__icon">📈</span>
          <div class="stat-card__content">
            <span class="stat-card__value stat-card__value--blue">{{ upcomingSchedules }}</span>
            <span class="stat-card__label">Upcoming</span>
          </div>
        </div>
        <div class="stat-card">
          <span class="stat-card__icon">✅</span>
          <div class="stat-card__content">
            <span class="stat-card__value stat-card__value--gray">{{ completedSchedules }}</span>
            <span class="stat-card__label">Completed</span>
          </div>
        </div>
      </div>

      <!-- Schedules Table -->
      <div class="section-card">
        <h3 class="section-card__title">Training Schedules</h3>
        
        <div v-if="schedules.length === 0" class="empty-state">
          <span class="empty-state__icon">📅</span>
          <h4>No schedules</h4>
          <p>Get started by creating a new schedule for this group.</p>
        </div>
        
        <div v-else class="table-container">
          <table class="data-table">
            <thead>
              <tr>
                <th>Date</th>
                <th>Time</th>
                <th>Location</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="schedule in sortedSchedules" :key="schedule.id" :class="{ 'row-past': isPast(schedule.date) }">
                <td class="cell-date">{{ formatDate(schedule.date) }}</td>
                <td>{{ schedule.time }}</td>
                <td>{{ schedule.location || '-' }}</td>
                <td>
                  <span v-if="isPast(schedule.date)" class="status-badge status-badge--gray">
                    Completed
                  </span>
                  <span v-else class="status-badge status-badge--blue">
                    Upcoming
                  </span>
                </td>
                <td>
                  <div class="action-btns">
                    <button @click="editSchedule(schedule)" class="action-btn action-btn--edit">Edit</button>
                    <button @click="deleteSchedule(schedule.id)" class="action-btn action-btn--delete">Delete</button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Edit Modal -->
    <div v-if="showEditModal" class="modal-overlay" @click.self="showEditModal = false">
      <div class="modal">
        <h2 class="modal__title">Edit Schedule</h2>
        
        <div v-if="error" class="modal__error">{{ error }}</div>
        
        <form @submit.prevent="saveSchedule" class="modal__form">
          <div class="form-group">
            <label class="form-label">Date *</label>
            <input v-model="editForm.date" type="date" required class="form-input" />
          </div>
          
          <div class="form-group">
            <label class="form-label">Time *</label>
            <input v-model="editForm.time" type="time" required class="form-input" />
          </div>
          
          <div class="form-group">
            <label class="form-label">Location *</label>
            <input v-model="editForm.location" type="text" required class="form-input" placeholder="Training location" />
          </div>
          
          <div class="form-group">
            <label class="form-label">Group *</label>
            <select v-model="editForm.group" required class="form-input">
              <option value="">Select Group</option>
              <option v-for="group in groups" :key="group.id" :value="group.id">{{ group.name }}</option>
            </select>
          </div>
          
          <div class="modal__actions">
            <button type="submit" :disabled="saving" class="btn-primary">
              {{ saving ? 'Saving...' : 'Save' }}
            </button>
            <button type="button" @click="showEditModal = false" class="btn-secondary">
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

watch(() => route.params.id, () => {
  if (route.name === 'admin-schedule-detail') {
    loadData()
  }
})

onMounted(loadData)
</script>

<style scoped>
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.page-title {
  font-size: 1.5rem;
  font-weight: 800;
  color: #1e293b;
}

.page-subtitle {
  color: #64748b;
  font-size: 0.9rem;
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
  text-decoration: none;
  display: inline-flex;
  align-items: center;
}

.btn-secondary:hover {
  background: #cbd5e1;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.stat-card {
  background: white;
  border-radius: 1rem;
  padding: 1.25rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.stat-card__icon {
  font-size: 2rem;
}

.stat-card__value {
  display: block;
  font-size: 1.75rem;
  font-weight: 800;
  color: #1e293b;
  line-height: 1;
}

.stat-card__value--blue {
  color: #2563eb;
}

.stat-card__value--gray {
  color: #64748b;
}

.stat-card__label {
  font-size: 0.8rem;
  color: #64748b;
}

.section-card {
  background: white;
  border-radius: 1rem;
  padding: 1.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.section-card__title {
  font-size: 1.125rem;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 1rem;
}

.empty-state {
  text-align: center;
  padding: 3rem;
  color: #64748b;
}

.empty-state__icon {
  font-size: 3rem;
  display: block;
  margin-bottom: 1rem;
}

.empty-state h4 {
  font-size: 1rem;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 0.25rem;
}

.table-container {
  overflow-x: auto;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
}

.data-table th {
  background: #f8fafc;
  padding: 0.75rem 1rem;
  text-align: left;
  font-size: 0.75rem;
  font-weight: 600;
  color: #64748b;
  text-transform: uppercase;
}

.data-table td {
  padding: 0.75rem 1rem;
  border-bottom: 1px solid #f1f5f9;
  vertical-align: middle;
}

.row-past {
  background: #f8fafc;
  opacity: 0.8;
}

.cell-date {
  font-weight: 600;
  color: #1e293b;
}

.status-badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 600;
}

.status-badge--blue { background: #dbeafe; color: #1e40af; }
.status-badge--gray { background: #e2e8f0; color: #64748b; }

.action-btns {
  display: flex;
  gap: 0.5rem;
}

.action-btn {
  padding: 0.375rem 0.75rem;
  border-radius: 0.375rem;
  font-size: 0.8rem;
  font-weight: 500;
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
}

.form-input:focus {
  outline: none;
  border-color: #2563eb;
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
