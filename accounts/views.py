
from rest_framework import viewsets, status
from .models import CustomUser
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import RegisterUserSerializer, AuthenticationSerializer
from django.contrib.auth import login, logout
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import ForgotPasswordSerializer, VerifyCodeSerializer, ResetPasswordSerializer









class RegisterUserViewSet(viewsets.ModelViewSet):
    queryset=CustomUser.objects.all()
    serializer_class=RegisterUserSerializer
    def create(self, request):
        serializer=RegisterUserSerializer(data=request.data)
        if serializer.is_valid():
            user=serializer.save()
            return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=400)

class LoginViewSet(viewsets.GenericViewSet):
    queryset = CustomUser.objects.none()
    permission_classes = [AllowAny]
    serializer_class = AuthenticationSerializer

    def create(self, request, *args, **kwargs):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user=serializer.validated_data['user']
        login(request, user)
        refresh = RefreshToken.for_user(user)
        return Response({

            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'message': 'Login successful',
            'you logged in as': str(user),


        },status=200)

class LogoutViewSet(viewsets.GenericViewSet):
    permission_classes=[AllowAny]

    def create(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logout successful"}, status=status.HTTP_205_RESET_CONTENT)
        except KeyError:
            return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)
        except (TokenError, InvalidToken):
            return Response({"error": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)

class ForgotPasswordViewSet(viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    serializer_class = ForgotPasswordSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Verification code sent to email"}, status=200)



class VerifyCodeViewSet(viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    serializer_class = VerifyCodeSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"message": "Code is valid"}, status=200)


class ResetPasswordViewSet(viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    serializer_class = ResetPasswordSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Password reset successful"}, status=200)