<template>
  <AdminLayout>
    <div class="pending-page">
      <h1 class="page-title">Pending Registrations</h1>
      
      <div v-if="loading" class="loading">
        <div class="loading__spinner"></div>
        <p>Loading...</p>
      </div>
      
      <div v-else-if="pendingPlayers.length === 0" class="empty-state">
        <span class="empty-state__icon">✅</span>
        <h3>Tidak ada pendaftaran pending</h3>
        <p>Semua pendaftaran sudah diproses</p>
      </div>
      
      <div v-else class="pending-list">
        <div v-for="player in pendingPlayers" :key="player.id" class="pending-card">
          <div class="pending-card__header">
            <div class="pending-card__avatar">
              <img v-if="player.photo" :src="player.photo" class="pending-card__avatar-img" />
              <span v-else>{{ player.name?.charAt(0)?.toUpperCase() || '?' }}</span>
            </div>
            <div class="pending-card__info">
              <h3 class="pending-card__name">{{ player.name }}</h3>
              <p class="pending-card__date">
                Registered: {{ new Date(player.registered_at).toLocaleDateString('id-ID') }}
              </p>
            </div>
          </div>
          
          <div class="pending-card__details">
            <div class="detail-item">
              <span class="detail-item__label">Username</span>
              <span class="detail-item__value">{{ player.username }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-item__label">Email</span>
              <span class="detail-item__value">{{ player.email }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-item__label">Umur</span>
              <span class="detail-item__value">{{ player.age }} tahun</span>
            </div>
            <div class="detail-item">
              <span class="detail-item__label">Posisi</span>
              <span class="detail-item__value">{{ player.position }}</span>
            </div>
          </div>
          
          <div class="pending-card__actions">
            <div class="pending-card__group-select">
              <label class="pending-card__label">Pilih grup:</label>
              <select 
                v-model="selectedGroups[player.id]" 
                class="pending-card__select"
                :disabled="processing === player.id"
              >
                <option value="">-- Pilih --</option>
                <option v-for="group in groups" :key="group.id" :value="group.id">
                  {{ group.name }}
                </option>
              </select>
            </div>
            
            <div class="pending-card__buttons">
              <button 
                @click="approve(player.id)"
                :disabled="processing === player.id || !selectedGroups[player.id]"
                class="btn btn--approve"
              >
                {{ processing === player.id ? 'Processing...' : '✓ Approve' }}
              </button>
              <button 
                @click="reject(player.id)"
                :disabled="processing === player.id"
                class="btn btn--reject"
              >
                ✗ Reject
              </button>
            </div>
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

<style scoped>
.page-title {
  font-size: 1.5rem;
  font-weight: 800;
  color: #1e293b;
  margin-bottom: 1.5rem;
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

.empty-state {
  background: white;
  border-radius: 1rem;
  padding: 3rem;
  text-align: center;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.empty-state__icon {
  font-size: 3rem;
  display: block;
  margin-bottom: 1rem;
}

.empty-state h3 {
  font-size: 1.125rem;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 0.25rem;
}

.empty-state p {
  color: #64748b;
}

.pending-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.pending-card {
  background: white;
  border-radius: 1rem;
  padding: 1.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.pending-card__header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.25rem;
}

.pending-card__avatar {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: linear-gradient(135deg, #1e40af, #2563eb);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1.5rem;
  font-weight: 700;
  overflow: hidden;
  flex-shrink: 0;
}

.pending-card__avatar-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.pending-card__name {
  font-size: 1.125rem;
  font-weight: 700;
  color: #1e293b;
}

.pending-card__date {
  font-size: 0.8rem;
  color: #64748b;
}

.pending-card__details {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.75rem;
  margin-bottom: 1.25rem;
  padding: 1rem;
  background: #f8fafc;
  border-radius: 0.75rem;
}

@media (min-width: 768px) {
  .pending-card__details {
    grid-template-columns: repeat(4, 1fr);
  }
}

.detail-item__label {
  display: block;
  font-size: 0.7rem;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 0.125rem;
}

.detail-item__value {
  font-weight: 600;
  color: #1e293b;
}

.pending-card__actions {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

@media (min-width: 640px) {
  .pending-card__actions {
    flex-direction: row;
    align-items: center;
  }
}

.pending-card__group-select {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 0.75rem;
  flex: 1;
}

.pending-card__label {
  font-size: 0.875rem;
  font-weight: 600;
  color: #374151;
  white-space: nowrap;
}

.pending-card__select {
  flex: 1;
  padding: 0.625rem 1rem;
  border: 2px solid #e2e8f0;
  border-radius: 0.5rem;
  font-size: 0.9rem;
  background: white;
  cursor: pointer;
}

.pending-card__select:focus {
  outline: none;
  border-color: #2563eb;
}

.pending-card__buttons {
  display: flex;
  gap: 0.5rem;
}

.btn {
  padding: 0.625rem 1.25rem;
  border-radius: 0.5rem;
  font-weight: 600;
  font-size: 0.875rem;
  cursor: pointer;
  border: none;
  transition: all 0.2s;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn--approve {
  background: #059669;
  color: white;
}

.btn--approve:hover:not(:disabled) {
  background: #047857;
}

.btn--reject {
  background: #dc2626;
  color: white;
}

.btn--reject:hover:not(:disabled) {
  background: #b91c1c;
}
</style>
