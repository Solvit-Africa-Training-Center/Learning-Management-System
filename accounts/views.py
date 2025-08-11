
from rest_framework import viewsets
from .models import CustomUser
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from .serializer import RegisterUserSerializer, AuthenticationSerializer
from django.contrib.auth import login, logout



# Create your views here.



class RegisterUserViewSet(viewsets.ModelViewSet):
    queryset=CustomUser.objects.all()
    serializer_class=RegisterUserSerializer
    def create(self, request):
        serializer=RegisterUserSerializer(data=request.data)
        if serializer.is_valid():
            user=serializer.save()
            return Response({'message': 'User created successfully'})
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


        },status=200)
