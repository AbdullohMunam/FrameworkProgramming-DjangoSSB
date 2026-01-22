<template>
  <TransitionRoot :show="isOpen" as="template">
    <Dialog as="div" class="relative z-50" @close="close">
      <TransitionChild
        as="template"
        enter="duration-300 ease-out"
        enter-from="opacity-0"
        enter-to="opacity-100"
        leave="duration-200 ease-in"
        leave-from="opacity-100"
        leave-to="opacity-0"
      >
        <div class="fixed inset-0 bg-black/50 backdrop-blur-sm" />
      </TransitionChild>

      <div class="fixed inset-0 overflow-y-auto">
        <div class="flex min-h-full items-center justify-center p-4">
          <TransitionChild
            as="template"
            enter="duration-300 ease-out"
            enter-from="opacity-0 scale-95"
            enter-to="opacity-100 scale-100"
            leave="duration-200 ease-in"
            leave-from="opacity-100 scale-100"
            leave-to="opacity-0 scale-95"
          >
            <DialogPanel :class="panelClasses">
              <DialogTitle
                v-if="title"
                as="h3"
                class="text-lg font-semibold leading-6 text-gray-900 dark:text-white mb-4"
              >
                {{ title }}
              </DialogTitle>
              
              <div class="mt-2">
                <slot></slot>
              </div>
              
              <div v-if="showActions" class="mt-6 flex justify-end gap-3">
                <BaseButton variant="outline" @click="close">
                  {{ cancelText }}
                </BaseButton>
                <BaseButton
                  :variant="confirmVariant"
                  :loading="loading"
                  @click="$emit('confirm')"
                >
                  {{ confirmText }}
                </BaseButton>
              </div>
            </DialogPanel>
          </TransitionChild>
        </div>
      </div>
    </Dialog>
  </TransitionRoot>
</template>

<script setup>
import { computed } from 'vue'
import {
  Dialog,
  DialogPanel,
  DialogTitle,
  TransitionRoot,
  TransitionChild,
} from '@headlessui/vue'
import BaseButton from './BaseButton.vue'

const props = defineProps({
  isOpen: Boolean,
  title: String,
  size: {
    type: String,
    default: 'md',
    validator: (value) => ['sm', 'md', 'lg', 'xl'].includes(value)
  },
  showActions: {
    type: Boolean,
    default: false
  },
  confirmText: {
    type: String,
    default: 'Confirm'
  },
  cancelText: {
    type: String,
    default: 'Cancel'
  },
  confirmVariant: {
    type: String,
    default: 'primary'
  },
  loading: Boolean
})

const emit = defineEmits(['close', 'confirm'])

const close = () => emit('close')

const panelClasses = computed(() => {
  const base = 'w-full transform overflow-hidden rounded-2xl bg-white dark:bg-slate-800 p-6 text-left align-middle shadow-xl transition-all'
  
  const sizes = {
    sm: 'max-w-md',
    md: 'max-w-lg',
    lg: 'max-w-2xl',
    xl: 'max-w-4xl'
  }
  
  return `${base} ${sizes[props.size]}`
})
</script>
