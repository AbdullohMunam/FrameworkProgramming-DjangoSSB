### Apa itu SSB Academy?

> **SSB Academy** adalah aplikasi manajemen **Sekolah Sepak Bola (SSB)** berbasis web yang memudahkan proses pendaftaran, pengelolaan pemain, pelatih, dan jadwal latihan.



## ✨ Fitur Utama

### 👤 Fitur User (Pemain)

```
📝 Registrasi User      → Membuat user dan data pemain
🔐 Login/Logout          → Autentikasi aman
👤 Profil Pemain         → Lihat & edit data diri
📅 Jadwal Latihan        → Lihat jadwal tim
👥 Tim Saya              → Lihat anggota & pelatih
```

### 👨‍💼 Fitur Admin

```
📊 Dashboard             → Statistik overview
✅ Approval Workflow     → Approve/Reject pendaftaran
🏃 Kelola Pemain         → CRUD data pemain
🧑‍🏫 Kelola Pelatih        → CRUD data pelatih
👥 Kelola Grup           → CRUD grup latihan
📆 Kelola Jadwal         → CRUD jadwal latihan
```

---

## 🏗️ Arsitektur Decoupled

### Apa itu Arsitektur Decoupled?

> Memisahkan **Frontend** dan **Backend** menjadi aplikasi terpisah yang berkomunikasi via **REST API**

---

### Diagram Arsitektur

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER BROWSER                             │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  📦 FRONTEND (Vue.js 3)                                         │
│  ─────────────────────────                                      │
│  • Single Page Application (SPA)                                │
│  • User Interface & Routing                                     │
│  • State Management (Pinia)                                     │
│  • Port: 5173                                                   │
└─────────────────────────────┬───────────────────────────────────┘
                              │ HTTP/REST API
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  ⚙️ BACKEND (Django REST Framework)                             │
│  ───────────────────────────────────                            │
│  • REST API Endpoints                                           │
│  • Business Logic                                               │
│  • Authentication (Token)                                       │
│  • Port: 8000                                                   │
└─────────────────────────────┬───────────────────────────────────┘
                              │ ORM
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  🗄️ DATABASE (SQLite)                                           │
│  ─────────────────────                                          │
│  • Data Storage                                                 │
│  • Relationships                                                │
└─────────────────────────────────────────────────────────────────┘
```

---

### Mengapa Memilih Arsitektur Decoupled?

| Aspek | Keuntungan |
|-------|------------|
| 🔄 **Reusability** | API bisa dipakai mobile app / 3rd party |
| 👥 **Team Scalability** | Tim frontend & backend bisa kerja paralel |
| 🚀 **Performance** | Frontend bisa di-cache via CDN |
| 🔧 **Maintainability** | Perubahan frontend tidak ganggu backend |
| 🛡️ **Security** | Backend terpisah, lebih aman |

---



## 📊 Entity Relationship Diagram (ERD)

```
┌────────────────────┐                              ┌────────────────────┐
│       USER         │                              │       COACH        │
│  (Django Built-in) │                              │                    │
├────────────────────┤                              ├────────────────────┤
│ • id (PK)          │                              │ • id (PK)          │
│ • username         │                              │ • name             │
│ • password         │                              │ • license_level    │
│ • email            │                              │ • phone            │
│ • is_staff         │                              │ • photo            │
└─────────┬──────────┘                              └─────────┬──────────┘
          │                                                   │
          │ 1:1                                               │ 1:N
          │                                                   │
          ▼                                                   ▼
┌────────────────────┐         N:1          ┌────────────────────┐
│      PLAYER        │─────────────────────►│       GROUP        │
├────────────────────┤                      ├────────────────────┤
│ • id (PK)          │                      │ • id (PK)          │
│ • user (FK)        │                      │ • name             │
│ • name             │                      │ • coach (FK)       │
│ • age              │                      └─────────┬──────────┘
│ • position         │                                │
│ • photo            │                                │ 1:N
│ • group (FK)       │                                │
│ • status           │                                ▼
│ • registered_at    │                      ┌────────────────────┐
│ • approved_at      │                      │ TRAINING_SCHEDULE  │
│ • approved_by (FK) │                      ├────────────────────┤
└────────────────────┘                      │ • id (PK)          │
                                            │ • date             │
                                            │ • time             │
                                            │ • group (FK)       │
                                            └────────────────────┘
```

---

## 🔗 Hubungan Antar Model

### 1️⃣ ONE-TO-ONE: User ↔ Player

```python
user = models.OneToOneField(User, on_delete=models.CASCADE)
```

```
┌──────────┐    1    ────    1    ┌──────────┐
│   USER   │◄────────────────────►│  PLAYER  │
└──────────┘                      └──────────┘

