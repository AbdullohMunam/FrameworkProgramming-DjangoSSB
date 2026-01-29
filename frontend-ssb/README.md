# Frontend SSB

Frontend aplikasi SSB Academy Management menggunakan Vue 3 + Vite.

## Tech Stack

- **Vue 3** - Framework JavaScript
- **Vite** - Build tool & dev server
- **Pinia** - State management
- **Vue Router** - Routing
- **Axios** - HTTP client
- **TailwindCSS** - Styling

## IDE Setup

[VS Code](https://code.visualstudio.com/) + [Vue (Official)](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (dan disable Vetur).

## Browser Setup (optional)

- Chromium: [Vue.js devtools](https://chromewebstore.google.com/detail/vuejs-devtools/nhdogjmejiglipccpnnnanhbledajbpd)
- Firefox: [Vue.js devtools](https://addons.mozilla.org/en-US/firefox/addon/vue-js-devtools/)

## Project Setup

```sh
npm install
```

### Development

```sh
npm run dev
```

### Production Build

```sh
npm run build
```

### Preview Production Build

```sh
npm run preview
```

## Struktur Project

```
src/
├── assets/          # CSS dan asset statis
├── components/      # Komponen reusable
├── layouts/         # Layout components
├── router/          # Vue Router configuration
├── services/        # API services
├── stores/          # Pinia stores
└── views/           # Page components
    ├── admin/       # Admin pages
    └── user/        # User pages
```
