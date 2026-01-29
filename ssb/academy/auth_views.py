"""
Authentication Views untuk Token-based Authentication
Menyediakan endpoint untuk login, logout, dan register
"""

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from .serializers import RegisterSerializer


@method_decorator(csrf_exempt, name='dispatch')
class LoginView(ObtainAuthToken):
    """
    POST /api/auth/login/
    Body: {
        "username": "admin",
        "password": "password123"
    }
    Response: {
        "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
        "user_id": 1,
        "username": "admin",
        "email": "admin@example.com"
    }
    """
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        
        # Check if user is admin
        if not (user.is_staff or user.is_superuser):
            # Check if user has player profile and is approved
            try:
                player = user.player
                if player.status != 'approved':
                    return Response({
                        'detail': 'Pendaftaran Anda sedang menunggu approval admin. Cek email untuk update.'
                    }, status=status.HTTP_403_FORBIDDEN)
            except:
                return Response({
                    'detail': 'No player profile found'
                }, status=status.HTTP_403_FORBIDDEN)
        
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username,
            'email': user.email,
            'is_staff': user.is_staff,
            'is_superuser': user.is_superuser,
            'message': 'Login successful'
        })


class LogoutView(APIView):
    """
    POST /api/auth/logout/
    Headers: Authorization: Token <your_token_here>
    Response: {
        "message": "Successfully logged out"
    }
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        # Hapus token user yang sedang login
        request.user.auth_token.delete()
        return Response({
            'message': 'Successfully logged out'
        }, status=status.HTTP_200_OK)


class UserProfileView(APIView):
    """
    GET /api/auth/profile/
    Headers: Authorization: Token <your_token_here>
    Response: {
        "id": 1,
        "username": "admin",
        "email": "admin@example.com",
        "first_name": "Admin",
        "last_name": "User"
    }
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
        })


@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(APIView):
    """
    POST /api/auth/register/
    Body: {
        "username": "user1",
        "email": "user1@example.com",
        "password": "password123",
        "password_confirm": "password123",
        "name": "John Doe",
        "age": 18,
        "position": "Forward",
        "photo": <file> (optional)
    }
    Response: {
        "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
        "user_id": 1,
        "username": "user1",
        "message": "Registration successful"
    }
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        print("=== REGISTER REQUEST DATA ===")
        print(request.data)
        
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # Send email notification to admin (will be handled by signal)
            
            return Response({
                'message': 'Pendaftaran berhasil! Menunggu approval dari admin. Cek email Anda untuk update status.',
                'username': user.username,
                'email': user.email
            }, status=status.HTTP_201_CREATED)
        
        print("=== VALIDATION ERRORS ===")
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
