<template>
  <nav class="user-nav">
    <div class="user-nav__container">
      <router-link to="/" class="user-nav__logo">
        <span class="user-nav__logo-icon">⚽</span>
        <span class="user-nav__logo-text">SSB Academy</span>
      </router-link>
      
      <div class="user-nav__links">
        <router-link to="/profile" class="user-nav__link" :class="{ 'user-nav__link--active': $route.path === '/profile' }">
          Profile
        </router-link>
        <router-link to="/schedules" class="user-nav__link" :class="{ 'user-nav__link--active': $route.path === '/schedules' }">
          Jadwal
        </router-link>
        <router-link to="/team" class="user-nav__link" :class="{ 'user-nav__link--active': $route.path === '/team' }">
          Tim Saya
        </router-link>
      </div>
      
      <button @click="$emit('logout')" class="user-nav__logout">
        <svg class="user-nav__logout-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
        </svg>
        <span class="user-nav__logout-text">Logout</span>
      </button>
    </div>
  </nav>
</template>

<script setup>
defineEmits(['logout'])
</script>

<style scoped>
.user-nav {
  background: linear-gradient(135deg, #1e40af 0%, #2563eb 100%);
  box-shadow: 0 4px 20px rgba(30, 64, 175, 0.3);
  position: sticky;
  top: 0;
  z-index: 100;
}

.user-nav__container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 1rem 1.5rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}

.user-nav__logo {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  text-decoration: none;
}

.user-nav__logo-icon {
  font-size: 1.5rem;
}

.user-nav__logo-text {
  font-size: 1.25rem;
  font-weight: 800;
  color: white;
}

.user-nav__links {
  display: flex;
  gap: 0.5rem;
}

@media (min-width: 640px) {
  .user-nav__links {
    gap: 1rem;
  }
}

.user-nav__link {
  padding: 0.5rem 1rem;
  color: rgba(255, 255, 255, 0.8);
  text-decoration: none;
  font-weight: 500;
  border-radius: 9999px;
  transition: all 0.3s;
  font-size: 0.9rem;
}

@media (min-width: 640px) {
  .user-nav__link {
    padding: 0.5rem 1.25rem;
  }
}

.user-nav__link:hover {
  color: white;
  background: rgba(255, 255, 255, 0.15);
}

.user-nav__link--active {
  color: white;
  background: rgba(255, 255, 255, 0.2);
  font-weight: 600;
}

.user-nav__logout {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: rgba(255, 255, 255, 0.15);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 9999px;
  color: white;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 0.9rem;
}

.user-nav__logout:hover {
  background: #dc2626;
  border-color: #dc2626;
}

.user-nav__logout-icon {
  width: 18px;
  height: 18px;
}

.user-nav__logout-text {
  display: none;
}

@media (min-width: 640px) {
  .user-nav__logout-text {
    display: inline;
  }
}
</style>
