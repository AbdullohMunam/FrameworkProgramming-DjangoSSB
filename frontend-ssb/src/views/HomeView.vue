<template>
  <AppLayout>
    <!-- Hero Section -->
    <section class="text-center py-20">
      <div class="max-w-4xl mx-auto">
        <h1 class="text-5xl md:text-6xl font-bold text-gray-900 dark:text-white mb-6">
          Welcome to
          <span class="bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-purple-600">
            SSB Academy
          </span>
        </h1>
        <p class="text-xl text-gray-600 dark:text-gray-400 mb-8">
          Modern soccer academy management system with powerful features
        </p>
        <div class="flex justify-center gap-4">
          <router-link v-if="!authStore.isAuthenticated" to="/login">
            <BaseButton size="lg">Get Started</BaseButton>
          </router-link>
          <router-link v-else to="/players">
            <BaseButton size="lg">View Players</BaseButton>
          </router-link>
        </div>
      </div>
    </section>

    <!-- Features -->
    <section class="py-16">
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <BaseCard>
          <div class="text-center">
            <div class="w-16 h-16 bg-blue-100 dark:bg-blue-900/30 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg class="w-8 h-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
              </svg>
            </div>
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-2">Player Management</h3>
            <p class="text-gray-600 dark:text-gray-400">Manage player profiles, photos, and performance data</p>
          </div>
        </BaseCard>

        <BaseCard>
          <div class="text-center">
            <div class="w-16 h-16 bg-purple-100 dark:bg-purple-900/30 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg class="w-8 h-8 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
            </div>
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-2">Coach Profiles</h3>
            <p class="text-gray-600 dark:text-gray-400">Track coaching staff and their specializations</p>
          </div>
        </BaseCard>

        <BaseCard>
          <div class="text-center">
            <div class="w-16 h-16 bg-green-100 dark:bg-green-900/30 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg class="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
              </svg>
            </div>
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-2">Group Organization</h3>
            <p class="text-gray-600 dark:text-gray-400">Organize players into training groups</p>
          </div>
        </BaseCard>

        <BaseCard>
          <div class="text-center">
            <div class="w-16 h-16 bg-pink-100 dark:bg-pink-900/30 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg class="w-8 h-8 text-pink-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
            </div>
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-2">Schedule Management</h3>
            <p class="text-gray-600 dark:text-gray-400">Plan and manage training schedules</p>
          </div>
        </BaseCard>
      </div>
    </section>

    <!-- Stats Section -->
    <section v-if="authStore.isAuthenticated" class="py-16">
      <h2 class="text-3xl font-bold text-gray-900 dark:text-white text-center mb-12">
        Quick Overview
      </h2>
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
        <BaseCard>
          <div class="text-center">
            <p class="text-4xl font-bold text-blue-600 mb-2">{{ stats.players }}</p>
            <p class="text-gray-600 dark:text-gray-400">Total Players</p>
          </div>
        </BaseCard>
        <BaseCard>
          <div class="text-center">
            <p class="text-4xl font-bold text-purple-600 mb-2">{{ stats.coaches }}</p>
            <p class="text-gray-600 dark:text-gray-400">Coaches</p>
          </div>
        </BaseCard>
        <BaseCard>
          <div class="text-center">
            <p class="text-4xl font-bold text-green-600 mb-2">{{ stats.groups }}</p>
            <p class="text-gray-600 dark:text-gray-400">Groups</p>
          </div>
        </BaseCard>
        <BaseCard>
          <div class="text-center">
            <p class="text-4xl font-bold text-pink-600 mb-2">{{ stats.schedules }}</p>
            <p class="text-gray-600 dark:text-gray-400">Schedules</p>
          </div>
        </BaseCard>
      </div>
    </section>
  </AppLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { playersService } from '@/services/playersService'
import { coachesService } from '@/services/coachesService'
import { groupsService } from '@/services/groupsService'
import { schedulesService } from '@/services/schedulesService'
import AppLayout from '@/components/layout/AppLayout.vue'
import BaseCard from '@/components/common/BaseCard.vue'
import BaseButton from '@/components/common/BaseButton.vue'

const authStore = useAuthStore()

const stats = ref({
  players: 0,
  coaches: 0,
  groups: 0,
  schedules: 0
})

const loadStats = async () => {
  if (!authStore.isAuthenticated) return
  
  try {
    const [players, coaches, groups, schedules] = await Promise.all([
      playersService.getPlayers({ page_size: 1 }),
      coachesService.getCoaches({ page_size: 1 }),
      groupsService.getGroups({ page_size: 1 }),
      schedulesService.getSchedules({ page_size: 1 })
    ])
    
    stats.value = {
      players: players.count || 0,
      coaches: coaches.count || 0,
      groups: groups.count || 0,
      schedules: schedules.count || 0
    }
  } catch (err) {
    console.error('Failed to load stats:', err)
  }
}

onMounted(() => {
  loadStats()
})
</script>
