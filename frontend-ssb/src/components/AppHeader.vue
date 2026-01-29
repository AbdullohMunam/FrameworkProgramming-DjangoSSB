<template>
  <header 
    class="header"
    :class="{ 'header--scrolled': isScrolled }"
  >
    <div class="header__container">
      <!-- Logo -->
      <router-link to="/" class="header__logo">
        <span class="header__logo-icon">⚽</span>
        <span class="header__logo-text">SSB Academy</span>
      </router-link>

      <!-- Desktop Navigation -->
      <nav class="header__nav">
        <a href="#about" class="header__link">Tentang Kami</a>
        <a href="#achievements" class="header__link">Prestasi</a>
        <a href="#coaches" class="header__link">Pelatih</a>
        <a href="#contact" class="header__link">Kontak</a>
      </nav>

      <!-- Auth Buttons -->
      <div class="header__auth">
        <router-link to="/login" class="header__btn header__btn--outline">
          Login
        </router-link>
        <router-link to="/register" class="header__btn header__btn--solid">
          Daftar
        </router-link>
      </div>

      <!-- Mobile Menu Button -->
      <button class="header__menu-btn" @click="toggleMobile">
        <span class="header__menu-icon" :class="{ 'header__menu-icon--open': isMobileOpen }"></span>
      </button>
    </div>

    <!-- Mobile Menu -->
    <div class="header__mobile" :class="{ 'header__mobile--open': isMobileOpen }">
      <a href="#about" class="header__mobile-link" @click="closeMobile">Tentang Kami</a>
      <a href="#achievements" class="header__mobile-link" @click="closeMobile">Prestasi</a>
      <a href="#coaches" class="header__mobile-link" @click="closeMobile">Pelatih</a>
      <a href="#contact" class="header__mobile-link" @click="closeMobile">Kontak</a>
      <div class="header__mobile-auth">
        <router-link to="/login" class="header__btn header__btn--outline" @click="closeMobile">
          Login
        </router-link>
        <router-link to="/register" class="header__btn header__btn--solid" @click="closeMobile">
          Daftar
        </router-link>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const isScrolled = ref(false)
const isMobileOpen = ref(false)

const handleScroll = () => {
  isScrolled.value = window.scrollY > 50
}

const toggleMobile = () => {
  isMobileOpen.value = !isMobileOpen.value
}

const closeMobile = () => {
  isMobileOpen.value = false
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>

<style scoped>
.header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  padding: 1rem 0;
  transition: all 0.3s ease;
  background: transparent;
}

.header--scrolled {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  box-shadow: 0 2px 20px rgba(0, 0, 0, 0.1);
  padding: 0.75rem 0;
}

.header--scrolled .header__logo-text,
.header--scrolled .header__link {
  color: #1f2937;
}

.header--scrolled .header__btn--outline {
  color: #1e40af;
  border-color: #1e40af;
}

.header__container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 1.5rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.header__logo {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  text-decoration: none;
}

.header__logo-icon {
  font-size: 2rem;
  animation: bounce 2s infinite;
}

.header__logo-text {
  font-size: 1.5rem;
  font-weight: 800;
  color: white;
  transition: color 0.3s;
}

.header__nav {
  display: none;
  gap: 2rem;
}

@media (min-width: 768px) {
  .header__nav {
    display: flex;
  }
}

.header__link {
  color: white;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.3s;
  position: relative;
}

.header__link::after {
  content: '';
  position: absolute;
  bottom: -4px;
  left: 0;
  width: 0;
  height: 2px;
  background: #f59e0b;
  transition: width 0.3s;
}

.header__link:hover::after {
  width: 100%;
}

.header__auth {
  display: none;
  gap: 1rem;
}

@media (min-width: 768px) {
  .header__auth {
    display: flex;
  }
}

.header__btn {
  padding: 0.625rem 1.5rem;
  border-radius: 9999px;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.3s;
  font-size: 0.9rem;
}

.header__btn--outline {
  color: white;
  border: 2px solid white;
  background: transparent;
}

.header__btn--outline:hover {
  background: white;
  color: #1e40af;
}

.header__btn--solid {
  background: linear-gradient(135deg, #f59e0b, #d97706);
  color: white;
  border: none;
}

.header__btn--solid:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(245, 158, 11, 0.4);
}

.header__menu-btn {
  display: flex;
  padding: 0.5rem;
  background: none;
  border: none;
  cursor: pointer;
}

@media (min-width: 768px) {
  .header__menu-btn {
    display: none;
  }
}

.header__menu-icon {
  width: 24px;
  height: 2px;
  background: white;
  position: relative;
  transition: all 0.3s;
}

.header--scrolled .header__menu-icon,
.header--scrolled .header__menu-icon::before,
.header--scrolled .header__menu-icon::after {
  background: #1f2937;
}

.header__menu-icon::before,
.header__menu-icon::after {
  content: '';
  position: absolute;
  width: 24px;
  height: 2px;
  background: white;
  left: 0;
  transition: all 0.3s;
}

.header__menu-icon::before {
  top: -7px;
}

.header__menu-icon::after {
  top: 7px;
}

.header__menu-icon--open {
  background: transparent;
}

.header__menu-icon--open::before {
  transform: rotate(45deg);
  top: 0;
}

.header__menu-icon--open::after {
  transform: rotate(-45deg);
  top: 0;
}

.header__mobile {
  display: none;
  flex-direction: column;
  padding: 1rem 1.5rem 1.5rem;
  background: white;
  margin-top: 1rem;
  border-radius: 1rem;
  margin-left: 1rem;
  margin-right: 1rem;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
}

.header__mobile--open {
  display: flex;
  animation: slideDown 0.3s ease;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.header__mobile-link {
  padding: 0.75rem 0;
  color: #1f2937;
  text-decoration: none;
  font-weight: 500;
  border-bottom: 1px solid #e5e7eb;
}

.header__mobile-auth {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
  padding-top: 1rem;
}

.header__mobile-auth .header__btn--outline {
  color: #1e40af;
  border-color: #1e40af;
  flex: 1;
  text-align: center;
}

.header__mobile-auth .header__btn--solid {
  flex: 1;
  text-align: center;
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-5px); }
}
</style>
