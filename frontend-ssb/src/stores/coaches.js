import { defineStore } from 'pinia'
import { ref } from 'vue'
import { coachesService } from '@/services/coachesService'

export const useCoachesStore = defineStore('coaches', () => {
  const coaches = ref([])
  const currentCoach = ref(null)
  const loading = ref(false)
  const error = ref(null)
  const pagination = ref({
    count: 0,
    next: null,
    previous: null
  })

  async function fetchCoaches(params = {}) {
    loading.value = true
    error.value = null
    try {
      const data = await coachesService.getCoaches(params)
      coaches.value = data.results
      pagination.value = {
        count: data.count,
        next: data.next,
        previous: data.previous
      }
    } catch (err) {
      error.value = err.response?.data?.detail || 'Failed to fetch coaches'
    } finally {
      loading.value = false
    }
  }

  async function fetchCoach(id) {
    loading.value = true
    error.value = null
    try {
      currentCoach.value = await coachesService.getCoach(id)
    } catch (err) {
      error.value = err.response?.data?.detail || 'Failed to fetch coach'
    } finally {
      loading.value = false
    }
  }

  async function createCoach(data) {
    loading.value = true
    error.value = null
    try {
      const newCoach = await coachesService.createCoach(data)
      coaches.value.unshift(newCoach)
      return newCoach
    } catch (err) {
      error.value = err.response?.data || 'Failed to create coach'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function updateCoach(id, data) {
    loading.value = true
    error.value = null
    try {
      const updatedCoach = await coachesService.updateCoach(id, data)
      const index = coaches.value.findIndex(c => c.id === id)
      if (index !== -1) {
        coaches.value[index] = updatedCoach
      }
      return updatedCoach
    } catch (err) {
      error.value = err.response?.data || 'Failed to update coach'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function deleteCoach(id) {
    loading.value = true
    error.value = null
    try {
      await coachesService.deleteCoach(id)
      coaches.value = coaches.value.filter(c => c.id !== id)
    } catch (err) {
      error.value = err.response?.data?.detail || 'Failed to delete coach'
      throw err
    } finally {
      loading.value = false
    }
  }

  return {
    coaches,
    currentCoach,
    loading,
    error,
    pagination,
    fetchCoaches,
    fetchCoach,
    createCoach,
    updateCoach,
    deleteCoach
  }
})
