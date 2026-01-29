<template>
  <div class="landing">
    <!-- Header -->
    <AppHeader />

    <!-- Hero Section -->
    <section class="hero">
      <div class="hero__bg"></div>
      <div class="hero__content">
        <!-- <div class="hero__badge animate-fade-in-up">
          🏆 Sejak 2010 di Kota Malang
        </div> -->
        <h1 class="hero__title animate-fade-in-up delay-100">
          Membentuk <span class="hero__highlight">Generasi Juara</span><br>
          dari Kota Malang
        </h1>
        <p class="hero__subtitle animate-fade-in-up delay-200">
          Sekolah Sepak Bola terbaik dengan pelatih berlisensi AFC untuk anak usia 6-18 tahun
        </p>
        <div class="hero__buttons animate-fade-in-up delay-300">
          <router-link to="/register" class="hero__btn hero__btn--primary">
            Daftar Sekarang
            <span class="hero__btn-arrow">→</span>
          </router-link>
          <router-link to="/login" class="hero__btn hero__btn--secondary">
            Login Member
          </router-link>
        </div>
        <div class="hero__scroll animate-fade-in delay-500">
          <span>Scroll untuk lihat lebih</span>
          <div class="hero__scroll-icon">↓</div>
        </div>
      </div>
    </section>

    <!-- About Section -->
    <section id="about" class="about">
      <div class="about__container">
        <div class="about__content" ref="aboutRef">
          <span class="section-badge">Tentang Kami</span>
          <h2 class="section-title">SSB Academy Malang</h2>
          <p class="about__text">
            SSB Academy adalah sekolah sepak bola yang berdiri sejak 2010 di Kota Malang, Jawa Timur. 
            Kami berkomitmen mengembangkan bakat sepak bola anak-anak Indonesia dengan metode pelatihan 
            modern dan pelatih berlisensi AFC. Dengan fasilitas lengkap dan program terstruktur, 
            kami telah melahirkan puluhan pemain yang berkarir di liga profesional Indonesia.
          </p>
        </div>
        <div class="about__image">
          <div class="about__image-wrapper animate-float">
            ⚽
          </div>
        </div>
      </div>
    </section>

    <!-- Stats Section -->
    <section class="stats">
      <div class="stats__container">
        <div class="stats__card" v-for="(stat, index) in statsData" :key="stat.label">
          <div class="stats__icon">{{ stat.icon }}</div>
          <div class="stats__number" :style="{ animationDelay: `${index * 0.1}s` }">
            {{ stat.value }}+
          </div>
          <div class="stats__label">{{ stat.label }}</div>
        </div>
      </div>
    </section>

    <!-- Achievements Section -->
    <section id="achievements" class="achievements">
      <div class="achievements__container">
        <span class="section-badge">Prestasi</span>
        <h2 class="section-title">Raihan Kami</h2>
        <div class="achievements__grid">
          <div 
            class="achievement-card" 
            v-for="(achievement, index) in achievements" 
            :key="index"
          >
            <div class="achievement-card__icon">{{ achievement.icon }}</div>
            <h3 class="achievement-card__title">{{ achievement.title }}</h3>
            <p class="achievement-card__desc">{{ achievement.description }}</p>
            <span class="achievement-card__year">{{ achievement.year }}</span>
          </div>
        </div>
      </div>
    </section>

    <!-- Coaches Section -->
    <section id="coaches" class="coaches">
      <div class="coaches__container">
        <span class="section-badge">Tim Pelatih</span>
        <h2 class="section-title">Pelatih Profesional</h2>
        <div class="coaches__grid">
          <div 
            class="coach-card" 
            v-for="coach in featuredCoaches" 
            :key="coach.id"
          >
            <div class="coach-card__avatar">
              {{ coach.name.charAt(0) }}
            </div>
            <h3 class="coach-card__name">{{ coach.name }}</h3>
            <p class="coach-card__license">{{ coach.license_level }}</p>
          </div>
          <div class="coach-card coach-card--placeholder" v-if="featuredCoaches.length === 0">
            <div class="coach-card__avatar">?</div>
            <h3 class="coach-card__name">Data pelatih</h3>
            <p class="coach-card__license">Segera hadir</p>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="cta">
      <div class="cta__container">
        <h2 class="cta__title">Siap Bergabung?</h2>
        <p class="cta__text">Daftarkan anak Anda sekarang dan mulai perjalanan menjadi pemain sepak bola profesional</p>
        <router-link to="/register" class="cta__btn">
          Daftar Sekarang
        </router-link>
      </div>
    </section>

    <!-- Footer -->
    <AppFooter />
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import AppHeader from '@/components/AppHeader.vue'
import AppFooter from '@/components/AppFooter.vue'
import { playersService, coachesService, groupsService, schedulesService } from '@/services'

const stats = ref({
  players: 0,
  coaches: 0,
  groups: 0,
  schedules: 0
})

const featuredCoaches = ref([])

