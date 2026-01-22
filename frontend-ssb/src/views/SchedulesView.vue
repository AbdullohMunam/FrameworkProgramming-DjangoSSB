<template>
  <AppLayout>
    <div class="space-y-6">
      <div class="flex justify-between items-center">
        <h1 class="text-3xl font-bold text-gray-900 dark:text-white">Schedules</h1>
        <BaseButton @click="showModal = true">+ Add Schedule</BaseButton>
      </div>
      
      <BaseSearchBar v-model="search" placeholder="Search schedules..." />
      
      <BaseSpinner v-if="store.loading" />
      
      <div v-else-if="store.schedules.length" class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <BaseCard v-for="schedule in store.schedules" :key="schedule.id">
          <div class="flex justify-between items-start mb-3">
            <h3 class="text-xl font-bold">{{ schedule.group_name }}</h3>
            <span class="px-3 py-1 bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 rounded-full text-sm">
              {{ formatDate(schedule.date) }}
            </span>
          </div>
          <div class="space-y-2 text-gray-600 dark:text-gray-400">
            <p>⏰ {{ formatTime(schedule.time) }}</p>
          </div>
          <div class="flex gap-2 mt-4">
            <BaseButton size="sm" @click="editItem(schedule)">Edit</BaseButton>
            <BaseButton size="sm" variant="danger" @click="deleteItem(schedule.id)">Delete</BaseButton>
          </div>
        </BaseCard>
      </div>
      
      <div v-else class="text-center py-16">
        <p class="text-gray-600 dark:text-gray-400">No schedules found</p>
        <BaseButton @click="showModal = true" class="mt-4">Add First Schedule</BaseButton>
      </div>

      <BaseModal :is-open="showModal" title="Schedule Form" size="lg" @close="showModal = false">
        <form @submit.prevent="handleSubmit" class="space-y-4">
          <div>
            <label class="block text-sm font-medium mb-2">Group</label>
            <select v-model="form.group" required class="w-full px-4 py-2 rounded-lg border dark:bg-slate-800">
              <option value="">Select group</option>
              <option v-for="group in groups" :key="group.id" :value="group.id">{{ group.name }}</option>
            </select>
          </div>
          <BaseInput v-model="form.date" label="Date" type="date" required />
          <BaseInput v-model="form.time" label="Time" type="time" required />
          <div class="flex gap-2">
            <BaseButton type="button" variant="outline" @click="showModal = false">Cancel</BaseButton>
            <BaseButton type="submit">Save</BaseButton>
          </div>
        </form>
      </BaseModal>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useSchedulesStore } from '@/stores/schedules'
import { groupsService } from '@/services/groupsService'
import { useToast } from 'vue-toastification'
import { formatTime, formatDate } from '@/utils/helpers'
import AppLayout from '@/components/layout/AppLayout.vue'
import BaseCard from '@/components/common/BaseCard.vue'
import BaseButton from '@/components/common/BaseButton.vue'
import BaseSearchBar from '@/components/common/BaseSearchBar.vue'
import BaseSpinner from '@/components/common/BaseSpinner.vue'
import BaseModal from '@/components/common/BaseModal.vue'
import BaseInput from '@/components/common/BaseInput.vue'

const store = useSchedulesStore()
const toast = useToast()
const search = ref('')
const showModal = ref(false)
const form = ref({ group: '', date: '', time: '' })
const editId = ref(null)
const groups = ref([])

watch(search, () => store.fetchSchedules({ search: search.value }))

const loadGroups = async () => {
  const data = await groupsService.getGroups({ page_size: 100 })
  groups.value = data.results
}

const handleSubmit = async () => {
  try {
    if (editId.value) {
      await store.updateSchedule(editId.value, form.value)
      toast.success('Schedule updated!')
    } else {
      await store.createSchedule(form.value)
      toast.success('Schedule created!')
    }
    showModal.value = false
    form.value = { group: '', date: '', time: '' }
    editId.value = null
    store.fetchSchedules()
  } catch (err) {
    toast.error('Operation failed')
  }
}

const editItem = (schedule) => {
  form.value = {
    group: schedule.group,
    date: schedule.date,
    time: schedule.time
  }
  editId.value = schedule.id
  showModal.value = true
}

const deleteItem = async (id) => {
  if (confirm('Delete this schedule?')) {
    await store.deleteSchedule(id)
    toast.success('Schedule deleted!')
    store.fetchSchedules()
  }
}

onMounted(() => {
  store.fetchSchedules()
  loadGroups()
})
</script>
