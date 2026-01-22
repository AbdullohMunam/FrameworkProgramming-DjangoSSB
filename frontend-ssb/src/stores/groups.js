import { defineStore } from 'pinia'
import { ref } from 'vue'
import { groupsService } from '@/services/groupsService'

export const useGroupsStore = defineStore('groups', () => {
  const groups = ref([])
  const currentGroup = ref(null)
  const loading = ref(false)
  const error = ref(null)
  const pagination = ref({
    count: 0,
    next: null,
    previous: null
  })

  async function fetchGroups(params = {}) {
    loading.value = true
    error.value = null
    try {
      const data = await groupsService.getGroups(params)
      groups.value = data.results
      pagination.value = {
        count: data.count,
        next: data.next,
        previous: data.previous
      }
    } catch (err) {
      error.value = err.response?.data?.detail || 'Failed to fetch groups'
    } finally {
      loading.value = false
    }
  }

  async function fetchGroup(id) {
    loading.value = true
    error.value = null
    try {
      currentGroup.value = await groupsService.getGroup(id)
    } catch (err) {
      error.value = err.response?.data?.detail || 'Failed to fetch group'
    } finally {
      loading.value = false
    }
  }

  async function createGroup(data) {
    loading.value = true
    error.value = null
    try {
      const newGroup = await groupsService.createGroup(data)
      groups.value.unshift(newGroup)
      return newGroup
    } catch (err) {
      error.value = err.response?.data || 'Failed to create group'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function updateGroup(id, data) {
    loading.value = true
    error.value = null
    try {
      const updatedGroup = await groupsService.updateGroup(id, data)
      const index = groups.value.findIndex(g => g.id === id)
      if (index !== -1) {
        groups.value[index] = updatedGroup
      }
      return updatedGroup
    } catch (err) {
      error.value = err.response?.data || 'Failed to update group'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function deleteGroup(id) {
    loading.value = true
    error.value = null
    try {
      await groupsService.deleteGroup(id)
      groups.value = groups.value.filter(g => g.id !== id)
    } catch (err) {
      error.value = err.response?.data?.detail || 'Failed to delete group'
      throw err
    } finally {
      loading.value = false
    }
  }

  return {
    groups,
    currentGroup,
    loading,
    error,
    pagination,
    fetchGroups,
    fetchGroup,
    createGroup,
    updateGroup,
    deleteGroup
  }
})