const statsData = computed(() => [
  { icon: '👥', value: stats.value.players, label: 'Pemain Aktif' },
  { icon: '🎯', value: stats.value.coaches, label: 'Pelatih Berlisensi' },
  { icon: '⚽', value: stats.value.groups, label: 'Kelompok Latihan' },
  { icon: '📅', value: stats.value.schedules, label: 'Jadwal Mingguan' }
])

const achievements = ref([
  {
    icon: '🥇',
    title: 'Juara 1 Piala Gubernur Jatim',
    description: 'Kategori U-15 mengalahkan 32 tim dari seluruh Jawa Timur',
    year: '2025'
  },
  {
    icon: '🥈',
    title: 'Runner-up Turnamen Nasional',
    description: 'Kompetisi nasional U-17 di Jakarta dengan 64 peserta',
    year: '2024'
  },
  {
    icon: '🏆',
    title: 'Best Academy Award',
    description: 'Penghargaan sebagai SSB terbaik se-Malang Raya',
    year: '2023'
  },
  {
    icon: '⭐',
    title: '15+ Pemain Profesional',
    description: 'Alumni yang berkarir di Liga 1 dan Liga 2 Indonesia',
    year: '2010-2025'
  }
])

onMounted(async () => {
  try {
    const [playersData, coachesData, groupsData, schedulesData] = await Promise.all([
      playersService.getPlayers(),
      coachesService.getCoaches(),
      groupsService.getGroups(),
      schedulesService.getSchedules()
    ])
    
    stats.value = {
      players: playersData.results?.length || playersData.length || 0,
      coaches: coachesData.results?.length || coachesData.length || 0,
      groups: groupsData.results?.length || groupsData.length || 0,
      schedules: schedulesData.results?.length || schedulesData.length || 0
    }
    
    const allCoaches = coachesData.results || coachesData
    featuredCoaches.value = allCoaches.slice(0, 3)
  } catch (error) {
    console.error('Failed to load data:', error)
  }
})
</script>

<style scoped>
/* Landing base */
.landing {
  min-height: 100vh;
  background: #f9fafb;
}

