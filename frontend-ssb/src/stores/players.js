import { defineStore } from 'pinia'
import { ref } from 'vue'
import { playersService } from '@/services/playersService'

export const usePlayersStore = defineStore('players', () => {
  const players = ref([])
  const currentPlayer = ref(null)
  const loading = ref(false)
  const error = ref(null)
  const pagination = ref({
    count: 0,
    next: null,
    previous: null
  })

  async function fetchPlayers(params = {}) {
    loading.value = true
    error.value = null
    try {
      const data = await playersService.getPlayers(params)
      players.value = data.results
      pagination.value = {
        count: data.count,
        next: data.next,
        previous: data.previous
      }
    } catch (err) {
      error.value = err.response?.data?.detail || 'Failed to fetch players'
    } finally {
      loading.value = false
    }
  }

  async function fetchPlayer(id) {
    loading.value = true
    error.value = null
    try {
      currentPlayer.value = await playersService.getPlayer(id)
    } catch (err) {
      error.value = err.response?.data?.detail || 'Failed to fetch player'
    } finally {
      loading.value = false
    }
  }

  async function createPlayer(data) {
    loading.value = true
    error.value = null
    try {
      const newPlayer = await playersService.createPlayer(data)
      players.value.unshift(newPlayer)
      return newPlayer
    } catch (err) {
      error.value = err.response?.data || 'Failed to create player'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function updatePlayer(id, data) {
    loading.value = true
    error.value = null
    try {
      const updatedPlayer = await playersService.updatePlayer(id, data)
      const index = players.value.findIndex(p => p.id === id)
      if (index !== -1) {
        players.value[index] = updatedPlayer
      }
      return updatedPlayer
    } catch (err) {
      error.value = err.response?.data || 'Failed to update player'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function deletePlayer(id) {
    loading.value = true
    error.value = null
    try {
      await playersService.deletePlayer(id)
      players.value = players.value.filter(p => p.id !== id)
    } catch (err) {
      error.value = err.response?.data?.detail || 'Failed to delete player'
      throw err
    } finally {
      loading.value = false
    }
  }

  return {
    players,
    currentPlayer,
    loading,
    error,
    pagination,
    fetchPlayers,
    fetchPlayer,
    createPlayer,
    updatePlayer,
    deletePlayer
  }
})
