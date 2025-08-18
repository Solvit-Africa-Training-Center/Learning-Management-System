
from rest_framework import viewsets, status
from .models import CustomUser
from api.models import StudentProgress
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializer import RegisterUserSerializer, AuthenticationSerializer, StudentProgressSerializer
from django.contrib.auth import login, logout
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework.views import APIView
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializer import RegisterUserSerializer,VerifyOtpSerizlizer





class RegisterUserViewSet(viewsets.ModelViewSet):
    queryset=CustomUser.objects.all()
    serializer_class=RegisterUserSerializer
    def create(self, request):
        serializer=RegisterUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            otp = user.generate_otp()
            send_mail(
                'OTP for registration',
                f'Your OTP is {otp}',
                'gihozoismail@gmail.com',
                [user.email],
                fail_silently=False,
            )
            return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=400)

class verifyOtpView(APIView):
    def post(self, request):
        serializer = VerifyOtpSerizlizer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = CustomUser.objects.get(email=email)
            user.is_active = True
            user.otp = None
            user.otp_expiry = None
            user.save()
            return Response({'message': 'OTP verified successfully'})
        return Response(serializer.errors, status=400)

class LoginViewSet(viewsets.GenericViewSet):
    queryset = CustomUser.objects.none()
    permission_classes = [AllowAny]
    serializer_class = AuthenticationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        # if not user.
        login(request, user)
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'message': 'Login successful',
            'you logged in as': str(user),
        }, status=200)

class LogoutViewSet(viewsets.GenericViewSet):
    permission_classes = [AllowAny]

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

class StudentProgressViewSet(viewsets.ModelViewSet):
    queryset = StudentProgress.objects.all()
    serializer_class = StudentProgressSerializer
    permission_classes = [IsAuthenticated]
