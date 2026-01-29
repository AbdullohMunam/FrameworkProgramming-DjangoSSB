<template>
  <div class="schedules-page">
    <UserNavbar @logout="handleLogout" />
    
    <div class="schedules-page__container">
      <div class="schedules-page__header">
        <h2 class="schedules-page__title">Jadwal Latihan</h2>
        <p v-if="userGroup" class="schedules-page__group">
          📋 Kelompok: <strong>{{ userGroup }}</strong>
        </p>
        <p v-else class="schedules-page__no-group">
          ⚠️ Anda belum ditugaskan ke kelompok manapun
        </p>
      </div>
      
      <div v-if="loading" class="schedules-page__loading">
        <div class="schedules-page__spinner"></div>
        <p>Memuat jadwal...</p>
      </div>
      
      <div v-else-if="schedules.length === 0" class="schedules-page__empty">
        <div class="schedules-page__empty-icon">📅</div>
        <h3>Belum Ada Jadwal</h3>
        <p>{{ userGroup ? 'Belum ada jadwal latihan untuk kelompok Anda' : 'Anda belum ditugaskan ke kelompok' }}</p>
      </div>
      
      <div v-else class="schedules-grid">
        <div v-for="schedule in schedules" :key="schedule.id" class="schedule-card">
          <div class="schedule-card__date">
            <span class="schedule-card__day">{{ formatDay(schedule.date) }}</span>
            <span class="schedule-card__month">{{ formatMonth(schedule.date) }}</span>
          </div>
          <div class="schedule-card__info">
            <p class="schedule-card__datetime">
              <span class="schedule-card__icon">🗓️</span>
              {{ formatDate(schedule.date) }}
            </p>
            <p class="schedule-card__time">
              <span class="schedule-card__icon">⏰</span>
              {{ schedule.time }}
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { schedulesService, playersService } from '@/services'
import UserNavbar from '@/components/UserNavbar.vue'

const router = useRouter()
const authStore = useAuthStore()
const schedules = ref([])
const loading = ref(true)
const userGroup = ref(null)

async function loadSchedules() {
  try {
    const profile = await playersService.getMyProfile()
    userGroup.value = profile.group_name
    
    const response = await schedulesService.getSchedules()
    const allSchedules = response.results || response || []
    
    if (profile.group) {
      schedules.value = allSchedules
        .filter(schedule => schedule.group === profile.group)
        .sort((a, b) => new Date(a.date) - new Date(b.date))
    } else {
      schedules.value = []
    }
  } catch (error) {
    console.error('Failed to load schedules:', error)
    schedules.value = []
  } finally {
    loading.value = false
  }
}

function formatDay(dateStr) {
  return new Date(dateStr).getDate()
}

function formatMonth(dateStr) {
  return new Date(dateStr).toLocaleDateString('id-ID', { month: 'short' })
}

function formatDate(dateStr) {
  return new Date(dateStr).toLocaleDateString('id-ID', {
    weekday: 'long',
    day: 'numeric',
    month: 'long',
    year: 'numeric'
  })
}

async function handleLogout() {
  await authStore.logout()
  router.push('/login')
}

onMounted(loadSchedules)
</script>

<style scoped>
.schedules-page {
  min-height: 100vh;
  background: linear-gradient(180deg, #f0f9ff 0%, #f9fafb 100%);
}

.schedules-page__container {
  max-width: 900px;
  margin: 0 auto;
  padding: 2rem 1.5rem;
}

.schedules-page__header {
  margin-bottom: 2rem;
}

.schedules-page__title {
  font-size: 1.75rem;
  font-weight: 800;
  color: #1f2937;
  margin-bottom: 0.5rem;
}

.schedules-page__group {
  color: #6b7280;
  font-size: 1rem;
}

.schedules-page__no-group {
  color: #dc2626;
  font-size: 0.9rem;
}

.schedules-page__loading {
  text-align: center;
  padding: 3rem;
  color: #6b7280;
}

.schedules-page__spinner {
  width: 40px;
  height: 40px;
  border: 3px solid #e5e7eb;
  border-top-color: #2563eb;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.schedules-page__empty {
  background: white;
  border-radius: 1.5rem;
  padding: 3rem;
  text-align: center;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.schedules-page__empty-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.schedules-page__empty h3 {
  font-size: 1.25rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 0.5rem;
}

.schedules-page__empty p {
  color: #6b7280;
}

.schedules-grid {
  display: grid;
  gap: 1rem;
}

@media (min-width: 640px) {
  .schedules-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

.schedule-card {
  background: white;
  border-radius: 1rem;
  padding: 1.5rem;
  display: flex;
  gap: 1.5rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  transition: all 0.3s;
}

.schedule-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
}

.schedule-card__date {
  background: linear-gradient(135deg, #1e40af, #2563eb);
  color: white;
  padding: 1rem;
  border-radius: 0.75rem;
  text-align: center;
  min-width: 70px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.schedule-card__day {
  font-size: 1.75rem;
  font-weight: 800;
  line-height: 1;
}

.schedule-card__month {
  font-size: 0.875rem;
  text-transform: uppercase;
  opacity: 0.9;
}

.schedule-card__info {
  flex: 1;
}

.schedule-card__group {
  font-size: 1.125rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 0.75rem;
}

.schedule-card__datetime,
.schedule-card__time {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #6b7280;
  font-size: 0.9rem;
  margin-bottom: 0.25rem;
}

.schedule-card__icon {
  font-size: 1rem;
}
</style>
