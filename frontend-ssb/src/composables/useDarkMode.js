import { ref, watch } from 'vue'

export function useDarkMode() {
  const isDark = ref(false)

  const initDarkMode = () => {
    try {
      const savedTheme = localStorage.getItem('theme')
      if (savedTheme) {
        isDark.value = savedTheme === 'dark'
      } else {
        isDark.value = window.matchMedia('(prefers-color-scheme: dark)').matches
      }
      updateTheme()
    } catch (error) {
      console.error('Dark mode init error:', error)
    }
  }

  const toggleDarkMode = () => {
    isDark.value = !isDark.value
    updateTheme()
  }

  const updateTheme = () => {
    try {
      if (isDark.value) {
        document.documentElement.classList.add('dark')
        localStorage.setItem('theme', 'dark')
      } else {
        document.documentElement.classList.remove('dark')
        localStorage.setItem('theme', 'light')
      }
    } catch (error) {
      console.error('Theme update error:', error)
    }
  }

  // Initialize on creation
  initDarkMode()

  return {
    isDark,
    toggleDarkMode
  }
}
