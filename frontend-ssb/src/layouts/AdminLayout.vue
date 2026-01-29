<template>
  <div class="admin-layout">
    <!-- Sidebar -->
    <aside class="sidebar" :class="{ 'sidebar--open': sidebarOpen }">
      <div class="sidebar__header">
        <div class="sidebar__logo">
          <span class="sidebar__logo-icon">⚽</span>
          <span class="sidebar__logo-text">SSB Admin</span>
        </div>
      </div>
      
      <nav class="sidebar__nav">
        <router-link to="/admin" class="nav-item" active-class="nav-item--active" :class="{ 'nav-item--active': $route.path === '/admin' }">
          <span class="nav-item__icon">📊</span>
          <span class="nav-item__text">Dashboard</span>
        </router-link>
        
        <router-link to="/admin/pending" class="nav-item" active-class="nav-item--active">
          <span class="nav-item__icon">⏳</span>
          <span class="nav-item__text">Pending</span>
          <span v-if="pendingCount > 0" class="nav-item__badge">{{ pendingCount }}</span>
        </router-link>
        
        <router-link to="/admin/players" class="nav-item" active-class="nav-item--active">
          <span class="nav-item__icon">👥</span>
          <span class="nav-item__text">Players</span>
        </router-link>
        
        <router-link to="/admin/coaches" class="nav-item" active-class="nav-item--active">
          <span class="nav-item__icon">🎯</span>
          <span class="nav-item__text">Coaches</span>
        </router-link>
        
        <!-- Groups Submenu -->
        <div class="nav-group">
          <button 
            @click="toggleGroups"
            class="nav-item nav-item--button"
            :class="{ 'nav-item--active': $route.path.startsWith('/admin/groups') }"
          >
            <span class="nav-item__icon">📂</span>
            <span class="nav-item__text">Groups</span>
            <svg class="nav-item__arrow" :class="{ 'nav-item__arrow--open': groupsExpanded }" viewBox="0 0 24 24">
              <path fill="currentColor" d="M7 10l5 5 5-5z"/>
            </svg>
          </button>
          
          <div v-show="groupsExpanded" class="nav-submenu">
            <router-link to="/admin/groups" class="nav-subitem" active-class="nav-subitem--active">
              All Groups
            </router-link>
            <router-link 
              v-for="group in groups" 
              :key="group.id"
              :to="`/admin/groups/${group.id}`"
              class="nav-subitem"
              active-class="nav-subitem--active"
            >
              {{ group.name }}
            </router-link>
          </div>
        </div>
        
        <!-- Schedules Submenu -->
        <div class="nav-group">
          <button 
            @click="toggleSchedules"
            class="nav-item nav-item--button"
            :class="{ 'nav-item--active': $route.path.startsWith('/admin/schedules') }"
          >
            <span class="nav-item__icon">📅</span>
            <span class="nav-item__text">Schedules</span>
            <svg class="nav-item__arrow" :class="{ 'nav-item__arrow--open': schedulesExpanded }" viewBox="0 0 24 24">
              <path fill="currentColor" d="M7 10l5 5 5-5z"/>
            </svg>
          </button>
          
          <div v-show="schedulesExpanded" class="nav-submenu">
            <router-link to="/admin/schedules" class="nav-subitem" active-class="nav-subitem--active">
              All Schedules
            </router-link>
            <router-link 
              v-for="group in groups" 
              :key="`schedule-${group.id}`"
              :to="`/admin/schedules/${group.id}`"
              class="nav-subitem"
              active-class="nav-subitem--active"
            >
              {{ group.name }}
            </router-link>
          </div>
        </div>
      </nav>
      
      <div class="sidebar__footer">
        <div class="sidebar__user">
          <div class="sidebar__user-avatar">
            {{ authStore.user?.username?.charAt(0)?.toUpperCase() || 'A' }}
          </div>
          <div class="sidebar__user-info">
            <span class="sidebar__user-name">{{ authStore.user?.username }}</span>
            <span class="sidebar__user-role">Administrator</span>
          </div>
        </div>
        <button @click="handleLogout" class="sidebar__logout">
          <svg class="sidebar__logout-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
          </svg>
          Logout
        </button>
      </div>
    </aside>

    <!-- Mobile Overlay -->
    <div v-if="sidebarOpen" class="mobile-overlay" @click="sidebarOpen = false"></div>

    <!-- Main Content -->
    <div class="main-wrapper">
      <!-- Top Bar -->
      <header class="topbar">
        <button class="topbar__menu" @click="sidebarOpen = !sidebarOpen">
          <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </button>
        <div class="topbar__breadcrumb">
          {{ currentPageTitle }}
        </div>
      </header>
      
      <!-- Main Content Area -->
      <main class="main-content">
        <slot />
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { groupsService, playersService } from '@/services'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()
const groups = ref([])
const groupsExpanded = ref(false)
const schedulesExpanded = ref(false)
const sidebarOpen = ref(false)
const pendingCount = ref(0)

const currentPageTitle = computed(() => {
  const titles = {
    '/admin': 'Dashboard',
    '/admin/pending': 'Pending Registrations',
    '/admin/players': 'Players Management',
    '/admin/coaches': 'Coaches Management',
    '/admin/groups': 'Groups Management',
    '/admin/schedules': 'Schedules Management'
  }
  return titles[route.path] || 'Admin Panel'
})

