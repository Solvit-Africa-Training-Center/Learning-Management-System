
from rest_framework import viewsets
from .models import CustomUser
from rest_framework.views import APIView
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializer import RegisterUserSerializer,VerifyOtpSerizlizer




# Create your views here.



class RegisterUserViewSet(viewsets.ModelViewSet):
    queryset=CustomUser.objects.all()
    serializer_class=RegisterUserSerializer
    def create(self, request):
        serializer=RegisterUserSerializer(data=request.data)
        if serializer.is_valid():
            user=serializer.save()
            otp=user.generate_otp()
            send_mail(
                'OTP for registration',
                f'Your OTP is {otp}',
                'gihozoismail@gmail.com',
                [user.email],
                fail_silently=False,
            )


            return Response({'message': 'User created successfully'})
        return Response(serializer.errors, status=400)



class verifyOtpView(APIView):
    def post(self,request):
        serializer=VerifyOtpSerizlizer(data=request.data)
        if serializer.is_valid():
            email=serializer.validated_data['email']
            user=CustomUser.objects.get(email=email)
            user.is_active = True
            user.otp = None
            user.otp_expiry = None
            user.save()
            return Response({'message': 'OTP verified successfully'})
        return Response(serializer.errors, status=400)