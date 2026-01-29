<template>
  <div class="register-page">
    <div class="register-page__bg"></div>
    
    <div class="register-card animate-fade-in-up">
      <router-link to="/" class="register-card__logo">
        <span class="register-card__logo-icon">⚽</span>
        <span class="register-card__logo-text">SSB Academy</span>
      </router-link>
      
      <h2 class="register-card__title">Daftar Member</h2>
      <p class="register-card__subtitle">Bergabung dengan SSB Academy Malang</p>
      
      <div v-if="success" class="register-card__success">
        <svg class="register-card__success-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        {{ successMessage }}
      </div>
      
      <div v-if="error" class="register-card__error">
        <svg class="register-card__error-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        {{ error }}
      </div>
      
      <form v-if="!success" @submit.prevent="handleRegister" class="register-form">
        <!-- Player Info -->
        <div class="register-form__section">
          <h3 class="register-form__section-title">
            <span class="register-form__section-icon">👤</span>
            Data Pemain
          </h3>
          
          <div class="register-form__grid">
            <div class="register-form__group">
              <label class="register-form__label">Nama Lengkap *</label>
              <input 
                v-model="form.name" 
                type="text" 
                required 
                class="register-form__input"
                placeholder="Nama lengkap pemain"
              />
            </div>
            
            <div class="register-form__group">
              <label class="register-form__label">Umur *</label>
              <input 
                v-model.number="form.age" 
                type="number" 
                required 
                min="5" 
                max="50" 
                class="register-form__input"
                placeholder="Umur"
              />
            </div>
          </div>
          
          <div class="register-form__group">
            <label class="register-form__label">Posisi *</label>
            <select v-model="form.position" required class="register-form__input register-form__select">
              <option value="">Pilih Posisi</option>
              <option value="Goalkeeper">🧤 Goalkeeper</option>
              <option value="Defender">🛡️ Defender</option>
              <option value="Midfielder">⚡ Midfielder</option>
              <option value="Forward">⚽ Forward</option>
            </select>
          </div>
          
          <div class="register-form__group">
            <label class="register-form__label">Foto (Opsional)</label>
            <input 
              @change="handleFileChange" 
              type="file" 
              accept="image/*" 
              class="register-form__file"
            />
            <p class="register-form__hint">Format: JPG, PNG. Max 2MB</p>
          </div>
        </div>
        
        <!-- Account Info -->
        <div class="register-form__section">
          <h3 class="register-form__section-title">
            <span class="register-form__section-icon">🔐</span>
            Akun Login
          </h3>
          
          <div class="register-form__grid">
            <div class="register-form__group">
              <label class="register-form__label">Username *</label>
              <input 
                v-model="form.username" 
                type="text" 
                required 
                class="register-form__input"
                placeholder="Username untuk login"
              />
            </div>
            
            <div class="register-form__group">
              <label class="register-form__label">Email *</label>
              <input 
                v-model="form.email" 
                type="email" 
                required 
                class="register-form__input"
                placeholder="Email aktif"
              />
            </div>
          </div>
          
          <div class="register-form__grid">
            <div class="register-form__group">
              <label class="register-form__label">Password *</label>
              <input 
                v-model="form.password" 
                type="password" 
                required 
                minlength="6" 
                class="register-form__input"
                placeholder="Min. 6 karakter"
              />
            </div>
            
            <div class="register-form__group">
              <label class="register-form__label">Konfirmasi Password *</label>
              <input 
                v-model="form.password_confirm" 
                type="password" 
                required 
                minlength="6" 
                class="register-form__input"
                placeholder="Ulangi password"
              />
            </div>
          </div>
        </div>
        
        <button type="submit" :disabled="loading" class="register-form__submit">
          <span v-if="loading" class="register-form__spinner"></span>
          {{ loading ? 'Mendaftar...' : 'Daftar Sekarang' }}
        </button>
      </form>
      
      <p class="register-card__footer">
        Sudah punya akun? 
        <router-link to="/login" class="register-card__link">Login</router-link>
      </p>
      
      <router-link to="/" class="register-card__back">
        ← Kembali ke Beranda
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { authService } from '@/services'

const form = ref({
  name: '',
  age: '',
  position: '',
  photo: null,
  username: '',
  email: '',
  password: '',
  password_confirm: ''
})

const loading = ref(false)
const error = ref('')
const success = ref(false)
const successMessage = ref('')

function handleFileChange(event) {
  const file = event.target.files[0]
  if (file) {
    if (file.size > 2 * 1024 * 1024) {
      error.value = 'Ukuran file maksimal 2MB'
      event.target.value = ''
      return
    }
    form.value.photo = file
  }
}

