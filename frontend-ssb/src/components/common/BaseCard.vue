<template>
  <div :class="cardClasses">
    <slot></slot>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  hover: {
    type: Boolean,
    default: true
  },
  padding: {
    type: String,
    default: 'normal',
    validator: (value) => ['none', 'sm', 'normal', 'lg'].includes(value)
  }
})

const cardClasses = computed(() => {
  const base = 'bg-white dark:bg-slate-800 rounded-xl shadow-md transition-all duration-300'
  const hoverClass = props.hover ? 'hover:shadow-xl hover:-translate-y-1' : ''
  
  const paddings = {
    none: '',
    sm: 'p-4',
    normal: 'p-6',
    lg: 'p-8'
  }
  
  return `${base} ${hoverClass} ${paddings[props.padding]}`
})
</script>
