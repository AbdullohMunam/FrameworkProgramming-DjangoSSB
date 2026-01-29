<template>
  <div class="team-page">
    <UserNavbar @logout="handleLogout" />
    
    <div class="team-page__container">
      <div class="team-page__header">
        <h2 class="team-page__title">Tim Saya</h2>
        <p v-if="groupName" class="team-page__group">
          ⚽ Kelompok: <strong>{{ groupName }}</strong>
        </p>
      </div>
      
      <div v-if="loading" class="team-page__loading">
        <div class="team-page__spinner"></div>
        <p>Memuat data tim...</p>
      </div>
      
      <div v-else-if="!groupName" class="team-page__empty">
        <div class="team-page__empty-icon">👥</div>
        <h3>Belum Ada Tim</h3>
        <p>Anda belum ditugaskan ke kelompok manapun</p>
      </div>
      
      <template v-else>
        <!-- Coach Section -->
        <div v-if="coach" class="coach-section">
          <h3 class="section-title">
            <span class="section-title__icon">🎯</span>
            Pelatih
          </h3>
          <div class="coach-card">
            <div class="coach-card__avatar">
              <img v-if="coach.photo" :src="coach.photo" class="coach-card__avatar-img" />
              <span v-else class="coach-card__avatar-placeholder">{{ coach.name?.charAt(0)?.toUpperCase() || '?' }}</span>
            </div>
            <div class="coach-card__info">
              <h4 class="coach-card__name">{{ coach.name }}</h4>
              <p class="coach-card__license">🏅 {{ coach.license_level || 'Lisensi -' }}</p>
              <p v-if="coach.phone" class="coach-card__phone">📞 {{ coach.phone }}</p>
            </div>
          </div>
        </div>
        
        <!-- Team Members -->
        <div class="members-section">
          <h3 class="section-title">
            <span class="section-title__icon">👥</span>
            Anggota Tim ({{ teammates.length }} pemain)
          </h3>
          
          <div v-if="teammates.length === 0" class="members-empty">
            Belum ada anggota tim lainnya
          </div>
          
          <div v-else class="members-grid">
            <div 
              v-for="player in teammates" 
              :key="player.id" 
              class="member-card"
              :class="{ 'member-card--me': player.id === myId }"
            >
              <div class="member-card__avatar">
                <img v-if="player.photo" :src="player.photo" class="member-card__avatar-img" />
                <span v-else class="member-card__avatar-placeholder">
                  {{ player.name ? player.name.charAt(0).toUpperCase() : '?' }}
                </span>
              </div>
              <div class="member-card__info">
                <h4 class="member-card__name">
                  {{ player.name }}
                  <span v-if="player.id === myId" class="member-card__me-badge">Anda</span>
                </h4>
                <p class="member-card__position">
                  {{ getPositionEmoji(player.position) }} {{ player.position }}
                </p>
                <p class="member-card__age">{{ player.age }} tahun</p>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Position Summary -->
        <div class="position-section">
          <h3 class="section-title">
            <span class="section-title__icon">📊</span>
            Komposisi Tim
          </h3>
          <div class="position-grid">
            <div class="position-card position-card--gk">
              <span class="position-card__count">{{ positionCounts.Goalkeeper || 0 }}</span>
              <span class="position-card__label">🧤 GK</span>
            </div>
            <div class="position-card position-card--def">
              <span class="position-card__count">{{ positionCounts.Defender || 0 }}</span>
              <span class="position-card__label">🛡️ DEF</span>
            </div>
            <div class="position-card position-card--mid">
              <span class="position-card__count">{{ positionCounts.Midfielder || 0 }}</span>
              <span class="position-card__label">⚡ MID</span>
            </div>
            <div class="position-card position-card--fwd">
              <span class="position-card__count">{{ positionCounts.Forward || 0 }}</span>
              <span class="position-card__label">⚽ FWD</span>
            </div>
          </div>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { playersService, coachesService, groupsService } from '@/services'
import UserNavbar from '@/components/UserNavbar.vue'

const router = useRouter()
const authStore = useAuthStore()
const loading = ref(true)
const groupName = ref(null)
const groupId = ref(null)
const coach = ref(null)
const teammates = ref([])
const myId = ref(null)

const positionCounts = computed(() => {
  const counts = {}
  teammates.value.forEach(player => {
    if (player.position) {
      counts[player.position] = (counts[player.position] || 0) + 1
    }
  })
  return counts
})

function getPositionEmoji(position) {
  const emojis = {
    'Goalkeeper': '🧤',
    'Defender': '🛡️',
    'Midfielder': '⚡',
    'Forward': '⚽'
  }
  return emojis[position] || ''
}

