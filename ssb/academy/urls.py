from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('players/', views.player_list, name='player_list'),
    path('players/<int:pk>/', views.player_detail, name='player_detail'),

    path('coaches/', views.coach_list, name='coach_list'),
    path('coaches/<int:pk>/', views.coach_detail, name='coach_detail'),

    path('groups/', views.group_list, name='group_list'),
    path('groups/<int:pk>/', views.group_detail, name='group_detail'),

    path('schedules/', views.schedule_list, name='schedule_list'),
    path('schedules/<int:pk>/', views.schedule_detail, name='schedule_detail'),
    
    
    # PLAYERS
	path('players/add/', views.player_add, name='player_add'),
	path('players/<int:pk>/edit/', views.player_edit, name='player_edit'),

	# COACHES
	path('coaches/add/', views.coach_add, name='coach_add'),
	path('coaches/<int:pk>/edit/', views.coach_edit, name='coach_edit'),

	# GROUPS
	path('groups/add/', views.group_add, name='group_add'),
	path('groups/<int:pk>/edit/', views.group_edit, name='group_edit'),

	# SCHEDULES
	path('schedules/add/', views.schedule_add, name='schedule_add'),
	path('schedules/<int:pk>/edit/', views.schedule_edit, name='schedule_edit'),
 
	# DELETE ROUTES
	path('players/<int:pk>/delete/', views.player_delete, name='player_delete'),
	path('coaches/<int:pk>/delete/', views.coach_delete, name='coach_delete'),
	path('groups/<int:pk>/delete/', views.group_delete, name='group_delete'),
	path('schedules/<int:pk>/delete/', views.schedule_delete, name='schedule_delete'),


]
