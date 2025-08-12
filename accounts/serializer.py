from rest_framework import serializers

from django.contrib.auth import  authenticate
from accounts.models import CustomUser



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

        


    
