import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes = [
  {
    path: '/',
    name: 'landing',
    component: () => import('@/views/LandingView.vue')
  },
  {
    path: '/register',
    name: 'register',
    component: () => import('@/views/user/RegisterView.vue')
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('@/views/user/LoginView.vue')
  },
  {
    path: '/admin/login',
    name: 'admin-login',
    component: () => import('@/views/admin/AdminLoginView.vue')
  },
  {
    path: '/admin',
    name: 'admin-dashboard',
    component: () => import('@/views/admin/DashboardView.vue'),
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/admin/pending',
    name: 'admin-pending',
    component: () => import('@/views/admin/PendingView.vue'),
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/admin/players',
    name: 'admin-players',
    component: () => import('@/views/admin/PlayersView.vue'),
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/admin/coaches',
    name: 'admin-coaches',
    component: () => import('@/views/admin/CoachesView.vue'),
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/admin/groups',
    name: 'admin-groups',
    component: () => import('@/views/admin/GroupsView.vue'),
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/admin/groups/:id',
    name: 'admin-group-detail',
    component: () => import('@/views/admin/GroupDetailView.vue'),
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/admin/schedules',
    name: 'admin-schedules',
    component: () => import('@/views/admin/SchedulesView.vue'),
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/admin/schedules/:id',
    name: 'admin-schedule-detail',
    component: () => import('@/views/admin/ScheduleDetailView.vue'),
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/admin/schedules/:id',
    name: 'admin-schedule-detail',
    component: () => import('@/views/admin/ScheduleDetailView.vue'),
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/profile',
    name: 'profile',
    component: () => import('@/views/user/ProfileView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/schedules',
    name: 'schedules',
    component: () => import('@/views/user/SchedulesView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/team',
    name: 'team',
    component: () => import('@/views/user/TeamView.vue'),
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation guard
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()

  // Admin routes - redirect to admin login if not authenticated
  if (to.path.startsWith('/admin') && to.name !== 'admin-login') {
    if (!authStore.isAuthenticated) {
      return next({ name: 'admin-login' })
    }
    if (!authStore.isAdmin) {
      return next({ name: 'landing' })
    }
  }

  // Redirect authenticated users away from login pages
  if (authStore.isAuthenticated) {
    // Admin trying to access admin login page
    if (to.name === 'admin-login' && authStore.isAdmin) {
      return next({ name: 'admin-dashboard' })
    }
    // User trying to access user login page
    if (to.name === 'login' && !authStore.isAdmin) {
      return next({ name: 'profile' })
    }
  }

  // Regular auth check
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    return next({ name: 'login' })
  }

  if (to.meta.requiresAdmin && !authStore.isAdmin) {
    return next({ name: 'landing' })
  }

  next()
})

// Update page title
router.afterEach((to) => {
  if (to.path.startsWith('/admin')) {
    document.title = 'SSB Admin'
  } else {
    document.title = 'SSB Academy'
  }
})

export default router
