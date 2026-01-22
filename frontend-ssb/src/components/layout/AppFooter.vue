<template>
  <footer class="bg-white dark:bg-slate-900 border-t border-gray-200 dark:border-gray-700 mt-auto">
    <div class="container mx-auto px-4 py-8">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
        <!-- About -->
        <div>
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">SSB Academy</h3>
          <p class="text-gray-600 dark:text-gray-400 text-sm">
            Modern soccer academy management system built with Vue 3 and Django.
          </p>
        </div>

        <!-- Quick Links -->
        <div>
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Quick Links</h3>
          <ul class="space-y-2 text-sm">
            <li>
              <router-link to="/" class="text-gray-600 dark:text-gray-400 hover:text-blue-600 dark:hover:text-blue-400 transition-colors">
                Home
              </router-link>
            </li>
            <li>
              <router-link to="/players" class="text-gray-600 dark:text-gray-400 hover:text-blue-600 dark:hover:text-blue-400 transition-colors">
                Players
              </router-link>
            </li>
            <li>
              <router-link to="/coaches" class="text-gray-600 dark:text-gray-400 hover:text-blue-600 dark:hover:text-blue-400 transition-colors">
                Coaches
              </router-link>
            </li>
            <li>
              <router-link to="/schedules" class="text-gray-600 dark:text-gray-400 hover:text-blue-600 dark:hover:text-blue-400 transition-colors">
                Schedules
              </router-link>
            </li>
          </ul>
        </div>

        <!-- Contact -->
        <div>
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Contact</h3>
          <p class="text-gray-600 dark:text-gray-400 text-sm">
            Framework Programming<br />
            Django SSB Project<br />
            2026
          </p>
        </div>
      </div>

      <div class="mt-8 pt-8 border-t border-gray-200 dark:border-gray-700">
        <p class="text-center text-sm text-gray-600 dark:text-gray-400">
          © {{ new Date().getFullYear() }} SSB Academy. All rights reserved.
        </p>
      </div>
    </div>
  </footer>
</template>
