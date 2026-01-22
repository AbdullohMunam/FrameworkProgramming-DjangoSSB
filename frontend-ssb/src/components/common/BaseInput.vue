<template>
  <div class="space-y-1">
    <label
      v-if="label"
      :for="id"
      class="block text-sm font-medium text-gray-700 dark:text-gray-300"
    >
      {{ label }}
      <span v-if="required" class="text-red-500">*</span>
    </label>
    
    <input
      :id="id"
      :type="type"
      :value="modelValue"
      :placeholder="placeholder"
      :required="required"
      :disabled="disabled"
      :accept="accept"
      :class="inputClasses"
      @input="$emit('update:modelValue', $event.target.value)"
      @change="$emit('change', $event)"
    />
    
    <p v-if="error" class="text-sm text-red-600 dark:text-red-400">
      {{ error }}
    </p>
    
    <p v-else-if="hint" class="text-sm text-gray-500 dark:text-gray-400">
      {{ hint }}
    </p>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  id: String,
  type: {
    type: String,
    default: 'text'
  },
  modelValue: [String, Number],
  label: String,
  placeholder: String,
  required: Boolean,
  disabled: Boolean,
  error: String,
  hint: String,
  accept: String
})

defineEmits(['update:modelValue', 'change'])

const inputClasses = computed(() => {
  const base = 'block w-full rounded-lg border px-4 py-2 transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed'
  const normal = 'border-gray-300 dark:border-gray-600 bg-white dark:bg-slate-700 text-gray-900 dark:text-gray-100 focus:border-blue-500 focus:ring-blue-500'
  const errorClass = 'border-red-500 focus:border-red-500 focus:ring-red-500'
  
  return `${base} ${props.error ? errorClass : normal}`
})
</script>
