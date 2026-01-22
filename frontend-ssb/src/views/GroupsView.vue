<template>
  <AppLayout>
    <div class="space-y-6">
      <div class="flex justify-between items-center">
        <h1 class="text-3xl font-bold text-gray-900 dark:text-white">Groups</h1>
        <BaseButton @click="showModal = true">+ Add Group</BaseButton>
      </div>
      
      <BaseSearchBar v-model="search" placeholder="Search groups..." />
      
      <BaseSpinner v-if="store.loading" />
      
      <div v-else-if="store.groups.length" class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <BaseCard v-for="group in store.groups" :key="group.id">
          <h3 class="text-xl font-bold">{{ group.name }}</h3>
          <p class="text-gray-600 dark:text-gray-400">Coach: {{ group.coach_name || 'Not assigned' }}</p>
          <div class="flex gap-2 mt-4">
            <BaseButton size="sm" @click="editItem(group)">Edit</BaseButton>
            <BaseButton size="sm" variant="danger" @click="deleteItem(group.id)">Delete</BaseButton>
          </div>
        </BaseCard>
      </div>
      
      <div v-else class="text-center py-16">
        <p class="text-gray-600 dark:text-gray-400">No groups found</p>
        <BaseButton @click="showModal = true" class="mt-4">Add First Group</BaseButton>
      </div>

      <BaseModal :is-open="showModal" title="Group Form" @close="showModal = false">
        <form @submit.prevent="handleSubmit" class="space-y-4">
          <BaseInput v-model="form.name" label="Name" required />
          <div>
            <label class="block text-sm font-medium mb-2">Coach</label>
            <select v-model="form.coach" class="w-full px-4 py-2 rounded-lg border dark:bg-slate-800">
              <option :value="null">No Coach</option>
              <option v-for="coach in coaches" :key="coach.id" :value="coach.id">{{ coach.name }}</option>
            </select>
          </div>
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
import { useGroupsStore } from '@/stores/groups'
import { coachesService } from '@/services/coachesService'
import { useToast } from 'vue-toastification'
import AppLayout from '@/components/layout/AppLayout.vue'
import BaseCard from '@/components/common/BaseCard.vue'
import BaseButton from '@/components/common/BaseButton.vue'
import BaseSearchBar from '@/components/common/BaseSearchBar.vue'
import BaseSpinner from '@/components/common/BaseSpinner.vue'
import BaseModal from '@/components/common/BaseModal.vue'
import BaseInput from '@/components/common/BaseInput.vue'

const store = useGroupsStore()
const toast = useToast()
const search = ref('')
const showModal = ref(false)
const form = ref({ name: '', coach: null })
const editId = ref(null)
const coaches = ref([])

watch(search, () => store.fetchGroups({ search: search.value }))

const loadCoaches = async () => {
  const data = await coachesService.getCoaches({ page_size: 100 })
  coaches.value = data.results
}

const handleSubmit = async () => {
  try {
    if (editId.value) {
      await store.updateGroup(editId.value, form.value)
      toast.success('Group updated!')
    } else {
      await store.createGroup(form.value)
      toast.success('Group created!')
    }
    showModal.value = false
    form.value = { name: '', coach: null }
    editId.value = null
    store.fetchGroups()
  } catch (err) {
    toast.error('Operation failed')
  }
}

const editItem = (group) => {
  form.value = { name: group.name, coach: group.coach }
  editId.value = group.id
  showModal.value = true
}

const deleteItem = async (id) => {
  if (confirm('Delete this group?')) {
    await store.deleteGroup(id)
    toast.success('Group deleted!')
    store.fetchGroups()
  }
}

onMounted(() => {
  store.fetchGroups()
  loadCoaches()
})
</script>
