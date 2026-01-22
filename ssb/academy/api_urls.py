from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import CoachViewSet, GroupViewSet, PlayerViewSet, TrainingScheduleViewSet
from .auth_views import LoginView, LogoutView, UserProfileView

router = DefaultRouter()
router.register(r'coaches', CoachViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'players', PlayerViewSet)
router.register(r'schedules', TrainingScheduleViewSet)

urlpatterns = [
    # Authentication endpoints
    path('auth/login/', LoginView.as_view(), name='api_login'),
    path('auth/logout/', LogoutView.as_view(), name='api_logout'),
    path('auth/profile/', UserProfileView.as_view(), name='api_profile'),
    
    # API CRUD endpoints
    path('', include(router.urls)),
]
