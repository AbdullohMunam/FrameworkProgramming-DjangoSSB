<template>
  <AppLayout>
    <div class="space-y-6">
      <!-- Header -->
      <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <h1 class="text-3xl font-bold text-gray-900 dark:text-white">Players</h1>
          <p class="text-gray-600 dark:text-gray-400 mt-1">Manage your soccer academy players</p>
        </div>
        <BaseButton @click="showAddModal = true">
          + Add Player
        </BaseButton>
      </div>

      <!-- Search and Filter -->
      <BaseCard :hover="false">
        <div class="flex flex-col md:flex-row gap-4">
          <div class="flex-1">
            <BaseSearchBar
              v-model="searchQuery"
              placeholder="Search players by name or position..."
            />
          </div>
          <div class="flex gap-2">
            <select
              v-model="sortOrder"
              class="px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-slate-800 text-gray-900 dark:text-gray-100"
            >
              <option value="name">Name (A-Z)</option>
              <option value="-name">Name (Z-A)</option>
              <option value="age">Age (Youngest)</option>
              <option value="-age">Age (Oldest)</option>
            </select>
          </div>
        </div>
      </BaseCard>

      <!-- Loading State -->
      <BaseSpinner v-if="playersStore.loading" text="Loading players..." />

      <!-- Players Grid -->
      <div v-else-if="playersStore.players.length > 0" class="space-y-6">
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          <PlayerCard
            v-for="player in playersStore.players"
            :key="player.id"
            :player="player"
            @view="viewPlayer"
            @edit="editPlayer"
            @delete="confirmDelete"
          />
        </div>

        <!-- Pagination -->
        <BasePagination
          v-if="totalPages > 1"
          :current-page="currentPage"
          :total-pages="totalPages"
          :per-page="perPage"
          :total="playersStore.pagination.count"
          :has-next="!!playersStore.pagination.next"
          :has-previous="!!playersStore.pagination.previous"
          @next="currentPage++"
          @previous="currentPage--"
          @goto="currentPage = $event"
        />
      </div>

      <!-- Empty State -->
      <div v-else class="text-center py-16">
        <svg class="w-24 h-24 mx-auto text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
        </svg>
        <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-2">No players found</h3>
        <p class="text-gray-600 dark:text-gray-400 mb-4">Get started by creating a new player</p>
        <BaseButton @click="showAddModal = true">Add First Player</BaseButton>
      </div>
    </div>

    <!-- Add/Edit Modal -->
    <BaseModal
      :is-open="showAddModal || showEditModal"
      :title="showEditModal ? 'Edit Player' : 'Add New Player'"
      size="lg"
      @close="closeModal"
    >
      <form @submit.prevent="handleSubmit" class="space-y-4">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <BaseInput
            id="name"
            v-model="form.name"
            label="Full Name"
            placeholder="Enter player name"
            required
          />
          <BaseInput
            id="age"
            v-model.number="form.age"
            type="number"
            label="Age"
            min="5"
            max="99"
            required
          />
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <BaseInput
            id="position"
            v-model="form.position"
            label="Position"
            placeholder="e.g., Striker, Midfielder, Defender"
            required
          />

          <div class="space-y-1">
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">
              Group
            </label>
            <select
              v-model="form.group"
              class="block w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-slate-700 text-gray-900 dark:text-gray-100 px-4 py-2"
            >
              <option :value="null">No Group</option>
              <option v-for="group in groups" :key="group.id" :value="group.id">{{ group.name }}</option>
            </select>
          </div>
        </div>

        <div class="space-y-1">
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">
            Photo
          </label>
          <input
            type="file"
            accept="image/*"
            @change="handleFileChange"
            class="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
          />
          <img v-if="photoPreview" :src="photoPreview" alt="Preview" class="mt-2 w-32 h-32 object-cover rounded-lg" />
        </div>

        <div class="flex justify-end gap-3 pt-4">
          <BaseButton type="button" variant="outline" @click="closeModal">
            Cancel
          </BaseButton>
          <BaseButton type="submit" :loading="submitting">
            {{ showEditModal ? 'Update' : 'Create' }}
          </BaseButton>
        </div>
      </form>
    </BaseModal>

    <!-- Delete Confirmation Modal -->
    <BaseModal
      :is-open="showDeleteModal"
      title="Delete Player"
      size="sm"
      show-actions
      confirm-text="Delete"
      confirm-variant="danger"
      :loading="deleting"
      @close="showDeleteModal = false"
      @confirm="handleDelete"
    >
      <p class="text-gray-600 dark:text-gray-400">
        Are you sure you want to delete <strong>{{ playerToDelete?.name }}</strong>? This action cannot be undone.
      </p>
    </BaseModal>

    <!-- View Detail Modal -->
    <BaseModal
      :is-open="showViewModal"
      title="Player Details"
      size="md"
      @close="showViewModal = false"
    >
      <div v-if="selectedPlayer" class="space-y-4">
        <img
          :src="getImageUrl(selectedPlayer.photo)"
          :alt="selectedPlayer.name"
          class="w-full h-64 object-cover rounded-lg"
        />
        <div class="space-y-2">
          <div>
            <label class="text-sm font-medium text-gray-500 dark:text-gray-400">Name</label>
            <p class="text-lg font-semibold text-gray-900 dark:text-white">{{ selectedPlayer.name }}</p>
          </div>
          <div>
            <label class="text-sm font-medium text-gray-500 dark:text-gray-400">Position</label>
            <p class="text-lg text-gray-900 dark:text-white">{{ selectedPlayer.position }}</p>
          </div>
          <div>
            <label class="text-sm font-medium text-gray-500 dark:text-gray-400">Age</label>
            <p class="text-lg text-gray-900 dark:text-white">{{ selectedPlayer.age }} years old</p>
          </div>
          <div>
            <label class="text-sm font-medium text-gray-500 dark:text-gray-400">Group</label>
            <p class="text-lg text-gray-900 dark:text-white">{{ selectedPlayer.group_name || 'No Group' }}</p>
          </div>
        </div>
      </div>
    </BaseModal>
  </AppLayout>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { usePlayersStore } from '@/stores/players'
