<template>
  <AppLayout>
    <div class="flex flex-col items-center justify-center min-h-[60vh]">
      <div class="text-center">
        <h1 class="text-9xl font-bold text-gray-200 dark:text-gray-700">404</h1>
        <h2 class="text-3xl font-semibold text-gray-900 dark:text-white mb-4">Page Not Found</h2>
        <p class="text-gray-600 dark:text-gray-400 mb-8">
          The page you're looking for doesn't exist or has been moved.
        </p>
        <router-link to="/">
          <BaseButton>Go Home</BaseButton>
        </router-link>
      </div>
    </div>
  </AppLayout>
</template>

<script setup>
import AppLayout from '@/components/layout/AppLayout.vue'
import BaseButton from '@/components/common/BaseButton.vue'
</script>
