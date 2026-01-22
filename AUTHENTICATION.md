# 🔐 Panduan Authentication & Permissions

## Authentication System

Aplikasi SSB Academy menggunakan **Token Authentication** untuk mengamankan API.

### Cara Kerja

1. **Login** - Dapatkan token dengan username dan password
2. **Gunakan Token** - Sertakan token di header request untuk akses endpoint yang terproteksi
3. **Logout** - Hapus token untuk keluar dari sistem

---

## Default Credentials

```
Username: admin
Password: admin
```

> **Catatan**: Anda bisa membuat user baru melalui Django Admin di `http://localhost:8000/admin/`

---

## Permission Rules

### IsAuthenticatedOrReadOnly (Default untuk semua endpoint)

| Action | Method | Authentication Required | Description |
|--------|--------|------------------------|-------------|
| **List** | GET | ❌ Tidak | Semua orang bisa melihat daftar |
| **Retrieve** | GET | ❌ Tidak | Semua orang bisa melihat detail |
| **Create** | POST | ✅ Ya | Harus login untuk menambah data |
| **Update** | PUT/PATCH | ✅ Ya | Harus login untuk edit data |
| **Delete** | DELETE | ✅ Ya | Harus login untuk hapus data |

### Contoh Penggunaan

#### 1. Tanpa Login (Read-Only)
```bash
# Bisa melihat daftar pemain
curl http://localhost:8000/api/players/

# Bisa melihat detail pemain
curl http://localhost:8000/api/players/1/
```

#### 2. Dengan Login (Full Access)
```bash
# Login terlebih dahulu
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin"}'

# Response:
# {"token":"9f2e669859df3afc2363aa28d359da4976a1af2e",...}

# Tambah pemain baru (harus ada token)
curl -X POST http://localhost:8000/api/players/ \
  -H "Authorization: Token 9f2e669859df3afc2363aa28d359da4976a1af2e" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Budi Santoso",
    "age": 15,
    "position": "Forward",
    "group": 1
  }'

# Edit pemain (harus ada token)
curl -X PUT http://localhost:8000/api/players/1/ \
  -H "Authorization: Token 9f2e669859df3afc2363aa28d359da4976a1af2e" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Budi Updated",
    "age": 16,
    "position": "Forward",
    "group": 1
  }'

# Hapus pemain (harus ada token)
curl -X DELETE http://localhost:8000/api/players/1/ \
  -H "Authorization: Token 9f2e669859df3afc2363aa28d359da4976a1af2e"
```

---

## API Endpoints

### Authentication Endpoints

#### 1. Login
```http
POST /api/auth/login/
Content-Type: application/json

{
  "username": "admin",
  "password": "admin"
}
```

**Response Success:**
```json
{
  "token": "9f2e669859df3afc2363aa28d359da4976a1af2e",
  "user_id": 1,
  "username": "admin",
  "email": "admin@example.com",
  "message": "Login successful"
}
```

**Response Error:**
```json
{
  "non_field_errors": [
    "Unable to log in with provided credentials."
  ]
}
```

#### 2. Logout
```http
POST /api/auth/logout/
Authorization: Token <your_token>
```

**Response:**
```json
{
  "message": "Successfully logged out"
}
```

#### 3. User Profile
```http
GET /api/auth/profile/
Authorization: Token <your_token>
```

**Response:**
```json
{
  "id": 1,
  "username": "admin",
  "email": "admin@example.com",
  "first_name": "Admin",
  "last_name": "User"
}
```

---

## Frontend Integration

### Menyimpan Token
```javascript
// Setelah login berhasil
localStorage.setItem('auth_token', token);
```

### Menggunakan Token di Request
```javascript
const token = localStorage.getItem('auth_token');

fetch('http://localhost:8000/api/players/', {
  method: 'POST',
  headers: {
    'Authorization': `Token ${token}`,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    name: 'Budi',
    age: 15,
    position: 'Forward',
    group: 1
  })
});
```

### Logout
```javascript
// Hapus token dari localStorage
localStorage.removeItem('auth_token');
localStorage.removeItem('user_info');
```

---

## Error Responses

### 401 Unauthorized
Terjadi ketika:
- Token tidak valid
- Token sudah dihapus (logout)
- Token tidak disertakan untuk endpoint yang memerlukan authentication

```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden
Terjadi ketika:
- User authenticated tapi tidak punya permission untuk action tertentu

```json
{
  "detail": "You do not have permission to perform this action."
}
```

---

## Testing di Frontend

### 1. Buka Browser
```
http://localhost:3000
```

### 2. Coba Akses Menu Tanpa Login
- ✅ Bisa melihat daftar Players, Coaches, Groups, Schedules
- ❌ Tidak bisa klik tombol "Add", "Edit", "Delete"

### 3. Login
- Klik tombol "Login" di navbar
- Masukkan username: `admin`, password: `admin`
- Klik "Login"

### 4. Setelah Login
- ✅ Sekarang bisa klik tombol "Add", "Edit", "Delete"
- ✅ Bisa create, update, delete data

---

## Membuat User Baru

### Via Django Admin
1. Akses: `http://localhost:8000/admin/`
2. Login dengan admin/admin
3. Klik "Users" → "Add User"
4. Isi username dan password
5. Save

### Via Django Shell
```bash
cd ssb
python3 manage.py shell
```

```python
from django.contrib.auth.models import User

# Create regular user
user = User.objects.create_user(
    username='johndoe',
    email='john@example.com',
    password='password123'
)

# Create superuser
admin = User.objects.create_superuser(
    username='admin2',
    email='admin2@example.com',
    password='admin123'
)
```

---

## Troubleshooting

### Login Failed
**Masalah**: "Unable to log in with provided credentials"

**Solusi**:
1. Pastikan username dan password benar
2. Reset password user:
```bash
cd ssb
python3 manage.py shell -c "from django.contrib.auth.models import User; u = User.objects.get(username='admin'); u.set_password('admin'); u.save(); print('Password reset!')"
```

### Token Invalid
**Masalah**: "Invalid token"

**Solusi**:
1. Logout dan login ulang
2. Clear localStorage di browser
3. Cek apakah token sudah dihapus dari database

### Cannot Edit Data
**Masalah**: Tombol edit/delete tidak muncul

**Solusi**:
1. Pastikan sudah login
2. Check localStorage: `localStorage.getItem('auth_token')`
3. Reload halaman setelah login

---

## Security Best Practices

1. **Jangan hardcode credentials** di production
2. **Gunakan HTTPS** untuk production
3. **Set token expiration** untuk keamanan lebih baik
4. **Implement CORS dengan whitelist** untuk production
5. **Validate input** di backend dan frontend
6. **Rate limiting** untuk mencegah brute force attack

---

## Mengubah Permission Rules

Jika ingin mengubah permission rules, edit `views.py`:

```python
from rest_framework.permissions import IsAuthenticated, AllowAny

class PlayerViewSet(ModelViewSet):
    # Semua endpoint butuh authentication
    permission_classes = [IsAuthenticated]
    
    # Atau buat custom permission per action
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated()]
```

---

## Summary

✅ **Read (GET)**: Tidak perlu login
❌ **Write (POST/PUT/DELETE)**: Harus login

Ini adalah best practice untuk public API yang:
- Memungkinkan publik browsing data
- Melindungi data dari perubahan unauthorized
- Memudahkan integrasi dengan aplikasi lain

**Silakan login dengan `admin/admin` untuk full access!** 🚀
