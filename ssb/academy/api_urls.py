from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import CoachViewSet, GroupViewSet, PlayerViewSet, TrainingScheduleViewSet

router = DefaultRouter()
router.register(r'coaches', CoachViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'players', PlayerViewSet)
router.register(r'schedules', TrainingScheduleViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