• 1 User = 1 Player
• 1 Player = 1 User
• Jika User dihapus → Player otomatis terhapus (CASCADE)
```

---

### 2️⃣ ONE-TO-MANY: Coach → Group

```python
coach = models.ForeignKey(Coach, on_delete=models.SET_NULL, null=True)
```

```
┌──────────┐    1    ────    N    ┌──────────┐
│  COACH   │─────────────────────►│  GROUP   │
└──────────┘                      └──────────┘

• 1 Coach bisa melatih BANYAK Group
• 1 Group hanya punya 1 Coach
• Jika Coach dihapus → Group tetap ada (coach=NULL)
```

---

### 3️⃣ ONE-TO-MANY: Group → Player

```python
group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True)
```

```
┌──────────┐    1    ────    N    ┌──────────┐
│  GROUP   │─────────────────────►│  PLAYER  │
└──────────┘                      └──────────┘

• 1 Group bisa punya BANYAK Player
• 1 Player hanya masuk 1 Group
• Jika Group dihapus → Player tetap ada (group=NULL)
```

---

### 4️⃣ ONE-TO-MANY: Group → TrainingSchedule

```python
group = models.ForeignKey(Group, on_delete=models.CASCADE)
```

```
┌──────────┐    1    ────    N    ┌──────────────────┐
│  GROUP   │─────────────────────►│ TRAINING_SCHEDULE│
└──────────┘                      └──────────────────┘

• 1 Group bisa punya BANYAK Jadwal
• 1 Jadwal untuk 1 Group saja
• Jika Group dihapus → Jadwal ikut terhapus (CASCADE)
```

---

## 📋 Detail Model

### Model: Coach (Pelatih)

```python
class Coach(models.Model):
    name = models.CharField(max_length=100)           # Nama pelatih
    license_level = models.CharField(max_length=50)   # Level lisensi (C, B, A)
    phone = models.CharField(max_length=20)           # Nomor telepon
    photo = models.ImageField(upload_to='coaches/')   # Foto pelatih
```

---

### Model: Group (Kelompok Latihan)

```python
class Group(models.Model):
    name = models.CharField(max_length=50)            # Nama grup (U-12, U-15, U-20)
    coach = models.ForeignKey(Coach, ...)             # Pelatih yang melatih
```

---

### Model: Player (Pemain)

```python
class Player(models.Model):
    # Relasi ke User Django
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # Data Pribadi
    name = models.CharField(max_length=100)           # Nama lengkap
    age = models.IntegerField()                       # Umur
    position = models.CharField(max_length=50)        # Posisi (GK, DF, MF, FW)
    photo = models.ImageField(upload_to='players/')   # Foto pemain
    
    # Relasi ke Group
    group = models.ForeignKey(Group, ...)             # Grup latihan
    
    # Status Approval
    status = models.CharField(...)                    # pending/approved/rejected
    registered_at = models.DateTimeField(...)         # Waktu registrasi
    approved_at = models.DateTimeField(...)           # Waktu di-approve
    approved_by = models.ForeignKey(User, ...)        # Admin yang approve
```

---

### Model: TrainingSchedule (Jadwal Latihan)

```python
class TrainingSchedule(models.Model):
    date = models.DateField()                         # Tanggal latihan
    time = models.TimeField()                         # Jam latihan
    group = models.ForeignKey(Group, ...)             # Grup yang latihan
```

---



## 📁 Struktur Backend Django

```
ssb/                          ← Root Project
├── academy/                  ← Main Application
│   ├── models.py            ← Database Models
│   ├── serializers.py       ← API Serializers (JSON converter)
│   ├── views.py             ← API Views & ViewSets
│   ├── urls.py              ← URL Routing
│   ├── auth_views.py        ← Login/Register Views
│   ├── signals.py           ← Event Handlers
│   └── admin.py             ← Django Admin Config
│
├── ssb/                      ← Project Configuration
│   ├── settings.py          ← Django Settings
│   └── urls.py              ← Main URL Config
│
├── media/                    ← Uploaded Files
│   ├── coaches/             ← Foto pelatih
│   └── players/             ← Foto pemain
│
└── manage.py                 ← Django CLI
```

---

## 🛠️ Implementasi Arsitektur Decoupled

### 1️⃣ Backend: REST API dengan DRF

```python
# views.py - ViewSet untuk CRUD otomatis
class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    
    # Custom endpoint: GET /api/players/pending/
    @action(detail=False, methods=['get'])
    def pending(self, request):
        pending = Player.objects.filter(status='pending')
        return Response(PlayerSerializer(pending, many=True).data)
    
    # Custom endpoint: POST /api/players/{id}/approve/
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        player = self.get_object()
        player.status = 'approved'
        player.group_id = request.data.get('group')
        player.save()
        return Response({'status': 'approved'})
```

---

### 2️⃣ Backend: Serializer (Model → JSON)

```python
# serializers.py
class PlayerSerializer(serializers.ModelSerializer):
    group_name = serializers.CharField(source='group.name', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Player
        fields = ['id', 'name', 'age', 'position', 'group', 
                  'group_name', 'username', 'status']
```

**Input (Model):**
```python
Player(id=1, name="John", group_id=2, status="approved")
```

**Output (JSON):**
```json
{
  "id": 1,
  "name": "John",
  "group": 2,
  "group_name": "U-20 (Under 20)",
  "status": "approved"
}
```

---

### 3️⃣ Frontend: Service Layer (API Client)

```javascript
// services/index.js
import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:8000/api'
})

