from rest_framework import serializers


from django.contrib.auth import  authenticate

from django.utils import timezone

from accounts.models import CustomUser
from api.models import StudentProgress
from rest_framework import serializers
from django.contrib.auth import authenticate
from accounts.models import CustomUser, PasswordResetCode
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
import random
from django.core.mail import send_mail


class RegisterUserSerializer(serializers.ModelSerializer):
    first_name=serializers.CharField(required=True)
    username=serializers.CharField(required=True)
    last_name=serializers.CharField(required=True)
    phone=serializers.CharField(required=True)
    email=serializers.EmailField(required=True)
    password=serializers.CharField(required=True, write_only=True)
    re_type_password=serializers.CharField(required=True, write_only=True)
    class Meta:
        model=CustomUser
        fields=["first_name","username","last_name","email","phone","password","re_type_password","role"]
        extra_kwargs={
            "password": {"write_only": True},
            "re_type_password": {"write_only": True},
            "role": {"required": False}
        }

    def validate(self,data):
        if   data["password"]!=data["re_type_password"]   :
            raise serializers.ValidationError("Passwords do not match")
        return data
    def create(self, validated_data):
        user=CustomUser.objects.create_user(
            username=validated_data["username"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            email=validated_data["email"],
            phone=validated_data["phone"],
            password=validated_data["password"],
            role=validated_data.get("role", "Guest")
        )
        return user

class AuthenticationSerializer(serializers.ModelSerializer):
    username=serializers.CharField(required=True)
    password=serializers.CharField(required=True, write_only=True)


    class Meta:
        model=CustomUser
        fields=["username","password"]

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            raise serializers.ValidationError("All fields are required") 
        else:
            user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError("invalid username or password")
        data["user"] = user
        return data

class StudentProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProgress
        fields = "__all__"

     


    




class VerifyOtpSerizlizer(serializers.Serializer):
    
    email=serializers.EmailField()
    otp=serializers.CharField(max_length=6)



    def validate(self,data):
        email=data.get("email")
        otp=data.get("otp")
        try:
            user=CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
               raise serializers.ValidationError("User with this email does not exist")
        if user.otp !=otp:
            raise serializers.ValidationError("Invalid OTP")
        if user.otp_expiry and user.otp_expiry<timezone.now():
            raise serializers.ValidationError("OTP has expired")
        
        user.is_verified=True
        user.save()
        return data
class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("No user with this email found.")
        return value

    def save(self):
        user = CustomUser.objects.filter(email=self.validated_data["email"]).first()
        if not user:
            # This should never happen because of validation, but safe to check
            raise serializers.ValidationError("User not found.")

        code = str(random.randint(100000, 999999))  # Generate a 6-digit code
        PasswordResetCode.objects.create(user=user, code=code)

        # Send code to user's email (here we just print it for testing)
        print(f"Password reset code for {user.username}: {code}")

        send_mail(
            subject="Your Password Reset Code",
            message=f"Hello {user.username}, your password reset code is: {code}",
            from_email="gihozoismail@gmail.com",
            recipient_list=[user.email],
            fail_silently=False,
        )

        return user

class VerifyCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)

    def validate(self, data):
        user = CustomUser.objects.filter(email=data["email"]).first()  # ✅ fixed
        if not user:
            raise serializers.ValidationError("No user with this email found.")

        reset_code = PasswordResetCode.objects.filter(user=user, code=data["code"]).first()
        if not reset_code:
            raise serializers.ValidationError("Invalid or expired code.")

        if reset_code.created_at < timezone.now() - timedelta(minutes=10):
            raise serializers.ValidationError("Code has expired.")

        data["user"] = user
        return data



class ResetPasswordSerializer(serializers.Serializer):  # ✅ fixed name
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        if data["new_password"] != data["confirm_password"]:
            raise serializers.ValidationError("Passwords do not match")

        try:
            user = CustomUser.objects.get(email=data["email"])
            reset_code = PasswordResetCode.objects.filter(user=user, code=data["code"]).latest("created_at")
        except (CustomUser.DoesNotExist, PasswordResetCode.DoesNotExist):
            raise serializers.ValidationError("Invalid request")

        if timezone.now() > reset_code.created_at + timedelta(minutes=10):
            raise serializers.ValidationError("Code expired")

        data["user"] = user
        return data

    def save(self):
        user = self.validated_data["user"]
        user.password = make_password(self.validated_data["new_password"])
        user.save()
        
        return user

