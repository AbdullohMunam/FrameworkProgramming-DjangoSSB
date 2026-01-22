# SSB Academy - Modern Frontend with Vue 3

## 🎉 Frontend Modern Telah Berhasil Dibuat!

Frontend baru dengan Vue 3 + Vite telah selesai dibangun dengan fitur-fitur modern dan UX yang optimal.

## 🚀 Quick Start

### 1. Install Dependencies (Sudah Selesai)
```bash
cd frontend-ssb
npm install
```

### 2. Start Development Server
```bash
npm run dev
```
Aplikasi akan berjalan di: **http://localhost:5173**

### 3. Start Django Backend
Di terminal terpisah:
```bash
cd ssb
python manage.py runserver
```
Backend akan berjalan di: **http://localhost:8000**

## 📁 Struktur Project

```
frontend-ssb/
├── src/
│   ├── assets/styles/        # Global CSS dengan Tailwind
│   ├── components/
│   │   ├── common/          # Reusable components (7 files)
│   │   ├── layout/          # Layout components (3 files)
│   │   └── players/         # Player-specific components
│   ├── composables/         # Vue composables (2 files)
│   ├── router/              # Vue Router configuration
│   ├── services/            # API services (6 files)
│   ├── stores/              # Pinia stores (5 files)
│   ├── utils/               # Helper functions
│   ├── views/               # Page components (7 files)
│   ├── App.vue              # Root component
│   └── main.js              # Entry point
├── package.json
├── vite.config.js
├── tailwind.config.js
└── postcss.config.js
```

## ✨ Fitur-Fitur Modern

### 🎨 UI/UX Features
- ✅ **Dark Mode** - Toggle dengan persistent storage
- ✅ **Responsive Design** - Mobile, tablet, desktop optimized
- ✅ **Modern Cards** - Glassmorphism effects
- ✅ **Smooth Animations** - Transitions yang halus
- ✅ **Toast Notifications** - Feedback untuk setiap action
- ✅ **Modal Dialogs** - Accessible dengan Headless UI
- ✅ **Loading States** - Spinner dan skeleton loaders
- ✅ **Empty States** - Friendly messages untuk data kosong

### 🔧 Functional Features
- ✅ **Authentication** - Token-based dengan auto-redirect
- ✅ **CRUD Operations** - Create, Read, Update, Delete untuk semua entity
- ✅ **Search & Filter** - Real-time search dengan debouncing
- ✅ **Pagination** - Smooth pagination controls
- ✅ **Image Upload** - Dengan preview sebelum upload
- ✅ **Form Validation** - Real-time validation
- ✅ **Delete Confirmation** - Modal konfirmasi untuk destructive actions
- ✅ **Error Handling** - User-friendly error messages

### 🛠️ Technical Stack
- **Vue 3** - Composition API
- **Vite** - Lightning fast HMR
- **Pinia** - State management
- **Vue Router** - Navigation dengan guards
- **Axios** - HTTP client dengan interceptors
- **Tailwind CSS** - Utility-first CSS
- **Headless UI** - Accessible components
- **Vue Toastification** - Toast notifications

## 📱 Pages & Routes

| Route | Component | Description | Auth Required |
|-------|-----------|-------------|---------------|
| `/` | HomeView | Homepage dengan features | ❌ |
| `/login` | LoginView | Login form | ❌ |
| `/players` | PlayersView | Players CRUD | ✅ |
| `/coaches` | CoachesView | Coaches CRUD | ✅ |
| `/groups` | GroupsView | Groups CRUD | ✅ |
| `/schedules` | SchedulesView | Schedules CRUD | ✅ |
| `*` | NotFoundView | 404 page | ❌ |

## 🎯 Component Architecture

### Base Components (Reusable)
1. **BaseButton** - Button dengan variants (primary, secondary, danger, success, outline)
2. **BaseCard** - Card container dengan hover effects
3. **BaseInput** - Form input dengan label dan error handling
4. **BaseModal** - Modal dialog dengan backdrop
5. **BasePagination** - Pagination controls
6. **BaseSearchBar** - Search input dengan clear button
7. **BaseSpinner** - Loading spinner dengan sizes

### Layout Components
1. **AppHeader** - Navbar dengan dark mode toggle dan auth status
2. **AppFooter** - Footer dengan links
3. **AppLayout** - Main layout wrapper

## 🔐 Authentication Flow

1. User mengakses halaman yang memerlukan auth
2. Jika tidak authenticated → redirect ke `/login`
3. User login dengan username & password
4. Token disimpan di localStorage
5. Axios interceptor menambahkan token ke setiap request
6. Token expired → auto logout dan redirect ke login

## 🎨 Dark Mode Implementation

Dark mode menggunakan Tailwind CSS class strategy:
- Toggle button di AppHeader
- State disimpan di localStorage
- Class `dark` ditambahkan ke `<html>` element
- Semua component menggunakan `dark:` variants

## 📊 State Management dengan Pinia

### Auth Store
- `isAuthenticated` - computed dari token
- `login(username, password)` - Login action
- `logout()` - Logout action
- `checkAuth()` - Verify token validity

### Entity Stores (Players, Coaches, Groups, Schedules)
- `fetch{Entity}()` - Load list dengan params
- `fetch{Entity}(id)` - Load single item
- `create{Entity}(data)` - Create new item
- `update{Entity}(id, data)` - Update item
- `delete{Entity}(id)` - Delete item

