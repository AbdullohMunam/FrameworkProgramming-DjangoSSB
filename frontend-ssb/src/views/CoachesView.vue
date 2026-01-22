<template>
  <AppLayout>
    <div class="space-y-6">
      <div class="flex justify-between items-center">
        <h1 class="text-3xl font-bold text-gray-900 dark:text-white">Coaches</h1>
        <BaseButton @click="showModal = true">+ Add Coach</BaseButton>
      </div>
      
      <BaseSearchBar v-model="search" placeholder="Search coaches..." />
      
      <BaseSpinner v-if="store.loading" />
      
      <div v-else-if="store.coaches.length" class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <BaseCard v-for="coach in store.coaches" :key="coach.id">
          <img :src="getImageUrl(coach.photo)" class="w-full h-48 object-cover rounded-lg mb-4" />
          <h3 class="text-xl font-bold">{{ coach.name }}</h3>
          <p class="text-gray-600 dark:text-gray-400">{{ coach.specialization }}</p>
          <div class="flex gap-2 mt-4">
            <BaseButton size="sm" variant="primary" @click="editItem(coach)">Edit</BaseButton>
            <BaseButton size="sm" variant="danger" @click="deleteItem(coach.id)">Delete</BaseButton>
          </div>
        </BaseCard>
      </div>
      
      <div v-else class="text-center py-16">
        <p class="text-gray-600 dark:text-gray-400">No coaches found</p>
        <BaseButton @click="showModal = true" class="mt-4">Add First Coach</BaseButton>
      </div>

      <BaseModal :is-open="showModal" title="Coach Form" @close="showModal = false">
        <form @submit.prevent="handleSubmit" class="space-y-4">
          <BaseInput v-model="form.name" label="Name" required />
          <BaseInput v-model="form.specialization" label="Specialization" required />
          <input type="file" @change="form.photo = $event.target.files[0]" accept="image/*" class="w-full" />
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
import { useCoachesStore } from '@/stores/coaches'
import { useToast } from 'vue-toastification'
import { getImageUrl } from '@/utils/helpers'
import AppLayout from '@/components/layout/AppLayout.vue'
import BaseCard from '@/components/common/BaseCard.vue'
import BaseButton from '@/components/common/BaseButton.vue'
import BaseSearchBar from '@/components/common/BaseSearchBar.vue'
import BaseSpinner from '@/components/common/BaseSpinner.vue'
import BaseModal from '@/components/common/BaseModal.vue'
import BaseInput from '@/components/common/BaseInput.vue'

const store = useCoachesStore()
const toast = useToast()
const search = ref('')
const showModal = ref(false)
const form = ref({ name: '', specialization: '', photo: null })
const editId = ref(null)

watch(search, () => store.fetchCoaches({ search: search.value }))

const handleSubmit = async () => {
  try {
    if (editId.value) {
      await store.updateCoach(editId.value, form.value)
      toast.success('Coach updated!')
    } else {
      await store.createCoach(form.value)
      toast.success('Coach created!')
    }
    showModal.value = false
    form.value = { name: '', specialization: '', photo: null }
    editId.value = null
    store.fetchCoaches()
  } catch (err) {
    toast.error('Operation failed')
  }
}

const editItem = (coach) => {
  form.value = { name: coach.name, specialization: coach.specialization, photo: null }
  editId.value = coach.id
  showModal.value = true
}

const deleteItem = async (id) => {
  if (confirm('Delete this coach?')) {
    await store.deleteCoach(id)
    toast.success('Coach deleted!')
    store.fetchCoaches()
  }
}

onMounted(() => store.fetchCoaches())
</script>
