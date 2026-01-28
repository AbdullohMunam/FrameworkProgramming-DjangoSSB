# 🏃‍♂️ SSB Academy - Framework Programming Project

Sistem Manajemen Sekolah Sepak Bola menggunakan Django REST Framework + Vue.js dengan approval workflow.

## 📋 Prerequisites

- Python 3.8+
- Node.js 16+
- Gmail account dengan 2FA (untuk email notifications)

## 🚀 Setup Backend (Django)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Konfigurasi Email (Gmail)
Edit file `ssb/.env` dan isi dengan kredensial Gmail Anda:

```env
# ssb/.env
GMAIL_ADDRESS=email-anda@gmail.com
GMAIL_APP_PASS=abcd-efgh-ijkl-mnop
```

**Cara mendapatkan Gmail App Password:**
1. Buka [Google Account Security](https://myaccount.google.com/security)
2. Aktifkan **2-Step Verification** (jika belum)
3. Buka [App Passwords](https://myaccount.google.com/apppasswords)
4. Pilih "Mail" dan "Other" (beri nama: SSB Academy)
5. Copy password 16 karakter (tanpa spasi)
6. Paste ke `GMAIL_APP_PASS` di file `.env`

### 3. Database Migration
```bash
cd ssb
python manage.py migrate
```

### 4. Create Superuser (sudah ada: admin/admin123)
```bash
python manage.py createsuperuser
# Password: admin
```

### 5. Jalankan Backend Server
```bash
python manage.py runserver
```

Backend berjalan di: http://localhost:8000

## 🎨 Setup Frontend (Vue.js)

### 1. Install Dependencies
```bash
cd frontend-ssb
npm install
```

### 2. Jalankan Development Server
```bash
npm run dev
```

Frontend berjalan di: http://localhost:5173

## 📝 Cara Penggunaan

### Flow Registrasi & Approval:

1. **User Register** (http://localhost:5173/register)
   - User mengisi form registrasi
   - Status awal: **Pending**
   - Email otomatis dikirim ke admin

2. **Admin Menerima Notifikasi**
   - Email notifikasi dikirim ke `GMAIL_ADDRESS`

3. **Admin Login** (http://localhost:5173/admin/login)
   - Username: `admin`
   - Password: `admin123`

4. **Admin Approve/Reject**
   - Dashboard menampilkan pending registrations
   - Approve atau Reject pendaftar
   - Email otomatis dikirim ke user

5. **User Login** (http://localhost:5173/login)
   - Setelah di-approve, user bisa login

### Akses:
- **Landing Page**: http://localhost:5173
- **Admin Dashboard**: http://localhost:5173/admin
- **User Login**: http://localhost:5173/login

## 🔐 Testing Email Tanpa Gmail

Edit `ssb/ssb/settings.py` line 217, uncomment:
```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

## 📂 Struktur Project

```
ssb/                          # Backend Django
├── .env                      # Konfigurasi email
├── manage.py
├── academy/                  # App utama
│   ├── models.py            # Player dengan approval fields
│   ├── signals.py           # Email notifications
│   └── views.py             # API dengan approve/reject
└── ssb/
    └── settings.py          # Config dengan dotenv

frontend-ssb/                # Frontend Vue.js
├── src/
│   ├── views/
│   │   ├── admin/
│   │   │   ├── DashboardView.vue
│   │   │   └── PendingView.vue    # ⭐ Approval interface
│   │   └── user/
│   ├── stores/auth.js
│   └── services/
└── vite.config.js
```

## 🔑 API Endpoints

### Authentication
- `POST /api/auth/login/` - Login dan dapatkan token
- `POST /api/auth/logout/` - Logout (hapus token)
- `GET /api/auth/profile/` - Get user profile (requires auth)

### CRUD Endpoints
- `GET/POST /api/players/` - List & Create players
- `GET/PUT/PATCH/DELETE /api/players/{id}/` - Detail, Update, Delete player
- `GET/POST /api/coaches/` - List & Create coaches
- `GET/PUT/PATCH/DELETE /api/coaches/{id}/` - Detail, Update, Delete coach
- `GET/POST /api/groups/` - List & Create groups
- `GET/PUT/PATCH/DELETE /api/groups/{id}/` - Detail, Update, Delete group
- `GET/POST /api/schedules/` - List & Create schedules
- `GET/PUT/PATCH/DELETE /api/schedules/{id}/` - Detail, Update, Delete schedule

### Documentation
- `/swagger/` - Swagger UI
- `/redoc/` - ReDoc
- `/swagger.json/` - OpenAPI schema

## 🔍 Query Parameters

### Pagination
```
GET /api/players/?page=2
```

### Search
```
GET /api/players/?search=budi
GET /api/coaches/?search=goalkeeper
```

### Ordering
```
GET /api/players/?ordering=name          # A-Z
GET /api/players/?ordering=-name         # Z-A
GET /api/players/?ordering=age           # Ascending
GET /api/schedules/?ordering=-date       # Newest first
```

### Kombinasi
```
GET /api/players/?search=budi&ordering=age&page=1
```

## 🔐 Authentication Usage

### 1. Login via API
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin"}'
```

Response:
```json
{
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
  "user_id": 1,
  "username": "admin",
  "email": "admin@example.com"
}
```

### 2. Use Token for Protected Endpoints
```bash
curl -X POST http://localhost:8000/api/players/ \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b" \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "age": 18, "position": "Forward"}'
```

## 🎨 Features

- ✅ **RESTful API** dengan Django REST Framework
- ✅ **Token Authentication** untuk keamanan
- ✅ **Permissions** - Read untuk semua, Write untuk authenticated users
- ✅ **Pagination** - 10 items per page
- ✅ **Search & Filter** - Cari dan urutkan data
- ✅ **CORS** - Frontend dan backend terpisah
- ✅ **Swagger UI** - Interactive API documentation
- ✅ **Frontend Decoupled** - HTML/CSS/JS konsumsi API
- ✅ **Django Templates** - Masih tersedia untuk fallback

## 🧪 Testing dengan Postman

1. Import collection dari Swagger
2. Buat environment variable `base_url` = `http://localhost:8000`
3. Login untuk mendapatkan token
4. Set token di Authorization header: `Token <your_token>`
5. Test semua endpoints

## 📖 Documentation

- **Swagger UI**: http://localhost:8000/swagger/
- **ReDoc**: http://localhost:8000/redoc/
- **Django Admin**: http://localhost:8000/admin/
- **Web Templates**: http://localhost:8000/ (masih bisa diakses)
- **Frontend**: http://localhost:3000/

## 🛠️ Development

### Backend Development
```bash
cd ssb
python manage.py runserver
```

### Frontend Development
```bash
cd frontend
python -m http.server 3000
```

### Create Test Data
```bash
python manage.py shell
```

```python
from academy.models import Coach, Group, Player, TrainingSchedule

# Create coach
coach = Coach.objects.create(
    name="John Doe",
    specialization="Goalkeeper Training",
    email="john@example.com"
)

# Create group
group = Group.objects.create(
    name="U-15 Team",
    coach=coach,
    level="Intermediate"
)

# Create player
player = Player.objects.create(
    name="Jane Smith",
    age=15,
    position="Forward",
    group=group
)
```

## 📝 Notes

- Template Django di `ssb/academy/templates/` masih ada dan berfungsi
- Frontend di `frontend/` adalah implementasi decoupled architecture
- Gunakan Swagger UI untuk testing dan dokumentasi API
- Untuk production: set `DEBUG=False`, configure ALLOWED_HOSTS, dan gunakan HTTPS

## 👨‍💻 Author

Project Framework Programming - Django REST Framework dengan Frontend Terpisah

## 📄 License

Educational Project