// Interceptor: Auto-attach token ke setiap request
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Token ${token}`
  }
  return config
})

// Service functions
export const playersService = {
  getAll: () => api.get('/players/'),
  getPending: () => api.get('/players/pending/'),
  approve: (id, groupId) => api.post(`/players/${id}/approve/`, { group: groupId }),
  reject: (id) => api.post(`/players/${id}/reject/`)
}
```

---

### 4️⃣ Frontend: State Management (Pinia)

```javascript
// stores/auth.js
export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: null
  }),
  
  getters: {
    isAuthenticated: (state) => !!state.token,
    isAdmin: (state) => state.user?.is_staff === true
  },
  
  actions: {
    async login(username, password) {
      const response = await authService.login(username, password)
      this.token = response.token
      this.user = response
      localStorage.setItem('token', response.token)
    }
  }
})
```

---

### 5️⃣ Frontend: Route Protection

```javascript
// router/index.js
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  // Route butuh login tapi belum login
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    return next({ name: 'login' })
  }
  
  // Route butuh admin tapi bukan admin
  if (to.meta.requiresAdmin && !authStore.isAdmin) {
    return next({ name: 'landing' })
  }
  
  next()
})
```
---

## ⚙️ Alur Kerja Modul

### Alur Registrasi & Approval

```
┌─────────────────────────────────────────────────────────────────┐
│                      ALUR REGISTRASI                            │
└─────────────────────────────────────────────────────────────────┘

  USER                 FRONTEND              BACKEND             DATABASE
   │                      │                     │                    │
   │  1. Isi Form         │                     │                    │
   ├─────────────────────►│                     │                    │
   │                      │ 2. POST /register/  │                    │
   │                      ├────────────────────►│                    │
   │                      │                     │ 3. Create User     │
   │                      │                     │    & Player        │
   │                      │                     ├───────────────────►│
   │                      │                     │    status=pending  │
   │                      │                     │◄───────────────────┤
   │                      │ 4. Success Response │                    │
   │                      │◄────────────────────┤                    │
   │  5. Notifikasi       │                     │                    │
   │◄─────────────────────┤                     │                    │
   │                      │                     │                    │

┌─────────────────────────────────────────────────────────────────┐
│                      ALUR APPROVAL                              │
└─────────────────────────────────────────────────────────────────┘

 ADMIN                 FRONTEND              BACKEND             DATABASE
   │                      │                     │                    │
   │  1. Buka Pending     │                     │                    │
   ├─────────────────────►│                     │                    │
   │                      │ 2. GET /players/    │                    │
   │                      │    pending/         │                    │
   │                      ├────────────────────►│                    │
   │                      │                     │ 3. Query pending   │
   │                      │                     ├───────────────────►│
   │                      │                     │◄───────────────────┤
   │                      │◄────────────────────┤                    │
   │  4. Lihat Daftar     │                     │                    │
   │◄─────────────────────┤                     │                    │
   │                      │                     │                    │
   │  5. Pilih & Approve  │                     │                    │
   ├─────────────────────►│                     │                    │
   │                      │ 6. POST /players/   │                    │
   │                      │    {id}/approve/    │                    │
   │                      ├────────────────────►│                    │
   │                      │                     │ 7. Update status   │
   │                      │                     │    = approved      │
   │                      │                     ├───────────────────►│
   │                      │                     │◄───────────────────┤
   │                      │◄────────────────────┤                    │
   │  8. Success          │                     │                    │
   │◄─────────────────────┤                     │                    │
```

---

## 🔐 Flow Autentikasi

```
┌─────────────────────────────────────────────────────────────────┐
│                    TOKEN AUTHENTICATION                         │
└─────────────────────────────────────────────────────────────────┘

1. LOGIN
   ┌──────┐                  ┌─────────┐              ┌──────────┐
   │ User │ POST /login/     │ Backend │  Generate    │ Database │
   │      │ {user, pass} ───►│         │─────────────►│  Token   │
   │      │                  │         │◄─────────────│          │
   │      │◄─────────────────│ {token} │              │          │
   └──────┘                  └─────────┘              └──────────┘
   
2. STORE TOKEN
   ┌──────────────┐
   │ localStorage │ token = "abc123xyz..."
   └──────────────┘

3. API REQUESTS
   ┌──────┐                           ┌─────────┐
   │ User │  GET /api/players/        │         │
   │      │  Header: Authorization:   │ Backend │
   │      │  Token abc123xyz... ─────►│         │
   │      │                           │         │
   │      │◄─────────────────────────│ {data}  │
   └──────┘                           └─────────┘
```