import { groupsService } from '@/services/groupsService'
import { useToast } from 'vue-toastification'
import { getImageUrl, formatDate } from '@/utils/helpers'
import AppLayout from '@/components/layout/AppLayout.vue'
import BaseCard from '@/components/common/BaseCard.vue'
import BaseButton from '@/components/common/BaseButton.vue'
import BaseSearchBar from '@/components/common/BaseSearchBar.vue'
import BaseSpinner from '@/components/common/BaseSpinner.vue'
import BasePagination from '@/components/common/BasePagination.vue'
import BaseModal from '@/components/common/BaseModal.vue'
import BaseInput from '@/components/common/BaseInput.vue'
import PlayerCard from '@/components/players/PlayerCard.vue'

const playersStore = usePlayersStore()
const toast = useToast()

const searchQuery = ref('')
const sortOrder = ref('name')
const currentPage = ref(1)
const perPage = ref(10)

const showAddModal = ref(false)
const showEditModal = ref(false)
const showDeleteModal = ref(false)
const showViewModal = ref(false)

const submitting = ref(false)
const deleting = ref(false)

const form = ref({
  name: '',
  age: '',
  position: '',
  group: null,
  photo: null
})

const photoPreview = ref(null)
const groups = ref([])
const playerToDelete = ref(null)
const selectedPlayer = ref(null)
const editingPlayerId = ref(null)

const totalPages = computed(() => Math.ceil(playersStore.pagination.count / perPage.value))

// Watch for search/filter changes
watch([searchQuery, sortOrder, currentPage], () => {
  loadPlayers()
}, { deep: true })

const loadPlayers = async () => {
  const params = {
    page: currentPage.value,
    page_size: perPage.value,
    ordering: sortOrder.value
  }
  
  if (searchQuery.value) {
    params.search = searchQuery.value
  }
  
  await playersStore.fetchPlayers(params)
}

const loadGroups = async () => {
  try {
    const data = await groupsService.getGroups({ page_size: 100 })
    groups.value = data.results
  } catch (err) {
    console.error('Failed to load groups:', err)
  }
}

const handleFileChange = (event) => {
  const file = event.target.files[0]
  if (file) {
    form.value.photo = file
    const reader = new FileReader()
    reader.onload = (e) => {
      photoPreview.value = e.target.result
    }
    reader.readAsDataURL(file)
  }
}

const handleSubmit = async () => {
  submitting.value = true
  try {
    if (showEditModal.value) {
      await playersStore.updatePlayer(editingPlayerId.value, form.value)
      toast.success('Player updated successfully!')
    } else {
      await playersStore.createPlayer(form.value)
      toast.success('Player created successfully!')
    }
    closeModal()
    loadPlayers()
  } catch (err) {
    toast.error(err.response?.data?.detail || 'Operation failed')
  } finally {
    submitting.value = false
  }
}

const viewPlayer = async (id) => {
  await playersStore.fetchPlayer(id)
  selectedPlayer.value = playersStore.currentPlayer
  showViewModal.value = true
}

const editPlayer = async (id) => {
  await playersStore.fetchPlayer(id)
  const player = playersStore.currentPlayer
  editingPlayerId.value = id
  form.value = {
    name: player.name,
    age: player.age,
    position: player.position,
    group: player.group,
    photo: null
  }
  photoPreview.value = getImageUrl(player.photo)
  showEditModal.value = true
}

const confirmDelete = (id, name) => {
  playerToDelete.value = { id, name }
  showDeleteModal.value = true
}

const handleDelete = async () => {
  deleting.value = true
  try {
    await playersStore.deletePlayer(playerToDelete.value.id)
    toast.success('Player deleted successfully!')
    showDeleteModal.value = false
    loadPlayers()
  } catch (err) {
    toast.error('Failed to delete player')
  } finally {
    deleting.value = false
  }
}

const closeModal = () => {
  showAddModal.value = false
  showEditModal.value = false
  form.value = {
    name: '',
    age: '',
    position: '',
    group: null,
    photo: null
  }
  photoPreview.value = null
  editingPlayerId.value = null
}

onMounted(() => {
  loadPlayers()
  loadGroups()
})
</script>
