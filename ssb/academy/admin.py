from django.contrib import admin
from .models import Coach, Group, Player, TrainingSchedule

admin.site.register(Coach)              # manajemen data pelatih
admin.site.register(Group)              # manajemen kelompok latihan
admin.site.register(Player)             # manajemen pemain
admin.site.register(TrainingSchedule)   # manajemen jadwal latihan
