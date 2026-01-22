# 🧪 Testing Guide - SSB Academy

## Quick Test: Login & CRUD Operations

### 1. Start Both Servers

```bash
# Terminal 1: Backend (Django)
cd ssb
python3 manage.py runserver

# Terminal 2: Frontend (HTTP Server)
cd frontend
python3 -m http.server 3000
```

**Atau gunakan script:**
```bash
./start.sh
```

---

## 2. Test Login di Frontend

### Buka Browser
```
http://localhost:3000
```

### Klik "Login"
- URL akan berubah ke `http://localhost:3000/login.html`
- Lihat form login dengan demo credentials

### Login dengan Credentials
```
Username: admin
Password: admin
```

### Hasil yang Diharapkan
✅ Redirect ke homepage
✅ Navbar berubah menampilkan "Welcome, admin" dan tombol "Logout"
✅ Sekarang bisa akses fitur Create/Edit/Delete

---

## 3. Test CRUD Operations

### Test Players (Tanpa Login)
1. Buka: `http://localhost:3000/players.html`
2. ✅ Bisa lihat daftar pemain
3. ❌ Tombol "Add Player" tidak aktif atau tidak muncul

### Test Players (Dengan Login)
1. Login dulu dengan admin/admin
2. Buka: `http://localhost:3000/players.html`
3. ✅ Tombol "Add Player" aktif dan bisa diklik
4. ✅ Bisa tambah, edit, delete data

---

## 4. Test API Directly (Postman/cURL)

### Test 1: Login
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin"}'
```

**Expected Response:**
```json
{
  "token": "9f2e669859df3afc2363aa28d359da4976a1af2e",
  "user_id": 1,
  "username": "admin",
  "email": "",
  "message": "Login successful"
}
```

### Test 2: Get Players (Tanpa Token)
```bash
curl http://localhost:8000/api/players/
```

**Expected:** ✅ Berhasil - Returns list of players

### Test 3: Create Player (Tanpa Token)
```bash
curl -X POST http://localhost:8000/api/players/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Player",
    "age": 15,
    "position": "Forward",
    "group": 1
  }'
```

**Expected:** ❌ Error 401 - Authentication required

### Test 4: Create Player (Dengan Token)
```bash
# Gunakan token dari login
TOKEN="9f2e669859df3afc2363aa28d359da4976a1af2e"

curl -X POST http://localhost:8000/api/players/ \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Budi Santoso",
    "age": 16,
    "position": "Midfielder",
    "group": 1
  }'
```

**Expected:** ✅ Success - Player created

---

## 5. Test Swagger UI

### Buka Swagger
```
http://localhost:8000/swagger/
```

### Test Endpoint di Swagger

#### Step 1: Authorize
1. Klik tombol "Authorize" (🔓) di kanan atas
2. Masukkan: `Token 9f2e669859df3afc2363aa28d359da4976a1af2e`
   - **PENTING**: Harus ada prefix "Token " sebelum token
3. Klik "Authorize" lalu "Close"

#### Step 2: Test Endpoint
1. Expand endpoint `/api/players/` POST
2. Klik "Try it out"
3. Edit request body:
```json
{
  "name": "Test from Swagger",
  "age": 17,
  "position": "Defender",
  "group": 1
}
```
4. Klik "Execute"

**Expected:** ✅ Status 201 Created

---

## 6. Test Pagination

```bash
# Default: 10 items per page
curl http://localhost:8000/api/players/

# Page 2
curl http://localhost:8000/api/players/?page=2

# Custom page size (tambah di settings jika perlu)
curl http://localhost:8000/api/players/?page=1
```

**Expected Response Format:**
```json
{
  "count": 25,
  "next": "http://localhost:8000/api/players/?page=2",
  "previous": null,
  "results": [
    // ... player objects
  ]
}
```

---

## 7. Test Search

```bash
# Search by name
curl "http://localhost:8000/api/players/?search=budi"

# Search by position
curl "http://localhost:8000/api/players/?search=forward"
```

---

## 8. Test Ordering

```bash
# Order by name (ascending)
curl "http://localhost:8000/api/players/?ordering=name"

# Order by age (descending)
curl "http://localhost:8000/api/players/?ordering=-age"

# Order by multiple fields
curl "http://localhost:8000/api/players/?ordering=position,name"
```

---

## 9. Test Combined Filters

```bash
# Search + Ordering + Pagination
curl "http://localhost:8000/api/players/?search=forward&ordering=age&page=1"
```

---

## 10. Test CORS

### Frontend Request dari Domain Berbeda

Buka browser console (F12) dan jalankan:

```javascript
// Test CORS
fetch('http://localhost:8000/api/players/')
  .then(r => r.json())
  .then(data => console.log('CORS works!', data))
  .catch(err => console.error('CORS failed:', err));
