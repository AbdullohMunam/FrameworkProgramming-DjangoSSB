# ============================================================
#  API VIEWSETS (Django REST Framework)
# ============================================================

from rest_framework.viewsets import ModelViewSet
from .models import Coach, Group, Player, TrainingSchedule
from .serializers import (
    CoachSerializer, GroupSerializer,
    PlayerSerializer, TrainingScheduleSerializer
)

class CoachViewSet(ModelViewSet):
    queryset = Coach.objects.all()
    serializer_class = CoachSerializer
    # API CRUD untuk pelatih

class GroupViewSet(ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    # API CRUD kelompok latihan

class PlayerViewSet(ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    # API CRUD pemain

class TrainingScheduleViewSet(ModelViewSet):
    queryset = TrainingSchedule.objects.all()
    serializer_class = TrainingScheduleSerializer
    # API CRUD jadwal latihan


# ============================================================
#  WEB VIEWS (HTML PAGES)
# ============================================================

from django.shortcuts import render, get_object_or_404, redirect

# ---------- HOME ----------
def home(request):
    return render(request, 'academy/home.html')


# ============================================================
#  PLAYER (LIST, DETAIL, ADD, EDIT)
# ============================================================

def player_list(request):
    players = Player.objects.all()
    return render(request, 'academy/player_list.html', {'players': players})


def player_detail(request, pk):
    player = get_object_or_404(Player, pk=pk)
    return render(request, 'academy/player_detail.html', {'player': player})


def player_add(request):
    groups = Group.objects.all()

    if request.method == 'POST':
        data = {
            'name': request.POST['name'],
            'age': request.POST['age'],
            'position': request.POST['position'],
            'group_id': request.POST['group']
        }
        photo = request.FILES.get('photo')
        if photo:
            data['photo'] = photo
        Player.objects.create(**data)
        return redirect('player_list')

    return render(request, 'academy/player_form.html', {
        'groups': groups,
        'title': 'Tambah Pemain'
    })


def player_edit(request, pk):
    player = get_object_or_404(Player, pk=pk)
    groups = Group.objects.all()

    if request.method == 'POST':
        player.name = request.POST['name']
        player.age = request.POST['age']
        player.position = request.POST['position']
        player.group_id = request.POST['group']
        photo = request.FILES.get('photo')
        if photo:
            player.photo = photo
        player.save()
        return redirect('player_detail', pk=pk)

    return render(request, 'academy/player_form.html', {
        'player': player,
        'groups': groups,
        'title': 'Edit Pemain'
    })


# ============================================================
#  COACH (LIST, DETAIL, ADD, EDIT)
# ============================================================

def coach_list(request):
    coaches = Coach.objects.all()
    return render(request, 'academy/coach_list.html', {'coaches': coaches})


def coach_detail(request, pk):
    coach = get_object_or_404(Coach, pk=pk)
    return render(request, 'academy/coach_detail.html', {'coach': coach})


def coach_add(request):
    if request.method == 'POST':
        data = {
        #   urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  'name': request.POST['name'],
            'license_level': request.POST.get('license_level', ''),
            'phone': request.POST.get('phone', '')
        }
        photo = request.FILES.get('photo')
        if photo:
            data['photo'] = photo
        Coach.objects.create(**data)
        return redirect('coach_list')

    return render(request, 'academy/coach_form.html', {
        'title': 'Tambah Pelatih'
    })


def coach_edit(request, pk):
    coach = get_object_or_404(Coach, pk=pk)

    if request.method == 'POST':
        coach.name = request.POST['name']
        coach.license_level = request.POST.get('license_level', '')
        coach.phone = request.POST.get('phone', '')
        photo = request.FILES.get('photo')
        if photo:
            coach.photo = photo
        coach.save()
        return redirect('coach_detail', pk=pk)

    return render(request, 'academy/coach_form.html', {
        'coach': coach,
        'title': 'Edit Pelatih'
    })


# ============================================================
#  GROUP (LIST, DETAIL, ADD, EDIT)
# ============================================================

def group_list(request):
    groups = Group.objects.all()
    return render(request, 'academy/group_list.html', {'groups': groups})


def group_detail(request, pk):
    group = get_object_or_404(Group, pk=pk)
    players = Player.objects.filter(group=group)
    schedules = TrainingSchedule.objects.filter(group=group)
    return render(request, 'academy/group_detail.html', {
        'group': group,
        'players': players,
        'schedules': schedules
    })


def group_add(request):
    coaches = Coach.objects.all()

    if request.method == 'POST':
        Group.objects.create(
            name=request.POST['name'],
            coach_id=request.POST['coach']
        )
        return redirect('group_list')

    return render(request, 'academy/group_form.html', {
        'coaches': coaches,
        'title': 'Tambah Kelompok'
    })


def group_edit(request, pk):
    group = get_object_or_404(Group, pk=pk)
    coaches = Coach.objects.all()

    if request.method == 'POST':
        group.name = request.POST['name']
        group.coach_id = request.POST['coach']
        group.save()
        return redirect('group_detail', pk=pk)

    return render(request, 'academy/group_form.html', {
        'group': group,
        'coaches': coaches,
        'title': 'Edit Kelompok'
    })


# ============================================================
#  TRAINING SCHEDULE (LIST, DETAIL, ADD, EDIT)
# ============================================================

def schedule_list(request):
    schedules = TrainingSchedule.objects.all()
    return render(request, 'academy/schedule_list.html', {'schedules': schedules})


def schedule_detail(request, pk):
    schedule = get_object_or_404(TrainingSchedule, pk=pk)
    return render(request, 'academy/schedule_detail.html', {'schedule': schedule})


def schedule_add(request):
    groups = Group.objects.all()

    if request.method == 'POST':
        TrainingSchedule.objects.create(
            date=request.POST['date'],
            time=request.POST['time'],
            group_id=request.POST['group']
        )
        return redirect('schedule_list')

    return render(request, 'academy/schedule_form.html', {
        'groups': groups,
        'title': 'Tambah Jadwal'
    })


def schedule_edit(request, pk):
    schedule = get_object_or_404(TrainingSchedule, pk=pk)
    groups = Group.objects.all()

    if request.method == 'POST':
        schedule.date = request.POST['date']
        schedule.time = request.POST['time']
        schedule.group_id = request.POST['group']
        schedule.save()
        return redirect('schedule_detail', pk=pk)

    return render(request, 'academy/schedule_form.html', {
        'schedule': schedule,
        'groups': groups,
        'title': 'Edit Jadwal'
    })
