import { defineStore } from 'pinia'
import { ref } from 'vue'
import { schedulesService } from '@/services/schedulesService'

export const useSchedulesStore = defineStore('schedules', () => {
  const schedules = ref([])
  const currentSchedule = ref(null)
  const loading = ref(false)
  const error = ref(null)
  const pagination = ref({
    count: 0,
    next: null,
    previous: null
  })

  async function fetchSchedules(params = {}) {
    loading.value = true
    error.value = null
    try {
      const data = await schedulesService.getSchedules(params)
      schedules.value = data.results
      pagination.value = {
        count: data.count,
        next: data.next,
        previous: data.previous
      }
    } catch (err) {
      error.value = err.response?.data?.detail || 'Failed to fetch schedules'
    } finally {
      loading.value = false
    }
  }

  async function fetchSchedule(id) {
    loading.value = true
    error.value = null
    try {
      currentSchedule.value = await schedulesService.getSchedule(id)
    } catch (err) {
      error.value = err.response?.data?.detail || 'Failed to fetch schedule'
    } finally {
      loading.value = false
    }
  }

  async function createSchedule(data) {
    loading.value = true
    error.value = null
    try {
      const newSchedule = await schedulesService.createSchedule(data)
      schedules.value.unshift(newSchedule)
      return newSchedule
    } catch (err) {
      error.value = err.response?.data || 'Failed to create schedule'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function updateSchedule(id, data) {
    loading.value = true
    error.value = null
    try {
      const updatedSchedule = await schedulesService.updateSchedule(id, data)
      const index = schedules.value.findIndex(s => s.id === id)
      if (index !== -1) {
        schedules.value[index] = updatedSchedule
      }
      return updatedSchedule
    } catch (err) {
      error.value = err.response?.data || 'Failed to update schedule'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function deleteSchedule(id) {
    loading.value = true
    error.value = null
    try {
      await schedulesService.deleteSchedule(id)
      schedules.value = schedules.value.filter(s => s.id !== id)
    } catch (err) {
      error.value = err.response?.data?.detail || 'Failed to delete schedule'
      throw err
    } finally {
      loading.value = false
    }
  }

  return {
    schedules,
    currentSchedule,
    loading,
    error,
    pagination,
    fetchSchedules,
    fetchSchedule,
    createSchedule,
    updateSchedule,
    deleteSchedule
  }
})
