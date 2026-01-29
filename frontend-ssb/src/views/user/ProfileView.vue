<template>
  <div class="profile-page">
    <UserNavbar @logout="handleLogout" />
    
    <div class="profile-page__container">
      <h2 class="profile-page__title">Profil Saya</h2>
      
      <div v-if="loading" class="profile-page__loading">
        <div class="profile-page__spinner"></div>
        <p>Memuat data...</p>
      </div>
      
      <div v-else-if="profile" class="profile-card">
        <!-- Avatar -->
        <div class="profile-card__avatar-section">
          <div class="profile-card__avatar">
            <img v-if="profile.photo" :src="profile.photo" class="profile-card__avatar-img" />
            <span v-else class="profile-card__avatar-placeholder">
              {{ profile.name ? profile.name.charAt(0).toUpperCase() : '?' }}
            </span>
          </div>
          <h3 class="profile-card__name">{{ profile.name || profile.username }}</h3>
          <span 
            class="profile-card__status"
            :class="{
              'profile-card__status--pending': profile.status === 'pending',
              'profile-card__status--approved': profile.status === 'approved',
              'profile-card__status--rejected': profile.status === 'rejected'
            }"
          >
            {{ profile.status === 'pending' ? '⏳ Menunggu Persetujuan' : 
               profile.status === 'approved' ? '✅ Aktif' : '❌ Ditolak' }}
          </span>
        </div>
        
        <!-- Info Grid -->
        <div class="profile-card__info">
          <div class="profile-info-item">
            <span class="profile-info-item__label">Username</span>
            <span class="profile-info-item__value">{{ profile.username }}</span>
          </div>
          <div class="profile-info-item">
            <span class="profile-info-item__label">Email</span>
            <span class="profile-info-item__value">{{ profile.email }}</span>
          </div>
          <div class="profile-info-item">
            <span class="profile-info-item__label">Umur</span>
            <span class="profile-info-item__value">{{ profile.age || '-' }} tahun</span>
          </div>
          <div class="profile-info-item">
            <span class="profile-info-item__label">Posisi</span>
            <span class="profile-info-item__value profile-info-item__value--position">
              {{ getPositionEmoji(profile.position) }} {{ profile.position || '-' }}
            </span>
          </div>
          <div class="profile-info-item profile-info-item--full">
            <span class="profile-info-item__label">Kelompok</span>
            <span class="profile-info-item__value">{{ profile.group_name || 'Belum ada kelompok' }}</span>
          </div>
        </div>
        
        <button @click="openEditModal" class="profile-card__edit-btn">
          ✏️ Edit Profil
        </button>
      </div>
    </div>
    
    <!-- Edit Modal -->
    <div v-if="showEditModal" class="modal-overlay" @click.self="closeEditModal">
      <div class="modal">
        <h2 class="modal__title">Edit Profil</h2>
        
        <div v-if="error" class="modal__error">{{ error }}</div>
        
        <form @submit.prevent="handleSave" class="modal__form">
          <div class="modal__group">
            <label class="modal__label">Nama Lengkap *</label>
            <input v-model="form.name" type="text" required class="modal__input" />
          </div>
          
          <div class="modal__group">
            <label class="modal__label">Umur *</label>
            <input v-model.number="form.age" type="number" required min="5" max="50" class="modal__input" />
          </div>
          
          <div class="modal__group">
            <label class="modal__label">Posisi *</label>
            <select v-model="form.position" required class="modal__input modal__select">
              <option value="">Pilih Posisi</option>
              <option value="Goalkeeper">🧤 Goalkeeper</option>
              <option value="Defender">🛡️ Defender</option>
              <option value="Midfielder">⚡ Midfielder</option>
              <option value="Forward">⚽ Forward</option>
            </select>
          </div>
          
          <div class="modal__group">
            <label class="modal__label">Foto (Opsional)</label>
            <input @change="handleFileChange" type="file" accept="image/*" class="modal__file" />
            <p v-if="profile.photo" class="modal__hint">Kosongkan jika tidak ingin mengubah foto</p>
          </div>
          
          <div class="modal__actions">
            <button type="submit" :disabled="saving" class="modal__btn modal__btn--primary">
              {{ saving ? 'Menyimpan...' : 'Simpan' }}
            </button>
            <button type="button" @click="closeEditModal" class="modal__btn modal__btn--secondary">
              Batal
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { playersService } from '@/services'
import UserNavbar from '@/components/UserNavbar.vue'

const router = useRouter()
const authStore = useAuthStore()
const profile = ref(null)
const loading = ref(true)
const showEditModal = ref(false)
const saving = ref(false)
const error = ref('')

const form = ref({
  name: '',
  age: '',
  position: '',
  photo: null
})

function getPositionEmoji(position) {
  const emojis = {
    'Goalkeeper': '🧤',
    'Defender': '🛡️',
    'Midfielder': '⚡',
    'Forward': '⚽'
  }
  return emojis[position] || ''
}

async function loadProfile() {
  try {
    profile.value = await playersService.getMyProfile()
  } catch (error) {
    console.error('Failed to load profile:', error)
  } finally {
    loading.value = false
  }
}

function openEditModal() {
  form.value = {
    name: profile.value.name || '',
    age: profile.value.age || '',
    position: profile.value.position || '',
    photo: null
  }
  error.value = ''
  showEditModal.value = true
}

