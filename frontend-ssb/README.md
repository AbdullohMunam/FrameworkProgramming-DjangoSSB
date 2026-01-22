# SSB Academy Frontend (Vue 3 + Vite)

Modern frontend application untuk SSB Academy Management System menggunakan Vue 3, Vite, dan Tailwind CSS.

## 🚀 Tech Stack

- **Vue 3** - Progressive JavaScript framework
- **Vite** - Next generation frontend tooling
- **Vue Router** - Official router untuk Vue.js
- **Pinia** - State management yang intuitif
- **Axios** - HTTP client
- **Tailwind CSS** - Utility-first CSS framework
- **Headless UI** - Unstyled accessible UI components
- **Heroicons** - Beautiful hand-crafted SVG icons

## 📦 Installation

```bash
npm install
```

## 🏃 Development

```bash
npm run dev
```

Aplikasi akan berjalan di `http://localhost:5173`

Backend Django harus berjalan di `http://localhost:8000`

## 🏗️ Build

```bash
npm run build
```

## 🎨 Features

- ✅ Authentication dengan token-based
- ✅ Dark mode toggle
- ✅ Responsive design (mobile, tablet, desktop)
- ✅ CRUD operations untuk Players, Coaches, Groups, Schedules
- ✅ Search & filter functionality
- ✅ Pagination
- ✅ Image upload dengan preview
- ✅ Toast notifications
- ✅ Modal dialogs
- ✅ Loading states
- ✅ Form validation
- ✅ Delete confirmation

## 🔐 Default Credentials

- Username: `admin`
- Password: `admin`

## 📁 Project Structure

```
src/
├── assets/          # Static assets
├── components/      # Vue components
├── composables/     # Composition API functions
├── router/          # Vue Router configuration
├── services/        # API services
├── stores/          # Pinia stores
├── utils/           # Utility functions
├── views/           # Page components
├── App.vue          # Root component
└── main.js          # Entry point
```
