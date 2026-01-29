<template>
  <AdminLayout>
    <div v-if="loading" class="loading">
      <div class="loading__spinner"></div>
      <p>Loading...</p>
    </div>
    
    <div v-else-if="group" class="group-detail">
      <!-- Header -->
      <div class="page-header">
        <div>
          <h1 class="page-title">{{ group.name }}</h1>
          <p class="page-subtitle">Pelatih: {{ group.coach_name || 'Belum ada pelatih' }}</p>
        </div>
        <div class="page-header__actions">
          <button @click="openEditModal" class="btn-primary">Edit Group</button>
          <router-link to="/admin/groups" class="btn-secondary">← Back</router-link>
        </div>
      </div>

      <!-- Stats Cards -->
      <div class="stats-grid">
        <div class="stat-card">
          <span class="stat-card__icon">👥</span>
          <div class="stat-card__content">
            <span class="stat-card__value">{{ players.length }}</span>
            <span class="stat-card__label">Total Players</span>
          </div>
        </div>
        <div class="stat-card">
          <span class="stat-card__icon">📊</span>
          <div class="stat-card__content">
            <span class="stat-card__value">{{ averageAge }}</span>
            <span class="stat-card__label">Average Age</span>
          </div>
        </div>
      </div>

      <!-- Position Distribution -->
      <div class="section-card">
        <h3 class="section-card__title">Position Distribution</h3>
        <div class="position-grid">
          <div class="position-item position-item--gk">
            <span class="position-item__count">{{ positionCounts.Goalkeeper || 0 }}</span>
            <span class="position-item__label">🧤 GK</span>
          </div>
          <div class="position-item position-item--def">
            <span class="position-item__count">{{ positionCounts.Defender || 0 }}</span>
            <span class="position-item__label">🛡️ DEF</span>
          </div>
          <div class="position-item position-item--mid">
            <span class="position-item__count">{{ positionCounts.Midfielder || 0 }}</span>
            <span class="position-item__label">⚡ MID</span>
          </div>
          <div class="position-item position-item--fwd">
            <span class="position-item__count">{{ positionCounts.Forward || 0 }}</span>
            <span class="position-item__label">⚽ FWD</span>
          </div>
        </div>
      </div>

      <!-- Players List -->
      <div class="section-card">
        <h3 class="section-card__title">Players in {{ group.name }}</h3>
        
        <div v-if="players.length === 0" class="empty-state">
          <p>No players in this group yet</p>
        </div>
        
        <div v-else class="table-container">
          <table class="data-table">
            <thead>
              <tr>
                <th>Photo</th>
                <th>Name</th>
                <th>Age</th>
                <th>Position</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="player in players" :key="player.id">
                <td>
                  <div class="avatar">
                    <img v-if="player.photo" :src="player.photo" class="avatar__img" />
                    <span v-else class="avatar__placeholder">
                      {{ player.name?.charAt(0)?.toUpperCase() || '?' }}
                    </span>
                  </div>
                </td>
                <td class="cell-name">{{ player.name || player.username }}</td>
                <td>{{ player.age || '-' }}</td>
                <td>{{ player.position || '-' }}</td>
                <td>
                  <span class="status-badge" :class="`status-badge--${player.status}`">
                    {{ player.status }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <div v-else class="empty-state">
      <p>Group not found</p>
    </div>

    <!-- Edit Modal -->
    <div v-if="showEditModal" class="modal-overlay" @click.self="showEditModal = false">
      <div class="modal">
        <h2 class="modal__title">Edit Group</h2>
        
        <div v-if="error" class="modal__error">{{ error }}</div>
        
        <form @submit.prevent="saveGroup" class="modal__form">
          <div class="form-group">
            <label class="form-label">Group Name *</label>
            <input v-model="editForm.name" type="text" required class="form-input" />
          </div>
          
          <div class="form-group">
            <label class="form-label">Coach (Optional)</label>
            <select v-model="editForm.coach" class="form-input">
              <option :value="null">No coach assigned</option>
              <option v-for="coach in coaches" :key="coach.id" :value="coach.id">
                {{ coach.name }}
              </option>
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
    const groupsResponse = await groupsService.getGroups()
    const allGroups = groupsResponse.results || groupsResponse || []
    group.value = allGroups.find(g => g.id === groupId.value)
    
    if (!group.value) {
      loading.value = false
      return
    }
    
    const playersResponse = await playersService.getPlayers()
    const allPlayers = playersResponse.results || playersResponse || []
    players.value = allPlayers.filter(p => p.group === groupId.value)
    
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

<style scoped>
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

.page-header__actions {
  display: flex;
  gap: 0.5rem;
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
  text-decoration: none;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(30, 64, 175, 0.4);
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
  grid-template-columns: repeat(2, 1fr);
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
  color: #1e40af;
  line-height: 1;
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
  margin-bottom: 1.5rem;
}

.section-card__title {
  font-size: 1.125rem;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 1rem;
}

.position-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
}

.position-item {
  text-align: center;
  padding: 1rem;
  border-radius: 0.75rem;
}

.position-item--gk { background: #d1fae5; }
.position-item--def { background: #dbeafe; }
.position-item--mid { background: #fef3c7; }
.position-item--fwd { background: #fee2e2; }

.position-item__count {
  display: block;
  font-size: 1.5rem;
  font-weight: 800;
}

.position-item--gk .position-item__count { color: #059669; }
.position-item--def .position-item__count { color: #2563eb; }
.position-item--mid .position-item__count { color: #d97706; }
.position-item--fwd .position-item__count { color: #dc2626; }

.position-item__label {
  font-size: 0.8rem;
  color: #64748b;
}

.empty-state {
  text-align: center;
  padding: 2rem;
  color: #64748b;
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

.avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  overflow: hidden;
  background: linear-gradient(135deg, #1e40af, #2563eb);
  display: flex;
  align-items: center;
  justify-content: center;
}

.avatar__img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar__placeholder {
  color: white;
  font-weight: 700;
  font-size: 0.875rem;
}

.cell-name {
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

.status-badge--pending { background: #fef3c7; color: #d97706; }
.status-badge--approved { background: #d1fae5; color: #059669; }
.status-badge--rejected { background: #fee2e2; color: #dc2626; }

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