function closeEditModal() {
  showEditModal.value = false
  form.value = { name: '', age: '', position: '', photo: null }
  error.value = ''
}

function handleFileChange(event) {
  const file = event.target.files[0]
  form.value.photo = file || null
}

async function handleSave() {
  error.value = ''
  saving.value = true
  
  try {
    await playersService.updateProfile(form.value)
    showEditModal.value = false
    await loadProfile()
  } catch (err) {
    const errorData = err.response?.data
    if (errorData) {
      error.value = errorData.detail || 
                    errorData.name?.[0] || 
                    errorData.age?.[0] || 
                    errorData.position?.[0] || 
                    'Gagal menyimpan profil. Periksa data Anda.'
    } else {
      error.value = 'Gagal menyimpan profil. Periksa koneksi Anda.'
    }
  } finally {
    saving.value = false
  }
}

async function handleLogout() {
  await authStore.logout()
  router.push('/login')
}

onMounted(loadProfile)
</script>

<style scoped>
.profile-page {
  min-height: 100vh;
  background: linear-gradient(180deg, #f0f9ff 0%, #f9fafb 100%);
}

.profile-page__container {
  max-width: 600px;
  margin: 0 auto;
  padding: 2rem 1.5rem;
}

.profile-page__title {
  font-size: 1.75rem;
  font-weight: 800;
  color: #1f2937;
  margin-bottom: 1.5rem;
}

.profile-page__loading {
  text-align: center;
  padding: 3rem;
  color: #6b7280;
}

.profile-page__spinner {
  width: 40px;
  height: 40px;
  border: 3px solid #e5e7eb;
  border-top-color: #2563eb;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.profile-card {
  background: white;
  border-radius: 1.5rem;
  padding: 2rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.profile-card__avatar-section {
  text-align: center;
  margin-bottom: 2rem;
}

.profile-card__avatar {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  margin: 0 auto 1rem;
  overflow: hidden;
  background: linear-gradient(135deg, #1e40af, #2563eb);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8px 25px rgba(30, 64, 175, 0.3);
}

.profile-card__avatar-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.profile-card__avatar-placeholder {
  font-size: 2.5rem;
  font-weight: 700;
  color: white;
}

.profile-card__name {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 0.5rem;
}

.profile-card__status {
  display: inline-block;
  padding: 0.375rem 1rem;
  border-radius: 9999px;
  font-size: 0.85rem;
  font-weight: 600;
}

.profile-card__status--pending {
  background: #fef3c7;
  color: #d97706;
}

.profile-card__status--approved {
  background: #d1fae5;
  color: #059669;
}

.profile-card__status--rejected {
  background: #fee2e2;
  color: #dc2626;
}

.profile-card__info {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
  margin-bottom: 2rem;
}

.profile-info-item {
  background: #f9fafb;
  padding: 1rem;
  border-radius: 0.75rem;
}

.profile-info-item--full {
  grid-column: span 2;
}

.profile-info-item__label {
  display: block;
  font-size: 0.75rem;
  color: #6b7280;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 0.25rem;
}

.profile-info-item__value {
  font-weight: 600;
  color: #1f2937;
}

.profile-info-item__value--position {
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.profile-card__edit-btn {
  width: 100%;
  padding: 1rem;
  background: linear-gradient(135deg, #1e40af, #2563eb);
  color: white;
  border: none;
  border-radius: 0.75rem;
  font-size: 1rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s;
}

.profile-card__edit-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(30, 64, 175, 0.4);
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
}

.modal {
  background: white;
  border-radius: 1.5rem;
  padding: 2rem;
  max-width: 450px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
}

.modal__title {
  font-size: 1.5rem;
  font-weight: 800;
  color: #1f2937;
  margin-bottom: 1.5rem;
}

.modal__error {
  background: #fef2f2;
  border: 1px solid #fecaca;
  color: #dc2626;
  padding: 0.75rem 1rem;
  border-radius: 0.5rem;
  margin-bottom: 1rem;
  font-size: 0.9rem;
}

.modal__group {
  margin-bottom: 1rem;
}

.modal__label {
  display: block;
  font-weight: 600;
  color: #374151;
  margin-bottom: 0.375rem;
  font-size: 0.9rem;
}

.modal__input {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 2px solid #e5e7eb;
  border-radius: 0.5rem;
  font-size: 1rem;
  transition: all 0.3s;
}

.modal__input:focus {
  outline: none;
  border-color: #2563eb;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
}

.modal__select {
  cursor: pointer;
}

.modal__file {
  width: 100%;
  padding: 0.5rem;
  border: 2px dashed #e5e7eb;
  border-radius: 0.5rem;
  font-size: 0.9rem;
  cursor: pointer;
}

.modal__hint {
  font-size: 0.75rem;
  color: #6b7280;
  margin-top: 0.25rem;
}

.modal__actions {
  display: flex;
  gap: 1rem;
  margin-top: 1.5rem;
}

.modal__btn {
  flex: 1;
  padding: 0.875rem;
  border-radius: 0.5rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  border: none;
}

.modal__btn--primary {
  background: linear-gradient(135deg, #1e40af, #2563eb);
  color: white;
}

.modal__btn--primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(30, 64, 175, 0.4);
}

.modal__btn--secondary {
  background: #e5e7eb;
  color: #374151;
}

.modal__btn--secondary:hover {
  background: #d1d5db;
}

.modal__btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}
</style>
