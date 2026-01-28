<template>
  <div class="flex h-screen bg-gray-100">
    <!-- Sidebar -->
    <aside class="w-64 bg-blue-800 text-white flex flex-col overflow-y-auto">
      <div class="p-4">
        <h1 class="text-2xl font-bold">SSB Admin</h1>
      </div>
      
      <nav class="flex-1 px-2 py-4 space-y-2">
        <router-link 
          to="/admin" 
          class="block px-4 py-2 rounded hover:bg-blue-700"
          active-class="bg-blue-700"
        >
          Dashboard
        </router-link>
        <router-link 
          to="/admin/pending" 
          class="block px-4 py-2 rounded hover:bg-blue-700"
          active-class="bg-blue-700"
        >
          Pending Registrations
        </router-link>
        <router-link 
          to="/admin/players" 
          class="block px-4 py-2 rounded hover:bg-blue-700"
          active-class="bg-blue-700"
        >
          Players
        </router-link>
        <router-link 
          to="/admin/coaches" 
          class="block px-4 py-2 rounded hover:bg-blue-700"
          active-class="bg-blue-700"
        >
          Coaches
        </router-link>
        
        <!-- Groups with Submenu -->
        <div>
          <button 
            @click="toggleGroups"
            class="w-full flex items-center justify-between px-4 py-2 rounded hover:bg-blue-700"
            :class="{ 'bg-blue-700': groupsExpanded || $route.path.startsWith('/admin/groups') }"
          >
            <span>Groups</span>
            <svg 
              class="w-4 h-4 transition-transform" 
              :class="{ 'rotate-180': groupsExpanded }"
              fill="none" 
              stroke="currentColor" 
              viewBox="0 0 24 24"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
            </svg>
          </button>
          
          <!-- Submenu -->
          <div v-show="groupsExpanded" class="ml-4 mt-1 space-y-1">
            <router-link 
              to="/admin/groups" 
              class="block px-4 py-2 text-sm rounded hover:bg-blue-700"
              active-class="bg-blue-700"
            >
              All Groups
            </router-link>
            <router-link 
              v-for="group in groups" 
              :key="group.id"
              :to="`/admin/groups/${group.id}`"
              class="block px-4 py-2 text-sm rounded hover:bg-blue-700"
              active-class="bg-blue-700"
            >
              {{ group.name }}
            </router-link>
          </div>
        </div>
        
        <!-- Schedules with Submenu -->
        <div>
          <button 
            @click="toggleSchedules"
            class="w-full flex items-center justify-between px-4 py-2 rounded hover:bg-blue-700"
            :class="{ 'bg-blue-700': schedulesExpanded || $route.path.startsWith('/admin/schedules') }"
          >
            <span>Schedules</span>
            <svg 
              class="w-4 h-4 transition-transform" 
              :class="{ 'rotate-180': schedulesExpanded }"
              fill="none" 
              stroke="currentColor" 
              viewBox="0 0 24 24"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
            </svg>
          </button>
          
          <!-- Submenu -->
          <div v-show="schedulesExpanded" class="ml-4 mt-1 space-y-1">
            <router-link 
              to="/admin/schedules" 
              class="block px-4 py-2 text-sm rounded hover:bg-blue-700"
              active-class="bg-blue-700"
            >
              All Schedules
            </router-link>
            <router-link 
              v-for="group in groups" 
              :key="`schedule-${group.id}`"
              :to="`/admin/schedules/${group.id}`"
              class="block px-4 py-2 text-sm rounded hover:bg-blue-700"
              active-class="bg-blue-700"
            >
              {{ group.name }}
            </router-link>
          </div>
        </div>
      </nav>
      
      <div class="p-4 border-t border-blue-700">
        <p class="text-sm mb-2">{{ authStore.user?.username }}</p>
        <button 
          @click="handleLogout"
          class="w-full bg-red-600 hover:bg-red-700 px-4 py-2 rounded"
        >
          Logout
        </button>
      </div>
    </aside>

    <!-- Main Content -->
    <main class="flex-1 overflow-y-auto">
      <div class="p-8">
        <slot />
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { groupsService } from '@/services'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()
const groups = ref([])
const groupsExpanded = ref(false)
const schedulesExpanded = ref(false)

async function loadGroups() {
  try {
    const response = await groupsService.getGroups()
    groups.value = response.results || response || []
    
    // Auto-expand if on groups page
    if (route.path.startsWith('/admin/groups')) {
      groupsExpanded.value = true
    }
    
    // Auto-expand if on schedules page
    if (route.path.startsWith('/admin/schedules')) {
      schedulesExpanded.value = true
    }
  } catch (error) {
    console.error('Failed to load groups:', error)
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

onMounted(loadGroups)
</script>