## 🔌 API Integration

### Base Configuration
```javascript
// src/services/api.js
- Base URL: /api
- Proxy to Django: http://localhost:8000
- Auto token injection via interceptor
- Auto logout on 401 responses
```

### Service Pattern
Setiap entity memiliki dedicated service file:
- `authService.js` - Login, logout, profile
- `playersService.js` - Players CRUD
- `coachesService.js` - Coaches CRUD
- `groupsService.js` - Groups CRUD
- `schedulesService.js` - Schedules CRUD

## 🎭 Composables

### useDarkMode
```javascript
const { isDark, toggleDarkMode } = useDarkMode()
```

### useDebounce
```javascript
const debouncedSearch = useDebounce(searchQuery, 500)
```

## 🚦 Development Workflow

1. **Start Backend**
   ```bash
   cd ssb
   python manage.py runserver
   ```

2. **Start Frontend** (Terminal baru)
   ```bash
   cd frontend-ssb
   npm run dev
   ```

3. **Access Application**
   - Frontend: http://localhost:5173
   - Backend: http://localhost:8000
   - Swagger API: http://localhost:8000/swagger/

4. **Login Credentials**
   - Username: `admin`
   - Password: `admin`

## 🏗️ Build for Production

```bash
cd frontend-ssb
npm run build
```

Output akan ada di folder `dist/` yang siap di-deploy.

## 🎨 Tailwind Configuration

### Dark Mode
```javascript
darkMode: 'class'
```

### Custom Colors
- Primary: Blue gradient (#3B82F6 to #2563EB)
- Extended with dark variants

### Custom Classes
- `.gradient-bg` - Gradient background
- `.glass-effect` - Glassmorphism effect
- `.card-hover` - Card hover animation

## 📝 Code Examples

### Creating a New Page

```vue
<template>
  <AppLayout>
    <h1>My New Page</h1>
  </AppLayout>
</template>

<script setup>
import AppLayout from '@/components/layout/AppLayout.vue'
</script>
```

### Using Base Components

```vue
<template>
  <BaseCard>
    <BaseInput v-model="name" label="Name" />
    <BaseButton @click="handleSubmit">Submit</BaseButton>
  </BaseCard>
</template>

<script setup>
import { ref } from 'vue'
import BaseCard from '@/components/common/BaseCard.vue'
import BaseInput from '@/components/common/BaseInput.vue'
import BaseButton from '@/components/common/BaseButton.vue'

const name = ref('')
const handleSubmit = () => {
  console.log('Name:', name.value)
}
</script>
```

### Using Store

```vue
<script setup>
import { onMounted } from 'vue'
import { usePlayersStore } from '@/stores/players'

const playersStore = usePlayersStore()

onMounted(async () => {
  await playersStore.fetchPlayers()
})
</script>
```

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Kill process on port 5173
lsof -ti:5173 | xargs kill -9
```

### CORS Issues
Pastikan Django backend running dan CORS settings sudah benar di `settings.py`:
```python
CORS_ALLOW_ALL_ORIGINS = True
```

### API 401 Unauthorized
1. Pastikan sudah login
2. Check token di localStorage
3. Pastikan backend authentication settings benar

## 🎯 Next Steps / Future Enhancements

1. **Add Unit Tests** - Vitest + Vue Test Utils
2. **Add E2E Tests** - Cypress or Playwright
3. **Image Optimization** - Lazy loading, compression
4. **PWA Support** - Service workers, offline mode
5. **Internationalization** - vue-i18n untuk multi-language
6. **Performance Monitoring** - Analytics integration
7. **Better Error Boundaries** - Global error handling
8. **Accessibility Audit** - WCAG compliance
9. **SEO Optimization** - Meta tags, SSR consideration
10. **CI/CD Pipeline** - Automated testing dan deployment

## 📚 Learning Resources

- [Vue 3 Documentation](https://vuejs.org/)
- [Vite Guide](https://vitejs.dev/)
- [Pinia Documentation](https://pinia.vuejs.org/)
- [Tailwind CSS](https://tailwindcss.com/)
- [Headless UI](https://headlessui.com/)

## 🤝 Comparison dengan Frontend Lama

| Feature | Old (Vanilla JS) | New (Vue 3) |
|---------|------------------|-------------|
| Framework | ❌ None | ✅ Vue 3 |
| Build Tool | ❌ None | ✅ Vite |
| State Management | ❌ localStorage only | ✅ Pinia |
| Routing | ❌ Manual | ✅ Vue Router |
| Components | ❌ No reusability | ✅ Component-based |
| Dark Mode | ❌ Not available | ✅ Full support |
| Type Safety | ❌ No | ⚠️ JS (could add TS) |
| Hot Reload | ❌ Manual refresh | ✅ HMR |
| Code Organization | ❌ Mixed | ✅ Structured |
| Dev Experience | ⚠️ Basic | ✅ Excellent |

## ✅ Completion Status

Semua fitur telah berhasil diimplementasikan:
- ✅ Project setup & configuration
- ✅ All base components
- ✅ Layout components
- ✅ Authentication system
- ✅ Players CRUD
- ✅ Coaches CRUD
- ✅ Groups CRUD
- ✅ Schedules CRUD
- ✅ Dark mode
- ✅ Responsive design
- ✅ API integration
- ✅ Error handling
- ✅ Loading states

**Frontend Vue modern dengan UX terbaik sudah siap digunakan! 🎉**
