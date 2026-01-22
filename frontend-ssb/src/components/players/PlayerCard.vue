<template>
  <BaseCard :hover="false">
    <div class="relative">
      <img
        :src="getImageUrl(player.photo)"
        :alt="player.name"
        class="w-full h-48 object-cover rounded-lg mb-4"
        @error="$event.target.src = '/default-avatar.png'"
      />
      <div class="absolute top-2 right-2">
        <span class="px-3 py-1 bg-blue-600 text-white text-xs font-semibold rounded-full">
          {{ player.position }}
        </span>
      </div>
    </div>
    
    <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-2">
      {{ player.name }}
    </h3>
    
    <div class="space-y-2 text-sm text-gray-600 dark:text-gray-400 mb-4">
      <div class="flex items-center">
        <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
        </svg>
        <span>{{ player.age }} years old</span>
      </div>
      <div class="flex items-center">
        <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
        </svg>
        <span>{{ player.group_name || 'No Group' }}</span>
      </div>
    </div>
    
    <div class="flex gap-2">
      <BaseButton size="sm" variant="outline" full-width @click="$emit('view', player.id)">
        View
      </BaseButton>
      <BaseButton size="sm" full-width @click="$emit('edit', player.id)">
        Edit
      </BaseButton>
      <BaseButton size="sm" variant="danger" @click="$emit('delete', player.id, player.name)">
        Delete
      </BaseButton>
    </div>
  </BaseCard>
</template>

<script setup>
import BaseCard from '../common/BaseCard.vue'
import BaseButton from '../common/BaseButton.vue'
import { getImageUrl } from '@/utils/helpers'

defineProps({
  player: {
    type: Object,
    required: true
  }
})

defineEmits(['view', 'edit', 'delete'])
</script>