async function handleRegister() {
  error.value = ''
  
  if (form.value.password !== form.value.password_confirm) {
    error.value = 'Password tidak cocok'
    return
  }
  
  loading.value = true
  
  try {
    const formData = new FormData()
    formData.append('name', form.value.name)
    formData.append('age', form.value.age)
    formData.append('position', form.value.position)
    formData.append('username', form.value.username)
    formData.append('email', form.value.email)
    formData.append('password', form.value.password)
    formData.append('password_confirm', form.value.password_confirm)
    
    if (form.value.photo) {
      formData.append('photo', form.value.photo)
    }
    
    await authService.register(formData)
    success.value = true
    successMessage.value = 'Pendaftaran berhasil! Mohon tunggu persetujuan admin. Email notifikasi akan dikirim setelah disetujui.'
    form.value = { 
      name: '', age: '', position: '', photo: null,
      username: '', email: '', password: '', password_confirm: '' 
    }
  } catch (err) {
    const errorData = err.response?.data
    if (errorData) {
      error.value = errorData.detail || 
                    errorData.email?.[0] || 
                    errorData.username?.[0] || 
                    errorData.password?.[0] ||
                    errorData.age?.[0] ||
                    errorData.position?.[0] ||
                    errorData.name?.[0] ||
                    'Pendaftaran gagal. Periksa data Anda.'
    } else {
      error.value = 'Pendaftaran gagal. Periksa koneksi Anda.'
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.register-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem 1.5rem;
  position: relative;
  overflow: hidden;
}

.register-page__bg {
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, #1e40af 0%, #2563eb 50%, #1e40af 100%);
  background-size: 200% 200%;
  animation: gradientMove 8s ease infinite;
}

.register-page__bg::before {
  content: '';
  position: absolute;
  inset: 0;
  background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.05'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
}

@keyframes gradientMove {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

.register-card {
  position: relative;
  background: white;
  padding: 2rem;
  border-radius: 1.5rem;
  box-shadow: 0 25px 80px rgba(0, 0, 0, 0.3);
  max-width: 600px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
}

.register-card__logo {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  text-decoration: none;
  margin-bottom: 1rem;
}

.register-card__logo-icon {
  font-size: 1.75rem;
}

.register-card__logo-text {
  font-size: 1.25rem;
  font-weight: 800;
  background: linear-gradient(135deg, #1e40af, #2563eb);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.register-card__title {
  font-size: 1.5rem;
  font-weight: 800;
  color: #1f2937;
  text-align: center;
  margin-bottom: 0.25rem;
}

.register-card__subtitle {
  color: #6b7280;
  text-align: center;
  margin-bottom: 1.5rem;
  font-size: 0.9rem;
}

.register-card__success {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  background: #ecfdf5;
  border: 1px solid #a7f3d0;
  color: #059669;
  padding: 1rem;
  border-radius: 0.75rem;
  margin-bottom: 1.5rem;
  font-size: 0.9rem;
  line-height: 1.5;
}

.register-card__success-icon {
  width: 24px;
  height: 24px;
  flex-shrink: 0;
}

.register-card__error {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: #fef2f2;
  border: 1px solid #fecaca;
  color: #dc2626;
  padding: 0.75rem 1rem;
  border-radius: 0.75rem;
  margin-bottom: 1.5rem;
  font-size: 0.9rem;
}

.register-card__error-icon {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
}

.register-form__section {
  background: #f9fafb;
  border-radius: 1rem;
  padding: 1.25rem;
  margin-bottom: 1.25rem;
}

.register-form__section-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 1rem;
}

.register-form__section-icon {
  font-size: 1.25rem;
}

.register-form__grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
}

@media (min-width: 480px) {
  .register-form__grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

.register-form__group {
  margin-bottom: 1rem;
}

.register-form__group:last-child {
  margin-bottom: 0;
}

.register-form__label {
  display: block;
  font-weight: 600;
  color: #374151;
  margin-bottom: 0.375rem;
  font-size: 0.85rem;
}

.register-form__input {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 2px solid #e5e7eb;
  border-radius: 0.5rem;
  font-size: 0.95rem;
  transition: all 0.3s;
  background: white;
}

.register-form__input:focus {
  outline: none;
  border-color: #2563eb;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
}

.register-form__select {
  cursor: pointer;
  appearance: none;
  background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3e%3cpath stroke='%236b7280' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='M6 8l4 4 4-4'/%3e%3c/svg%3e");
  background-position: right 0.75rem center;
  background-repeat: no-repeat;
  background-size: 1.25rem;
  padding-right: 2.5rem;
}

.register-form__file {
  width: 100%;
  padding: 0.5rem;
  border: 2px dashed #e5e7eb;
  border-radius: 0.5rem;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.3s;
  background: white;
}

.register-form__file:hover {
  border-color: #2563eb;
}

.register-form__hint {
  font-size: 0.75rem;
  color: #6b7280;
  margin-top: 0.25rem;
}

.register-form__submit {
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
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.register-form__submit:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(30, 64, 175, 0.4);
}

.register-form__submit:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.register-form__spinner {
  width: 20px;
  height: 20px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.register-card__footer {
  text-align: center;
  margin-top: 1.5rem;
  color: #6b7280;
  font-size: 0.9rem;
}

.register-card__link {
  color: #2563eb;
  font-weight: 600;
  text-decoration: none;
}

.register-card__link:hover {
  text-decoration: underline;
}

.register-card__back {
  display: block;
  text-align: center;
  margin-top: 1rem;
  color: #6b7280;
  font-size: 0.875rem;
  text-decoration: none;
}

.register-card__back:hover {
  color: #2563eb;
}
</style>
