
from rest_framework import viewsets
from .models import CustomUser
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializer import RegisterUserSerializer




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