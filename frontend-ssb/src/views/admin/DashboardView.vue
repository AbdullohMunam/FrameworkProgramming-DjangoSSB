<template>
  <AdminLayout>
    <div class="dashboard">
      <h1 class="dashboard__title">Dashboard</h1>
      <p class="dashboard__subtitle">Selamat datang di SSB Academy Admin Panel</p>
      
      <!-- Stats Cards -->
      <div class="stats-grid">
        <div class="stat-card stat-card--pending">
          <div class="stat-card__icon">⏳</div>
          <div class="stat-card__content">
            <span class="stat-card__value">{{ stats.pending }}</span>
            <span class="stat-card__label">Pending</span>
          </div>
        </div>
        <div class="stat-card stat-card--players">
          <div class="stat-card__icon">👥</div>
          <div class="stat-card__content">
            <span class="stat-card__value">{{ stats.players }}</span>
            <span class="stat-card__label">Total Players</span>
          </div>
        </div>
        <div class="stat-card stat-card--coaches">
          <div class="stat-card__icon">🎯</div>
          <div class="stat-card__content">
            <span class="stat-card__value">{{ stats.coaches }}</span>
            <span class="stat-card__label">Coaches</span>
          </div>
        </div>
        <div class="stat-card stat-card--groups">
          <div class="stat-card__icon">📂</div>
          <div class="stat-card__content">
            <span class="stat-card__value">{{ stats.groups }}</span>
            <span class="stat-card__label">Groups</span>
          </div>
        </div>
        <div class="stat-card stat-card--schedules">
          <div class="stat-card__icon">📅</div>
          <div class="stat-card__content">
            <span class="stat-card__value">{{ stats.schedules }}</span>
            <span class="stat-card__label">Schedules</span>
          </div>
        </div>
      </div>
      
      <!-- Pending Alert -->
      <div v-if="stats.pending > 0" class="pending-alert">
        <div class="pending-alert__content">
          <span class="pending-alert__icon">⚠️</span>
          <div>
            <p class="pending-alert__title">{{ stats.pending }} registrasi menunggu approval</p>
            <p class="pending-alert__desc">Review dan setujui pendaftaran baru</p>
          </div>
        </div>
        <router-link to="/admin/pending" class="pending-alert__btn">
          Lihat Sekarang →
        </router-link>
      </div>
      
      <!-- Quick Actions -->
      <h2 class="section-title">Quick Actions</h2>
      <div class="actions-grid">
        <router-link to="/admin/pending" class="action-card">
          <span class="action-card__icon">⏳</span>
          <h3 class="action-card__title">Pending Registrations</h3>
          <p class="action-card__desc">Review dan approve pendaftar baru</p>
        </router-link>
        
        <router-link to="/admin/players" class="action-card">
          <span class="action-card__icon">👥</span>
          <h3 class="action-card__title">Manage Players</h3>
          <p class="action-card__desc">Kelola data pemain</p>
        </router-link>
        
        <router-link to="/admin/coaches" class="action-card">
          <span class="action-card__icon">🎯</span>
          <h3 class="action-card__title">Manage Coaches</h3>
          <p class="action-card__desc">Kelola data pelatih</p>
        </router-link>
        
        <router-link to="/admin/schedules" class="action-card">
          <span class="action-card__icon">📅</span>
          <h3 class="action-card__title">Manage Schedules</h3>
          <p class="action-card__desc">Kelola jadwal latihan</p>
        </router-link>
      </div>
    </div>
  </AdminLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import AdminLayout from '@/layouts/AdminLayout.vue'
import { playersService, coachesService, groupsService, schedulesService } from '@/services'

const stats = ref({
  players: 0,
  coaches: 0,
  groups: 0,
  schedules: 0,
  pending: 0
})

onMounted(async () => {
  try {
    const [playersData, coachesData, groupsData, schedulesData, pendingData] = await Promise.all([
      playersService.getPlayers(),
      coachesService.getCoaches(),
      groupsService.getGroups(),
      schedulesService.getSchedules(),
      playersService.getPending()
    ])
    
    stats.value = {
      players: playersData.results?.length || playersData.length || 0,
      coaches: coachesData.results?.length || coachesData.length || 0,
      groups: groupsData.results?.length || groupsData.length || 0,
      schedules: schedulesData.results?.length || schedulesData.length || 0,
      pending: pendingData.length || 0
    }
  } catch (error) {
    console.error('Failed to load stats:', error)
  }
})
</script>

<style scoped>
.dashboard__title {
  font-size: 1.75rem;
  font-weight: 800;
  color: #1e293b;
  margin-bottom: 0.25rem;
}

.dashboard__subtitle {
  color: #64748b;
  margin-bottom: 2rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
  margin-bottom: 2rem;
}

@media (min-width: 768px) {
  .stats-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (min-width: 1024px) {
  .stats-grid {
    grid-template-columns: repeat(5, 1fr);
  }
}

.stat-card {
  background: white;
  border-radius: 1rem;
  padding: 1.25rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  transition: all 0.3s;
}

.stat-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.stat-card__icon {
  width: 48px;
  height: 48px;
  border-radius: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
}

.stat-card--pending .stat-card__icon { background: #fef3c7; }
.stat-card--players .stat-card__icon { background: #dbeafe; }
.stat-card--coaches .stat-card__icon { background: #d1fae5; }
.stat-card--groups .stat-card__icon { background: #ede9fe; }
.stat-card--schedules .stat-card__icon { background: #ffedd5; }

.stat-card__value {
  display: block;
  font-size: 1.75rem;
  font-weight: 800;
  color: #1e293b;
  line-height: 1;
}

.stat-card__label {
  font-size: 0.8rem;
  color: #64748b;
}

.pending-alert {
  background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
  border: 1px solid #f59e0b;
  border-radius: 1rem;
  padding: 1.25rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 2rem;
}

@media (min-width: 640px) {
  .pending-alert {
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
  }
}

.pending-alert__content {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.pending-alert__icon {
  font-size: 2rem;
}

.pending-alert__title {
  font-weight: 700;
  color: #92400e;
}

.pending-alert__desc {
  font-size: 0.875rem;
  color: #a16207;
}

.pending-alert__btn {
  background: #f59e0b;
  color: white;
  padding: 0.625rem 1.25rem;
  border-radius: 0.5rem;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.2s;
  white-space: nowrap;
}

.pending-alert__btn:hover {
  background: #d97706;
}

.section-title {
  font-size: 1.125rem;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 1rem;
}

.actions-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
}

@media (min-width: 640px) {
  .actions-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1024px) {
  .actions-grid {
    grid-template-columns: repeat(4, 1fr);
  }
}

.action-card {
  background: white;
  border-radius: 1rem;
  padding: 1.5rem;
  text-decoration: none;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  transition: all 0.3s;
  border: 2px solid transparent;
}

.action-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.12);
  border-color: #2563eb;
}

.action-card__icon {
  font-size: 2rem;
  display: block;
  margin-bottom: 0.75rem;
}

.action-card__title {
  font-size: 1rem;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 0.25rem;
}

.action-card__desc {
  font-size: 0.85rem;
  color: #64748b;
}
</style>
