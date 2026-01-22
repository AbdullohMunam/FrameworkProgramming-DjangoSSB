# SSB Academy - Frontend

Frontend aplikasi SSB Academy yang terpisah dari backend Django. Menggunakan HTML, CSS, dan JavaScript murni untuk konsumsi REST API.

## 🚀 Cara Menjalankan

### 1. Pastikan Backend Django Sudah Running

Backend harus berjalan di `http://localhost:8000`. Lihat panduan di folder `ssb/`.

### 2. Jalankan Frontend dengan Simple HTTP Server

#### Menggunakan Python:
```bash
# Di folder frontend
python -m http.server 3000
```

#### Menggunakan Node.js (jika terinstall):
```bash
# Install http-server secara global (hanya sekali)
npm install -g http-server

# Jalankan server
http-server -p 3000
```

#### Menggunakan PHP:
```bash
php -S localhost:3000
```

### 3. Akses Frontend

Buka browser dan akses: `http://localhost:3000`

## 📁 Struktur Folder

```
frontend/
├── index.html          # Halaman home
├── login.html          # Halaman login
├── players.html        # Daftar pemain
├── coaches.html        # Daftar pelatih
├── groups.html         # Kelompok latihan
├── schedules.html      # Jadwal latihan
├── swagger.html        # Link ke API docs
├── css/
│   └── style.css       # Stylesheet utama
├── js/
│   └── api.js          # API utilities & auth
└── img/                # Assets gambar
```

## 🔑 Login Credentials

Default user (buat dulu via Django Admin):
- **Username:** admin
- **Password:** admin

## ✨ Fitur

- ✅ **Separated Frontend & Backend** - Frontend dan backend terpisah sepenuhnya
- ✅ **Token Authentication** - Login dengan token-based auth
- ✅ **CRUD Operations** - List dan detail untuk semua entitas
- ✅ **Pagination** - Navigasi halaman data
- ✅ **Search & Filter** - Cari dan urutkan data
- ✅ **Responsive Design** - Tampilan optimal di semua device
- ✅ **Real-time API Consumption** - Fetch data langsung dari API

## 🎨 Teknologi

- **HTML5** - Struktur halaman
- **CSS3** - Styling (mirip dengan template Django)
- **Vanilla JavaScript** - Logika & API consumption
- **Fetch API** - HTTP requests ke backend

## 📖 Dokumentasi API

Akses Swagger UI untuk dokumentasi lengkap:
- Swagger UI: http://localhost:8000/swagger/
- ReDoc: http://localhost:8000/redoc/

## 🔧 Konfigurasi

Edit `js/api.js` jika backend berjalan di port/host berbeda:

```javascript
const API_BASE_URL = 'http://localhost:8000/api';
```

## 🐛 Troubleshooting

### CORS Error
Pastikan `django-cors-headers` sudah terinstall dan dikonfigurasi di backend:
```python
# settings.py
CORS_ALLOW_ALL_ORIGINS = True
```

### 401 Unauthorized
Token expired atau invalid. Login ulang untuk mendapatkan token baru.

### Cannot read properties of null
Backend tidak running atau API endpoint salah. Pastikan Django server berjalan di port 8000.

## 📝 Notes

- Template Django di folder `ssb/academy/templates/` tetap ada dan bisa digunakan
- Frontend ini adalah implementasi **decoupled architecture**
- Data disimpan di localStorage untuk token authentication
- Untuk production, gunakan HTTPS dan whitelist CORS origins