async function loadGroups() {
  try {
    const response = await groupsService.getGroups()
    groups.value = response.results || response || []
    
    if (route.path.startsWith('/admin/groups')) {
      groupsExpanded.value = true
    }
    
    if (route.path.startsWith('/admin/schedules')) {
      schedulesExpanded.value = true
    }
  } catch (error) {
    console.error('Failed to load groups:', error)
  }
}

async function loadPendingCount() {
  try {
    const pending = await playersService.getPending()
    pendingCount.value = pending.length || 0
  } catch (error) {
    console.error('Failed to load pending count:', error)
  }
}

function toggleGroups() {
  groupsExpanded.value = !groupsExpanded.value
}

function toggleSchedules() {
  schedulesExpanded.value = !schedulesExpanded.value
}

async function handleLogout() {
  await authStore.logout()
  router.push('/admin/login')
}

onMounted(() => {
  loadGroups()
  loadPendingCount()
})
</script>

<style scoped>
.admin-layout {
  display: flex;
  min-height: 100vh;
  background: #f1f5f9;
}

/* Sidebar */
.sidebar {
  width: 260px;
  height: 100vh;
  background: linear-gradient(180deg, #1e3a8a 0%, #1e40af 100%);
  display: flex;
  flex-direction: column;
  position: fixed;
  top: 0;
  left: 0;
  z-index: 100;
  transform: translateX(-100%);
  transition: transform 0.3s ease;
}

@media (min-width: 1024px) {
  .sidebar {
    position: sticky;
    top: 0;
    transform: translateX(0);
  }
}

.sidebar--open {
  transform: translateX(0);
}

.sidebar__header {
  padding: 1.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.sidebar__logo {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.sidebar__logo-icon {
  font-size: 1.75rem;
}

.sidebar__logo-text {
  font-size: 1.25rem;
  font-weight: 800;
  color: white;
}

.sidebar__nav {
  flex: 1;
  padding: 1rem 0.75rem;
  overflow-y: auto;
  min-height: 0;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  color: rgba(255, 255, 255, 0.8);
  text-decoration: none;
  border-radius: 0.5rem;
  transition: all 0.2s;
  margin-bottom: 0.25rem;
  font-size: 0.9rem;
}

.nav-item--button {
  width: 100%;
  background: none;
  border: none;
  cursor: pointer;
  text-align: left;
}

.nav-item:hover {
  background: rgba(255, 255, 255, 0.1);
  color: white;
}

.nav-item--active {
  background: rgba(255, 255, 255, 0.15);
  color: white;
  font-weight: 600;
}

.nav-item__icon {
  font-size: 1.125rem;
}

.nav-item__text {
  flex: 1;
}

.nav-item__badge {
  background: #f59e0b;
  color: white;
  font-size: 0.7rem;
  font-weight: 700;
  padding: 0.125rem 0.5rem;
  border-radius: 9999px;
}

.nav-item__arrow {
  width: 20px;
  height: 20px;
  transition: transform 0.2s;
}

.nav-item__arrow--open {
  transform: rotate(180deg);
}

.nav-group {
  margin-bottom: 0.25rem;
}

.nav-submenu {
  margin-left: 2rem;
  padding-left: 0.75rem;
  border-left: 1px solid rgba(255, 255, 255, 0.2);
}

.nav-subitem {
  display: block;
  padding: 0.5rem 1rem;
  color: rgba(255, 255, 255, 0.7);
  text-decoration: none;
  font-size: 0.85rem;
  border-radius: 0.375rem;
  transition: all 0.2s;
}

.nav-subitem:hover {
  color: white;
  background: rgba(255, 255, 255, 0.1);
}

.nav-subitem--active {
  color: white;
  background: rgba(255, 255, 255, 0.15);
}

.sidebar__footer {
  padding: 1rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.sidebar__user {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 0.75rem;
}

.sidebar__user-avatar {
  width: 40px;
  height: 40px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 700;
}

.sidebar__user-info {
  display: flex;
  flex-direction: column;
}

.sidebar__user-name {
  color: white;
  font-weight: 600;
  font-size: 0.9rem;
}

.sidebar__user-role {
  color: rgba(255, 255, 255, 0.6);
  font-size: 0.75rem;
}

.sidebar__logout {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.625rem;
  background: rgba(220, 38, 38, 0.2);
  border: 1px solid rgba(220, 38, 38, 0.3);
  border-radius: 0.5rem;
  color: #fca5a5;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.sidebar__logout:hover {
  background: #dc2626;
  color: white;
}

.sidebar__logout-icon {
  width: 18px;
  height: 18px;
}

/* Mobile Overlay */
.mobile-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 50;
}

@media (min-width: 1024px) {
  .mobile-overlay {
    display: none;
  }
}

/* Main Wrapper */
.main-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
}

/* Topbar */
.topbar {
  background: white;
  padding: 1rem 1.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 40;
}

.topbar__menu {
  display: flex;
  padding: 0.5rem;
  background: none;
  border: none;
  cursor: pointer;
  border-radius: 0.375rem;
}

.topbar__menu:hover {
  background: #f1f5f9;
}

.topbar__menu svg {
  width: 24px;
  height: 24px;
  color: #64748b;
}

@media (min-width: 1024px) {
  .topbar__menu {
    display: none;
  }
}

.topbar__breadcrumb {
  font-weight: 600;
  color: #1e293b;
}

/* Main Content */
.main-content {
  flex: 1;
  padding: 1.5rem;
}

@media (min-width: 768px) {
  .main-content {
    padding: 2rem;
  }
}
</style>
