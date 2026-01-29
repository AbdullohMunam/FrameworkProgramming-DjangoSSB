<template>
  <footer id="contact" class="footer">
    <div class="footer__container">
      <!-- Brand -->
      <div class="footer__brand">
        <div class="footer__logo">
          <span class="footer__logo-icon">⚽</span>
          <span class="footer__logo-text">SSB Academy</span>
        </div>
        <p class="footer__tagline">
          Membentuk Generasi Juara dari Kota Malang
        </p>
      </div>

      <!-- Quick Links -->
      <div class="footer__section">
        <h4 class="footer__title">Menu</h4>
        <ul class="footer__links">
          <li><a href="#about">Tentang Kami</a></li>
          <li><a href="#achievements">Prestasi</a></li>
          <li><a href="#coaches">Pelatih</a></li>
          <li><router-link to="/register">Pendaftaran</router-link></li>
        </ul>
      </div>

      <!-- Contact -->
      <div class="footer__section">
        <h4 class="footer__title">Kontak</h4>
        <ul class="footer__contact">
          <li>
            <span class="footer__icon">📍</span>
            <span>Jl. Raya Stadion No. 123<br>Malang, Jawa Timur 65145</span>
          </li>
          <li>
            <span class="footer__icon">📞</span>
            <span>(0341) 123-4567</span>
          </li>
          <li>
            <span class="footer__icon">✉️</span>
            <span>info@ssbacademy.id</span>
          </li>
        </ul>
      </div>

      <!-- Social -->
      <div class="footer__section">
        <h4 class="footer__title">Ikuti Kami</h4>
        <div class="footer__social">
          <a href="#" class="footer__social-link" aria-label="Instagram">
            <svg viewBox="0 0 24 24" fill="currentColor" width="24" height="24">
              <path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zM12 0C8.741 0 8.333.014 7.053.072 2.695.272.273 2.69.073 7.052.014 8.333 0 8.741 0 12c0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98C8.333 23.986 8.741 24 12 24c3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98C15.668.014 15.259 0 12 0zm0 5.838a6.162 6.162 0 100 12.324 6.162 6.162 0 000-12.324zM12 16a4 4 0 110-8 4 4 0 010 8zm6.406-11.845a1.44 1.44 0 100 2.881 1.44 1.44 0 000-2.881z"/>
            </svg>
          </a>
          <a href="#" class="footer__social-link" aria-label="Facebook">
            <svg viewBox="0 0 24 24" fill="currentColor" width="24" height="24">
              <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/>
            </svg>
          </a>
          <a href="#" class="footer__social-link" aria-label="YouTube">
            <svg viewBox="0 0 24 24" fill="currentColor" width="24" height="24">
              <path d="M23.498 6.186a3.016 3.016 0 00-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 00.502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 002.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 002.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/>
            </svg>
          </a>
        </div>
      </div>
    </div>

    <!-- Copyright -->
    <div class="footer__bottom">
      <p>&copy; {{ currentYear }} SSB Academy Malang. All rights reserved.</p>
    </div>
  </footer>
</template>

<script setup>
import { computed } from 'vue'

const currentYear = computed(() => new Date().getFullYear())
</script>

<style scoped>
.footer {
  background: linear-gradient(135deg, #1f2937 0%, #111827 100%);
  color: white;
  padding-top: 4rem;
}

.footer__container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 1.5rem;
  display: grid;
  grid-template-columns: 1fr;
  gap: 2.5rem;
}

@media (min-width: 640px) {
  .footer__container {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1024px) {
  .footer__container {
    grid-template-columns: 2fr 1fr 1.5fr 1fr;
  }
}

.footer__brand {
  max-width: 300px;
}

.footer__logo {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.footer__logo-icon {
  font-size: 2rem;
}

.footer__logo-text {
  font-size: 1.5rem;
  font-weight: 800;
}

.footer__tagline {
  color: #9ca3af;
  line-height: 1.6;
}

.footer__title {
  font-size: 1rem;
  font-weight: 700;
  margin-bottom: 1.25rem;
  color: #60a5fa;
}

.footer__links {
  list-style: none;
  padding: 0;
  margin: 0;
}

.footer__links li {
  margin-bottom: 0.75rem;
}

.footer__links a {
  color: #9ca3af;
  text-decoration: none;
  transition: all 0.3s;
}

.footer__links a:hover {
  color: white;
  padding-left: 5px;
}

.footer__contact {
  list-style: none;
  padding: 0;
  margin: 0;
}

.footer__contact li {
  display: flex;
  gap: 0.75rem;
  margin-bottom: 1rem;
  color: #9ca3af;
  font-size: 0.9rem;
  line-height: 1.5;
}

.footer__icon {
  flex-shrink: 0;
}

.footer__social {
  display: flex;
  gap: 1rem;
}

.footer__social-link {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 44px;
  height: 44px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 50%;
  color: white;
  transition: all 0.3s;
}

.footer__social-link:hover {
  background: #f59e0b;
  transform: translateY(-3px);
}

.footer__bottom {
  margin-top: 3rem;
  padding: 1.5rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  text-align: center;
  color: #6b7280;
  font-size: 0.875rem;
}
</style>
