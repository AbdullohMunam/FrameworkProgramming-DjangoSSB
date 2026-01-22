<template>
  <div class="flex items-center justify-between">
    <div class="text-sm text-gray-700 dark:text-gray-300">
      Showing {{ startItem }} to {{ endItem }} of {{ total }} results
    </div>
    
    <div class="flex gap-2">
      <button
        :disabled="!hasPrevious"
        class="px-3 py-1 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-slate-800 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-slate-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        @click="$emit('previous')"
      >
        Previous
      </button>
      
      <div class="flex items-center gap-1">
        <button
          v-for="page in displayPages"
          :key="page"
          :class="pageButtonClasses(page)"
          @click="page !== '...' && $emit('goto', page)"
        >
          {{ page }}
        </button>
      </div>
      
      <button
        :disabled="!hasNext"
        class="px-3 py-1 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-slate-800 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-slate-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        @click="$emit('next')"
      >
        Next
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  currentPage: {
    type: Number,
    required: true
  },
  totalPages: {
    type: Number,
    required: true
  },
  perPage: {
    type: Number,
    default: 10
  },
  total: {
    type: Number,
    required: true
  },
  hasNext: Boolean,
  hasPrevious: Boolean
})

defineEmits(['next', 'previous', 'goto'])

const startItem = computed(() => {
  return (props.currentPage - 1) * props.perPage + 1
})

const endItem = computed(() => {
  return Math.min(props.currentPage * props.perPage, props.total)
})

const displayPages = computed(() => {
  const pages = []
  const total = props.totalPages
  const current = props.currentPage
  
  if (total <= 7) {
    for (let i = 1; i <= total; i++) {
      pages.push(i)
    }
  } else {
    if (current <= 3) {
      pages.push(1, 2, 3, 4, '...', total)
    } else if (current >= total - 2) {
      pages.push(1, '...', total - 3, total - 2, total - 1, total)
    } else {
      pages.push(1, '...', current - 1, current, current + 1, '...', total)
    }
  }
  
  return pages
})

const pageButtonClasses = (page) => {
  const base = 'px-3 py-1 rounded-lg border transition-colors'
  const active = 'border-blue-600 bg-blue-600 text-white'
  const inactive = 'border-gray-300 dark:border-gray-600 bg-white dark:bg-slate-800 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-slate-700'
  const dots = 'cursor-default'
  
  if (page === '...') return `${base} ${inactive} ${dots}`
  return `${base} ${page === props.currentPage ? active : inactive}`
}
</script>
