from rest_framework import serializers
from django.contrib.auth.models import User
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
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    profile_completed = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Player
        fields = ['id', 'user', 'username', 'email', 'name', 'age', 'position', 'photo', 'group', 'group_name', 
                  'status', 'registered_at', 'approved_at', 'approved_by', 'profile_completed']
        read_only_fields = ['status', 'registered_at', 'approved_at', 'approved_by', 'profile_completed']


class CompleteProfileSerializer(serializers.ModelSerializer):
    """Serializer untuk melengkapi profil player setelah approved"""
    
    class Meta:
        model = Player
        fields = ['name', 'age', 'position', 'photo']
    
    def validate_name(self, value):
        if not value:
            raise serializers.ValidationError("Nama harus diisi")
        return value
    
    def validate_age(self, value):
        if not value or value < 5 or value > 50:
            raise serializers.ValidationError("Umur harus antara 5-50 tahun")
        return value
    
    def validate_position(self, value):
        if not value:
            raise serializers.ValidationError("Posisi harus diisi")
        return value

class TrainingScheduleSerializer(serializers.ModelSerializer):
    group_name = serializers.CharField(source='group.name', read_only=True, allow_null=True)
    
    class Meta:
        model = TrainingSchedule
        fields = "__all__"


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer untuk registrasi user baru dengan profil lengkap"""
    password = serializers.CharField(write_only=True, min_length=6)
    password_confirm = serializers.CharField(write_only=True)
    name = serializers.CharField(required=True)
    age = serializers.IntegerField(required=True)
    position = serializers.CharField(required=True)
    photo = serializers.ImageField(required=False, allow_null=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm', 'name', 'age', 'position', 'photo']
    
    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError("Email diperlukan untuk notifikasi")
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email sudah terdaftar")
        return value
    
    def validate_age(self, value):
        if value < 5 or value > 50:
            raise serializers.ValidationError("Umur harus antara 5-50 tahun")
        return value
    
    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({"password": "Password tidak cocok"})
        return data
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        
        # Extract player fields
        name = validated_data.pop('name')
        age = validated_data.pop('age')
        position = validated_data.pop('position')
        photo = validated_data.pop('photo', None)
        
        # Create user
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        
        # Create player with complete profile in PENDING status
        Player.objects.create(
            user=user,
            name=name,
            age=age,
            position=position,
            photo=photo,
            status=Player.STATUS_PENDING
        )
        
        return user