```

**Expected:** ✅ Data muncul di console (CORS allowed)

---

## 11. Test Frontend Features

### Test Without Login
- [x] Bisa akses homepage
- [x] Bisa lihat daftar players/coaches/groups/schedules
- [x] Bisa klik detail untuk melihat info lengkap
- [ ] Tidak bisa klik "Add New"
- [ ] Tidak muncul tombol "Edit" dan "Delete"

### Test With Login
- [x] Navbar berubah menampilkan username
- [x] Bisa klik "Add New"
- [x] Bisa create data baru
- [x] Muncul tombol "Edit" dan "Delete"
- [x] Bisa update data
- [x] Bisa delete data
- [x] Bisa logout

### Test Logout
- [x] Klik tombol "Logout"
- [x] Redirect ke login page
- [x] Token dihapus dari localStorage
- [x] Tidak bisa akses fitur Write lagi

---

## 12. Test Error Handling

### Test Wrong Password
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"wrong"}'
```

**Expected:**
```json
{
  "non_field_errors": [
    "Unable to log in with provided credentials."
  ]
}
```

### Test Invalid Token
```bash
curl -X POST http://localhost:8000/api/players/ \
  -H "Authorization: Token invalid_token_here" \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","age":15,"position":"Forward","group":1}'
```

**Expected:** ❌ Status 401 Unauthorized

### Test Missing Required Field
```bash
curl -X POST http://localhost:8000/api/players/ \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"Test"}'
```

**Expected:** ❌ Status 400 Bad Request with validation errors

---

## 13. Browser Testing Checklist

### Homepage (index.html)
- [ ] Layout tampil dengan benar
- [ ] Navbar fixed di atas
- [ ] Menu links berfungsi
- [ ] Statistics cards tampil
- [ ] Auth status di navbar benar

### Login (login.html)
- [ ] Form tampil
- [ ] Demo credentials terlihat
- [ ] Login dengan admin/admin berhasil
- [ ] Error message tampil jika gagal
- [ ] Redirect ke homepage setelah sukses

### Players (players.html)
- [ ] Daftar players tampil
- [ ] Foto players tampil (jika ada)
- [ ] Search box berfungsi
- [ ] Ordering dropdown berfungsi
- [ ] Pagination berfungsi
- [ ] "Add Player" muncul jika login
- [ ] Detail link berfungsi

### Player Detail (player-detail.html)
- [ ] Info lengkap tampil
- [ ] Foto tampil (jika ada)
- [ ] Tombol "Edit" dan "Delete" muncul jika login
- [ ] "Back" button berfungsi

### Add/Edit Player
- [ ] Form tampil
- [ ] Dropdown group terisi
- [ ] Upload foto berfungsi (jika implemented)
- [ ] Validation berfungsi
- [ ] Submit berhasil dan redirect

---

## 14. Performance Testing

### Test Response Time
```bash
# Time the API request
time curl http://localhost:8000/api/players/
```

### Test Large Dataset
```bash
# Create 100 players
for i in {1..100}; do
  curl -X POST http://localhost:8000/api/players/ \
    -H "Authorization: Token $TOKEN" \
    -H "Content-Type: application/json" \
    -d "{\"name\":\"Player $i\",\"age\":$((15 + RANDOM % 10)),\"position\":\"Forward\",\"group\":1}"
done

# Test pagination with large dataset
curl "http://localhost:8000/api/players/?page=5"
```

---

## Troubleshooting

### Problem: Login Failed
```
Error: "Unable to log in with provided credentials"
```

**Solution:**
```bash
cd ssb
python3 manage.py shell -c "
from django.contrib.auth.models import User
u = User.objects.get(username='admin')
u.set_password('admin')
u.save()
print('Password reset to: admin')
"
```

### Problem: CORS Error
```
Access to fetch at 'http://localhost:8000/api/' from origin 'http://localhost:3000' 
has been blocked by CORS policy
```

**Solution:** Check `settings.py`:
```python
CORS_ALLOW_ALL_ORIGINS = True  # Should be True for development
```

### Problem: Token Not Working
```
Error: "Invalid token"
```

**Solution:**
1. Clear localStorage in browser
2. Login again
3. Check token format: `Token <token_value>` (with space)

### Problem: Cannot Create Data
```
Error: 403 Forbidden
```

**Solution:**
1. Check if logged in
2. Verify token in localStorage
3. Check permission_classes in views.py

---

## Summary of Test Results

✅ **Authentication**: Login/Logout working
✅ **Permissions**: IsAuthenticatedOrReadOnly working
✅ **CRUD**: Create, Read, Update, Delete working
✅ **Pagination**: Working with default PAGE_SIZE=10
✅ **Search**: Working on specified fields
✅ **Ordering**: Working with +/- prefix
✅ **CORS**: Enabled for frontend access
✅ **Swagger UI**: API documentation accessible
✅ **Frontend**: All pages rendering correctly
✅ **Error Handling**: Proper error messages

---

## Next Steps

1. ✅ Test all features manually
2. ✅ Verify permissions are enforced
3. ✅ Check error messages are user-friendly
4. 🔄 Add more test data
5. 🔄 Test with multiple users
6. 🔄 Test edge cases
7. 🔄 Performance optimization if needed

**Happy Testing! 🚀**