async function loadTeamData() {
  try {
    const profile = await playersService.getMyProfile()
    myId.value = profile.id
    groupName.value = profile.group_name
    groupId.value = profile.group
    
    if (!groupId.value) {
      loading.value = false
      return
    }
    
    const playersResponse = await playersService.getPlayers()
    const allPlayers = playersResponse.results || playersResponse || []
    teammates.value = allPlayers
      .filter(p => p.group === groupId.value && p.status === 'approved')
      .sort((a, b) => {
        if (a.id === myId.value) return -1
        if (b.id === myId.value) return 1
        
        const positionOrder = { 'Goalkeeper': 1, 'Defender': 2, 'Midfielder': 3, 'Forward': 4 }
        const posA = positionOrder[a.position] || 5
        const posB = positionOrder[b.position] || 5
        
        if (posA !== posB) return posA - posB
        return (a.name || '').localeCompare(b.name || '')
      })
    
    const groupsResponse = await groupsService.getGroups()
    const allGroups = groupsResponse.results || groupsResponse || []
    const myGroup = allGroups.find(g => g.id === groupId.value)
    
    if (myGroup && myGroup.coach) {
      const coachesResponse = await coachesService.getCoaches()
      const allCoaches = coachesResponse.results || coachesResponse || []
      coach.value = allCoaches.find(c => c.id === myGroup.coach)
    }
  } catch (error) {
    console.error('Failed to load team data:', error)
  } finally {
    loading.value = false
  }
}

async function handleLogout() {
  await authStore.logout()
  router.push('/login')
}

onMounted(loadTeamData)
</script>

<style scoped>
.team-page {
  min-height: 100vh;
  background: linear-gradient(180deg, #f0f9ff 0%, #f9fafb 100%);
}

.team-page__container {
  max-width: 900px;
  margin: 0 auto;
  padding: 2rem 1.5rem;
}

.team-page__header {
  margin-bottom: 2rem;
}

.team-page__title {
  font-size: 1.75rem;
  font-weight: 800;
  color: #1f2937;
  margin-bottom: 0.5rem;
}

.team-page__group {
  color: #6b7280;
  font-size: 1rem;
}

.team-page__loading {
  text-align: center;
  padding: 3rem;
  color: #6b7280;
}

.team-page__spinner {
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

.team-page__empty {
  background: white;
  border-radius: 1.5rem;
  padding: 3rem;
  text-align: center;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.team-page__empty-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.team-page__empty h3 {
  font-size: 1.25rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 0.5rem;
}

.team-page__empty p {
  color: #6b7280;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1.125rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 1rem;
}

.section-title__icon {
  font-size: 1.25rem;
}

/* Coach Section */
.coach-section {
  margin-bottom: 2rem;
}

.coach-card {
  background: white;
  border-radius: 1rem;
  padding: 1.5rem;
  display: flex;
  gap: 1.5rem;
  align-items: center;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.coach-card__avatar {
  width: 80px;
  height: 80px;
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
  font-size: 1.25rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 0.5rem;
}

.coach-card__license,
.coach-card__phone {
  color: #6b7280;
  font-size: 0.9rem;
  margin-bottom: 0.25rem;
}

/* Members Section */
.members-section {
  margin-bottom: 2rem;
}

.members-empty {
  background: white;
  border-radius: 1rem;
  padding: 2rem;
  text-align: center;
  color: #6b7280;
}

.members-grid {
  display: grid;
  gap: 1rem;
}

@media (min-width: 640px) {
  .members-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1024px) {
  .members-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

.member-card {
  background: white;
  border-radius: 1rem;
  padding: 1.25rem;
  display: flex;
  gap: 1rem;
  align-items: center;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  transition: all 0.3s;
  border: 2px solid transparent;
}

.member-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
}

.member-card--me {
  background: linear-gradient(135deg, #eff6ff, #dbeafe);
  border-color: #2563eb;
}

.member-card__avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: linear-gradient(135deg, #1e40af, #2563eb);
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  flex-shrink: 0;
}

.member-card__avatar-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.member-card__avatar-placeholder {
  color: white;
  font-weight: 700;
  font-size: 1.25rem;
}

.member-card__name {
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 0.25rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.member-card__me-badge {
  background: #2563eb;
  color: white;
  padding: 0.125rem 0.5rem;
  border-radius: 9999px;
  font-size: 0.7rem;
  font-weight: 600;
}

.member-card__position,
.member-card__age {
  color: #6b7280;
  font-size: 0.85rem;
}

/* Position Section */
.position-section {
  margin-bottom: 2rem;
}

.position-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
}

.position-card {
  background: white;
  border-radius: 1rem;
  padding: 1.5rem 1rem;
  text-align: center;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.position-card__count {
  display: block;
  font-size: 2rem;
  font-weight: 800;
  margin-bottom: 0.25rem;
}

.position-card__label {
  font-size: 0.85rem;
  color: #6b7280;
}

.position-card--gk .position-card__count { color: #059669; }
.position-card--def .position-card__count { color: #2563eb; }
.position-card--mid .position-card__count { color: #d97706; }
.position-card--fwd .position-card__count { color: #dc2626; }
</style>