/* Section components */
.section-badge {
  display: inline-block;
  background: linear-gradient(135deg, #1e40af 0%, #2563eb 100%);
  color: white;
  padding: 0.5rem 1.25rem;
  border-radius: 9999px;
  font-size: 0.875rem;
  font-weight: 600;
  margin-bottom: 1rem;
}

.section-title {
  font-size: 2.5rem;
  font-weight: 800;
  color: #1f2937;
  margin-bottom: 1.5rem;
}

@media (min-width: 768px) {
  .section-title {
    font-size: 3rem;
  }
}

/* Hero Section */
.hero {
  position: relative;
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.hero__bg {
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, #1e40af 0%, #2563eb 50%, #1e40af 100%);
  background-size: 200% 200%;
  animation: gradientMove 8s ease infinite;
}

.hero__bg::before {
  content: '';
  position: absolute;
  inset: 0;
  background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.05'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
  opacity: 0.5;
}

@keyframes gradientMove {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

.hero__content {
  position: relative;
  z-index: 10;
  text-align: center;
  padding: 6rem 1.5rem 3rem;
  max-width: 900px;
}

.hero__badge {
  display: inline-block;
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(10px);
  color: white;
  padding: 0.625rem 1.5rem;
  border-radius: 9999px;
  font-size: 0.9rem;
  font-weight: 500;
  margin-bottom: 2rem;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.hero__title {
  font-size: 2.5rem;
  font-weight: 900;
  color: white;
  line-height: 1.2;
  margin-bottom: 1.5rem;
}

@media (min-width: 768px) {
  .hero__title {
    font-size: 4rem;
  }
}

.hero__highlight {
  background: linear-gradient(135deg, #f59e0b, #fbbf24);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero__subtitle {
  font-size: 1.125rem;
  color: rgba(255, 255, 255, 0.9);
  margin-bottom: 2.5rem;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}

@media (min-width: 768px) {
  .hero__subtitle {
    font-size: 1.25rem;
  }
}

.hero__buttons {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  justify-content: center;
  margin-bottom: 3rem;
}

@media (min-width: 640px) {
  .hero__buttons {
    flex-direction: row;
  }
}

.hero__btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 1rem 2rem;
  border-radius: 9999px;
  font-weight: 700;
  font-size: 1rem;
  text-decoration: none;
  transition: all 0.3s;
}

.hero__btn--primary {
  background: linear-gradient(135deg, #f59e0b, #d97706);
  color: white;
  box-shadow: 0 4px 20px rgba(245, 158, 11, 0.4);
}

.hero__btn--primary:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 30px rgba(245, 158, 11, 0.5);
}

.hero__btn-arrow {
  transition: transform 0.3s;
}

.hero__btn--primary:hover .hero__btn-arrow {
  transform: translateX(5px);
}

.hero__btn--secondary {
  background: transparent;
  color: white;
  border: 2px solid white;
}

.hero__btn--secondary:hover {
  background: white;
  color: #1e40af;
}

.hero__scroll {
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.875rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
}

.hero__scroll-icon {
  animation: bounce 2s infinite;
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(8px); }
}

/* About Section */
.about {
  padding: 6rem 1.5rem;
  background: white;
}

.about__container {
  max-width: 1280px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1fr;
  gap: 3rem;
  align-items: center;
}

@media (min-width: 768px) {
  .about__container {
    grid-template-columns: 1fr 1fr;
  }
}

.about__text {
  font-size: 1.125rem;
  color: #4b5563;
  line-height: 1.8;
}

.about__image {
  display: flex;
  justify-content: center;
}

.about__image-wrapper {
  width: 200px;
  height: 200px;
  background: linear-gradient(135deg, #1e40af 0%, #2563eb 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 5rem;
  box-shadow: 0 20px 60px rgba(30, 64, 175, 0.3);
}

/* Stats Section */
.stats {
  padding: 4rem 1.5rem;
  background: linear-gradient(135deg, #1f2937 0%, #111827 100%);
}

.stats__container {
  max-width: 1280px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
}

@media (min-width: 768px) {
  .stats__container {
    grid-template-columns: repeat(4, 1fr);
  }
}

.stats__card {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  border-radius: 1rem;
  padding: 2rem 1rem;
  text-align: center;
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.3s;
}

.stats__card:hover {
  transform: translateY(-5px);
  background: rgba(255, 255, 255, 0.1);
}

.stats__icon {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.stats__number {
  font-size: 2.5rem;
  font-weight: 800;
  color: #f59e0b;
  margin-bottom: 0.5rem;
}

.stats__label {
  color: rgba(255, 255, 255, 0.8);
  font-size: 0.9rem;
}

/* Achievements Section */
.achievements {
  padding: 6rem 1.5rem;
  background: #f9fafb;
  text-align: center;
}

.achievements__container {
  max-width: 1280px;
  margin: 0 auto;
}

.achievements__grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1.5rem;
  margin-top: 3rem;
}

@media (min-width: 640px) {
  .achievements__grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1024px) {
  .achievements__grid {
    grid-template-columns: repeat(4, 1fr);
  }
}

.achievement-card {
  background: white;
  border-radius: 1.5rem;
  padding: 2rem;
  text-align: center;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
  border: 1px solid #e5e7eb;
  transition: all 0.3s;
  position: relative;
  overflow: hidden;
}

.achievement-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
  border-color: #f59e0b;
}

.achievement-card__icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.achievement-card__title {
  font-size: 1.125rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 0.75rem;
}

.achievement-card__desc {
  font-size: 0.875rem;
  color: #6b7280;
  line-height: 1.6;
  margin-bottom: 1rem;
}

.achievement-card__year {
  display: inline-block;
  background: linear-gradient(135deg, #1e40af, #2563eb);
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 600;
}

/* Coaches Section */
.coaches {
  padding: 6rem 1.5rem;
  background: white;
  text-align: center;
}

.coaches__container {
  max-width: 1280px;
  margin: 0 auto;
}

.coaches__grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 2rem;
  margin-top: 3rem;
}

@media (min-width: 768px) {
  .coaches__grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

.coach-card {
  background: #f9fafb;
  border-radius: 1.5rem;
  padding: 2.5rem 2rem;
  transition: all 0.3s;
}

.coach-card:hover {
  background: linear-gradient(135deg, #1e40af 0%, #2563eb 100%);
  transform: translateY(-5px);
}

.coach-card:hover .coach-card__name,
.coach-card:hover .coach-card__license {
  color: white;
}

.coach-card:hover .coach-card__avatar {
  background: rgba(255, 255, 255, 0.2);
  color: white;
}

.coach-card__avatar {
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, #1e40af, #2563eb);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1.5rem;
  font-size: 2rem;
  font-weight: 700;
  color: white;
  transition: all 0.3s;
}

.coach-card__name {
  font-size: 1.25rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 0.5rem;
  transition: color 0.3s;
}

.coach-card__license {
  color: #6b7280;
  font-size: 0.9rem;
  transition: color 0.3s;
}

/* CTA Section */
.cta {
  padding: 6rem 1.5rem;
  background: linear-gradient(135deg, #1e40af 0%, #2563eb 100%);
  text-align: center;
}

.cta__container {
  max-width: 700px;
  margin: 0 auto;
}

.cta__title {
  font-size: 2.5rem;
  font-weight: 800;
  color: white;
  margin-bottom: 1rem;
}

.cta__text {
  font-size: 1.125rem;
  color: rgba(255, 255, 255, 0.9);
  margin-bottom: 2rem;
}

.cta__btn {
  display: inline-block;
  background: linear-gradient(135deg, #f59e0b, #d97706);
  color: white;
  padding: 1rem 3rem;
  border-radius: 9999px;
  font-weight: 700;
  font-size: 1.125rem;
  text-decoration: none;
  transition: all 0.3s;
  box-shadow: 0 4px 20px rgba(245, 158, 11, 0.4);
}

.cta__btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 30px rgba(245, 158, 11, 0.5);
}
</style>
