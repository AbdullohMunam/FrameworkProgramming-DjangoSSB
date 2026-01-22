<template>
  <div class="flex items-center justify-center" :class="wrapperClasses">
    <div :class="spinnerClasses">
      <div class="spinner-border" role="status">
        <svg class="animate-spin" :class="sizeClasses" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
      </div>
    </div>
    <p v-if="text" class="ml-3 text-gray-600 dark:text-gray-400">{{ text }}</p>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  size: {
    type: String,
    default: 'md',
    validator: (value) => ['sm', 'md', 'lg'].includes(value)
  },
  text: String,
  fullScreen: Boolean
})

const wrapperClasses = computed(() => {
  return props.fullScreen ? 'min-h-screen' : 'py-8'
})

const sizeClasses = computed(() => {
  const sizes = {
    sm: 'h-6 w-6',
    md: 'h-10 w-10',
    lg: 'h-16 w-16'
  }
  return sizes[props.size]
})

const spinnerClasses = computed(() => {
  return 'text-blue-600'
})
</script>
