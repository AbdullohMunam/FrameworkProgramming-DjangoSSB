<template>
  <AdminLayout>
    <div class="players-page">
      <div class="page-header">
        <h1 class="page-title">Players Management</h1>
        <button @click="showModal = true; editingPlayer = null; resetForm()" class="btn-primary">
          + Add Player
        </button>
      </div>

      <div v-if="loading" class="loading">
        <div class="loading__spinner"></div>
        <p>Loading...</p>
      </div>

      <div v-else>
        <p class="data-count">Showing {{ players.length }} player(s)</p>
        
        <div class="table-container">
          <table class="data-table">
            <thead>
              <tr>
                <th>Photo</th>
                <th>Name</th>
                <th>Age</th>
                <th>Position</th>
                <th>Group</th>
                <th>Status</th>
                <th>Actions</th>
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
                <td>{{ player.group_name || '-' }}</td>
                <td>
                  <span class="status-badge" :class="`status-badge--${player.status}`">
                    {{ player.status }}
                  </span>
                </td>
                <td>
                  <div class="action-btns">
                    <button @click="editPlayer(player)" class="action-btn action-btn--edit">Edit</button>
                    <button @click="deletePlayer(player.id)" class="action-btn action-btn--delete">Delete</button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Modal -->
      <div v-if="showModal" class="modal-overlay" @click.self="showModal = false">
        <div class="modal">
          <h2 class="modal__title">{{ editingPlayer ? 'Edit' : 'Add' }} Player</h2>
          
          <div v-if="error" class="modal__error">{{ error }}</div>
          
          <form @submit.prevent="savePlayer" class="modal__form">
            <div class="form-group">
              <label class="form-label">Name</label>
              <input v-model="form.name" type="text" required class="form-input" />
            </div>
            
            <div class="form-group">
              <label class="form-label">Age</label>
              <input v-model.number="form.age" type="number" required min="5" max="50" class="form-input" />
            </div>
            
            <div class="form-group">
              <label class="form-label">Position</label>
              <select v-model="form.position" required class="form-input">
                <option value="">Select Position</option>
                <option value="Goalkeeper">Goalkeeper</option>
                <option value="Defender">Defender</option>
                <option value="Midfielder">Midfielder</option>
                <option value="Forward">Forward</option>
              </select>
            </div>
            
            <div class="form-group">
              <label class="form-label">Group</label>
              <select v-model="form.group" class="form-input">
                <option :value="null">No Group</option>
                <option v-for="group in groups" :key="group.id" :value="group.id">{{ group.name }}</option>
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

.table-container {
  background: white;
  border-radius: 1rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
}

.data-table th {
  background: #f8fafc;
  padding: 0.875rem 1rem;
  text-align: left;
  font-size: 0.75rem;
  font-weight: 600;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  border-bottom: 1px solid #e2e8f0;
}

.data-table td {
  padding: 0.875rem 1rem;
  border-bottom: 1px solid #f1f5f9;
  vertical-align: middle;
}

.data-table tr:hover {
  background: #f8fafc;
}

.avatar {
  width: 40px;
  height: 40px;
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
  font-size: 1rem;
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
