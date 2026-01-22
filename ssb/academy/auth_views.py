"""
Authentication Views untuk Token-based Authentication
Menyediakan endpoint untuk login dan logout
"""

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


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
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username,
            'email': user.email,
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
