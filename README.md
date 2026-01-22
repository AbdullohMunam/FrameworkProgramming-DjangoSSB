# 🏃‍♂️ SSB Academy - Framework Programming Project

Sistem Manajemen Sekolah Sepak Bola menggunakan Django REST Framework dengan frontend yang terpisah.

## 📚 Modul yang Diimplementasikan

### ✅ Pertemuan 9: Autentikasi & Permissions
- Token Authentication dengan Django REST Framework
- Login/Logout endpoints
- Permission classes: `IsAuthenticatedOrReadOnly`
- User profile endpoint

### ✅ Pertemuan 10: Filtering, Searching & Pagination
- Pagination dengan `PageNumberPagination` (10 items per page)
- Search filter untuk mencari data berdasarkan keyword
- Ordering filter untuk mengurutkan data
- Query parameters: `?page=2&search=keyword&ordering=-name`

### ✅ Pertemuan 11: Frontend JavaScript dengan CORS
- CORS configuration untuk komunikasi frontend-backend
- Frontend terpisah menggunakan HTML/CSS/JavaScript
- Fetch API untuk konsumsi REST API
- Dynamic rendering dengan JavaScript

### ✅ Swagger UI Documentation
- API documentation dengan `drf-yasg`
- Interactive Swagger UI di `/swagger/`
- ReDoc alternative di `/redoc/`
- OpenAPI schema

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Database Migration

```bash
cd ssb
python manage.py migrate
```

### 3. Create Superuser (untuk login)

```bash
python manage.py createsuperuser
# Username: admin
# Password: admin
```

### 4. Run Django Backend

```bash
python manage.py runserver
```

Backend akan berjalan di: `http://localhost:8000`

### 5. Run Frontend (Terminal Baru)

```bash
cd ../frontend
python -m http.server 3000
```

Frontend akan berjalan di: `http://localhost:3000`

## 📂 Struktur Project

```
FrameworkProgramming-DjangoSSB/
├── ssb/                        # Backend Django
│   ├── manage.py
│   ├── db.sqlite3
│   ├── academy/                # Main app
│   │   ├── models.py           # Coach, Group, Player, Schedule
│   │   ├── serializers.py      # DRF Serializers
│   │   ├── views.py            # ViewSets dengan filters & permissions
│   │   ├── auth_views.py       # Login/Logout views
│   │   ├── api_urls.py         # API routing
│   │   ├── urls.py             # Web routing (template)
│   │   └── templates/          # Django templates (masih ada)
│   └── ssb/
│       ├── settings.py         # DRF config, CORS, Swagger
│       └── urls.py             # Swagger UI routes
│
├── frontend/                   # Frontend Terpisah
│   ├── index.html              # Home page
│   ├── login.html              # Login page
│   ├── players.html            # Players list
│   ├── coaches.html            # Coaches list
│   ├── groups.html             # Groups list
│   ├── schedules.html          # Schedules list
│   ├── swagger.html            # API docs page
│   ├── css/
│   │   └── style.css           # Styling mirip template Django
│   ├── js/
│   │   └── api.js              # API utilities & authentication
│   └── README.md
│
└── requirements.txt
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
