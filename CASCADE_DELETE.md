# Bidirectional Cascade Delete - User ↔ Player

## ✅ Implementasi

### Perubahan di `academy/models.py`:

```python
from django.db.models.signals import post_delete
from django.dispatch import receiver

class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='player')
    # ... fields lainnya

# Signal untuk menghapus User ketika Player dihapus
@receiver(post_delete, sender=Player)
def delete_user_with_player(sender, instance, **kwargs):
    """
    Delete associated User when Player is deleted
    This creates bidirectional cascade delete:
    - User deleted → Player deleted (via CASCADE)
    - Player deleted → User deleted (via this signal)
    """
    try:
        if instance.user:
            instance.user.delete()
    except User.DoesNotExist:
        pass  # User already deleted
```

---

## 🔄 Cara Kerja

### **Scenario 1: User Dihapus**
```
Admin hapus User → CASCADE → Player otomatis terhapus
```
- Menggunakan `on_delete=models.CASCADE` di OneToOneField
- Built-in Django behavior
- ✅ Sudah bekerja sejak awal

### **Scenario 2: Player Dihapus** 
```
Admin hapus Player → Signal → User otomatis terhapus
```
- Menggunakan Django signal `post_delete`
- Custom implementation
- ✅ Baru ditambahkan

---

## ✅ Test Results

```
============================================================
TESTING BIDIRECTIONAL CASCADE DELETE
============================================================

1️⃣ BEFORE DELETE:
   Total Users (non-superuser): 47
   Total Players: 46

2️⃣ DELETING PLAYER:
   Player: Manuel Neuer
   Associated User: manuelneuer

3️⃣ AFTER DELETE:
   Total Users (non-superuser): 46 (was 47)
   Total Players: 45 (was 46)
   User "manuelneuer" still exists: False

✅ SUCCESS: User was automatically deleted when Player was deleted!
   Bidirectional cascade delete is working correctly.
============================================================
```

---

## 💡 Kenapa Perlu Bidirectional?

### **Tanpa Bidirectional:**
- Hapus User → Player ikut terhapus ✅
- Hapus Player → User tetap ada ❌ (orphan user)

### **Dengan Bidirectional:**
- Hapus User → Player ikut terhapus ✅
- Hapus Player → User ikut terhapus ✅
- Tidak ada orphan data!

---

## 🎯 Use Cases

### 1. **Admin Dashboard - Delete Player**
Admin hapus pemain dari list players → User account juga terhapus

### 2. **Bulk Delete**
Admin hapus banyak players sekaligus → Semua user accounts terkait juga terhapus

### 3. **Data Cleanup**
Script maintenance untuk hapus data lama → Tidak ada user tanpa player

### 4. **Reject Registration**
Admin reject dan hapus player → User account juga bersih

---

## ⚠️ Important Notes

### **Keamanan Signal:**
```python
try:
    if instance.user:
        instance.user.delete()
except User.DoesNotExist:
    pass  # User already deleted
```

- Exception handling untuk cegah error jika User sudah terhapus
- Check `if instance.user` sebelum delete
- Tidak akan crash jika User tidak ada

### **Infinite Loop Prevention:**
Django otomatis mencegah infinite loop:
```
Player.delete() → Signal delete User → CASCADE delete Player (STOP)
```
Signal `post_delete` hanya trigger sekali, tidak akan loop.

---

## 🧪 Cara Test Manual

### Via Django Admin:
1. Login ke `/admin`
2. Pilih **Academy > Players**
3. Select player dan Delete
4. Periksa **Authentication > Users** → User juga hilang

### Via API (Admin Dashboard):
1. Login admin di frontend
2. Buka **Players Management**
3. Click Delete pada player
4. User terkait otomatis terhapus

### Via Django Shell:
```bash
python manage.py shell
```
```python
from django.contrib.auth.models import User
from academy.models import Player

# Ambil satu player
player = Player.objects.first()
username = player.user.username

# Hapus player
player.delete()

# Cek user
User.objects.filter(username=username).exists()  # Should be False
```

---

## 📊 Database Relationship

```
┌─────────────┐           ┌──────────────┐
│    User     │◄──────────┤    Player    │
│  (Django)   │ CASCADE   │  (Academy)   │
└─────────────┘           └──────────────┘
      ▲                          │
      │                          │
      └──────────────────────────┘
           DELETE via Signal
```

**OneToOne Relationship dengan Bidirectional Cascade Delete**

---

## 🚀 Benefits

1. **Data Integrity**: Tidak ada orphan users
2. **Clean Database**: Semua relasi terjaga
3. **Easy Maintenance**: Admin tidak perlu manual hapus keduanya
4. **Consistent**: Behavior sama dari sisi manapun (User/Player)
5. **Safe**: Exception handling mencegah errors

---

## 🔧 Maintenance

### Jika Butuh Soft Delete:
Tambahkan field `is_deleted` instead of actual delete:
```python
class Player(models.Model):
    is_deleted = models.BooleanField(default=False)
    
    def soft_delete(self):
        self.is_deleted = True
        self.user.is_active = False
        self.save()
        self.user.save()
```

### Jika Butuh Keep User:
Comment signal atau tambahkan kondisi:
```python
@receiver(post_delete, sender=Player)
def delete_user_with_player(sender, instance, **kwargs):
    if not getattr(instance, 'keep_user', False):
        if instance.user:
            instance.user.delete()
```

---

## ✅ Checklist Implementasi

- [x] Import signal dan receiver di models.py
- [x] Buat function delete_user_with_player
- [x] Decorator @receiver(post_delete, sender=Player)
- [x] Exception handling untuk User.DoesNotExist
- [x] Test via script Python
- [x] Verify hasil (User count berkurang)
- [x] Documentation

**Status: COMPLETE ✅**

---

Semua siap! Delete Player atau User dari sisi manapun, keduanya akan terhapus. 🎯
