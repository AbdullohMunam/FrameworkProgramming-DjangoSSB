# ============================================================
#  API VIEWSETS (Django REST Framework)
# ============================================================

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from .models import Coach, Group, Player, TrainingSchedule
from .serializers import (
    CoachSerializer, GroupSerializer,
    PlayerSerializer, TrainingScheduleSerializer,
    CompleteProfileSerializer
)

class CoachViewSet(ModelViewSet):
    """
    API endpoint untuk CRUD Pelatih (Coach)
    - List/Read: Semua orang (termasuk guest)
    - Create/Update/Delete: Harus login
    - Searching: ?search=nama
    - Ordering: ?ordering=name atau ?ordering=-name (descending)
    """
    queryset = Coach.objects.all()
    serializer_class = CoachSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'specialization']
    ordering_fields = ['name', 'specialization', 'id']
    ordering = ['name']  # default ordering

class GroupViewSet(ModelViewSet):
    """
    API endpoint untuk CRUD Kelompok (Group)
    - List/Read: Semua orang
    - Create/Update/Delete: Harus login
    - Searching: ?search=nama_kelompok
    - Ordering: ?ordering=name
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'id']
    ordering = ['name']

class PlayerViewSet(ModelViewSet):
    """
    API endpoint untuk CRUD Pemain (Player)
    - List/Read: Semua orang
    - Create/Update/Delete: Harus login
    - Searching: ?search=nama_pemain
    - Ordering: ?ordering=name atau ?ordering=age
    - Pagination: ?page=1, ?page=2, dst
    """
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'position']
    ordering_fields = ['name', 'age', 'position', 'id']
    ordering = ['name']
    
    @action(detail=False, methods=['get'], permission_classes=[IsAdminUser])
    def pending(self, request):
        """Get list of pending player registrations"""
        pending_players = Player.objects.filter(status=Player.STATUS_PENDING).order_by('-registered_at')
        serializer = self.get_serializer(pending_players, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def approve(self, request, pk=None):
        """Approve a player registration and assign to group"""
        player = self.get_object()
        group_id = request.data.get('group')
        
        # Assign group if provided
        if group_id:
            try:
                group = Group.objects.get(id=group_id)
                player.group = group
            except Group.DoesNotExist:
                return Response({'error': 'Group not found'}, status=status.HTTP_400_BAD_REQUEST)
        
        player.status = Player.STATUS_APPROVED
        player.approved_at = timezone.now()
        player.approved_by = request.user
        player.save()
        
        # Send email to user
        try:
            group_info = f"\nAnda ditempatkan di grup: {player.group.name}" if player.group else ""
            send_mail(
                'Pendaftaran SSB Disetujui',
                f'Selamat! Pendaftaran Anda di SSB Academy telah disetujui.{group_info}\n\n'
                f'Detail Akun:\n'
                f'Username: {player.user.username}\n'
                f'Nama: {player.name}\n'
                f'Umur: {player.age} tahun\n'
                f'Posisi: {player.get_position_display()}{group_info}\n\n'
                f'Silakan login di: {settings.FRONTEND_URL}/login\n\n'
                f'Terima kasih!',
                settings.DEFAULT_FROM_EMAIL,
                [player.user.email],
                fail_silently=True
            )
        except:
            pass
        
        serializer = self.get_serializer(player)
        return Response({
            'status': 'approved', 
            'message': f'Player {player.name} berhasil disetujui',
            'player': serializer.data
        })
    
    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def reject(self, request, pk=None):
        """Reject a player registration"""
        player = self.get_object()
        player.status = Player.STATUS_REJECTED
        player.save()
        
        # Send email to user
        try:
            send_mail(
                'Pendaftaran SSB Ditolak',
                f'Maaf, pendaftaran Anda di SSB Academy ditolak. Silakan hubungi admin untuk informasi lebih lanjut.',
                settings.DEFAULT_FROM_EMAIL,
                [player.user.email],
                fail_silently=True
            )
        except:
            pass
        
        return Response({'status': 'rejected', 'message': f'Player {player.name or player.user.username} ditolak'})
    
    @action(detail=False, methods=['get', 'put', 'patch'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """Get or update current user's player profile"""
        try:
            player = request.user.player
        except Player.DoesNotExist:
            return Response({'error': 'Player profile not found'}, status=status.HTTP_404_NOT_FOUND)
        
        if request.method == 'GET':
            serializer = self.get_serializer(player)
            return Response(serializer.data)
        else:
            # Update profile
            serializer = CompleteProfileSerializer(player, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                # Return full player data
                player_serializer = self.get_serializer(player)
                return Response(player_serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TrainingScheduleViewSet(ModelViewSet):
    """
    API endpoint untuk CRUD Jadwal Latihan (TrainingSchedule)
    - List/Read: Semua orang
    - Create/Update/Delete: Harus login
    - Searching: ?search=nama_group
    - Ordering: ?ordering=date atau ?ordering=-date (newest first)
    """
    queryset = TrainingSchedule.objects.all()
    serializer_class = TrainingScheduleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['group__name', 'location']
    ordering_fields = ['date', 'time', 'id']
    ordering = ['-date']  # default: newest first


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


from django.views.decorators.http import require_POST

# ============================================================
#  DELETE PLAYER
# ============================================================
@require_POST
def player_delete(request, pk):
    player = get_object_or_404(Player, pk=pk)
    player.delete()
    return redirect('player_list')


# ============================================================
#  DELETE COACH
# ============================================================
@require_POST
def coach_delete(request, pk):
    coach = get_object_or_404(Coach, pk=pk)
    coach.delete()
    return redirect('coach_list')


# ============================================================
#  DELETE GROUP
# ============================================================
@require_POST
def group_delete(request, pk):
    group = get_object_or_404(Group, pk=pk)
    group.delete()
    return redirect('group_list')


# ============================================================
#  DELETE TRAINING SCHEDULE
# ============================================================
@require_POST
def schedule_delete(request, pk):
    schedule = get_object_or_404(TrainingSchedule, pk=pk)
    schedule.delete()
    return redirect('schedule_list')
