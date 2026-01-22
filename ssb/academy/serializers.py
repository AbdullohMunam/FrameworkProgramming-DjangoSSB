from rest_framework import serializers
from .models import Coach, Group, Player, TrainingSchedule

class CoachSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coach
        fields = "__all__"

class GroupSerializer(serializers.ModelSerializer):
    coach_name = serializers.CharField(source='coach.name', read_only=True, allow_null=True)
    
    class Meta:
        model = Group
        fields = "__all__"

class PlayerSerializer(serializers.ModelSerializer):
    group_name = serializers.CharField(source='group.name', read_only=True, allow_null=True)
    
    class Meta:
        model = Player
        fields = "__all__"

class TrainingScheduleSerializer(serializers.ModelSerializer):
    group_name = serializers.CharField(source='group.name', read_only=True, allow_null=True)
    
    class Meta:
        model = TrainingSchedule
        fields = "__all__"
