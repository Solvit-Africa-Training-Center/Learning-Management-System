
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from accounts.models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken

# Create your tests here.


class AuthTest(APITestCase):
    def setUp(self):
        self.register_url=reverse("user-list")
        self.login_url=reverse("login-list")
        self.logout_url=reverse("logout-list")
        self.user_data = {
        "first_name": "Test",
        "last_name": "User",
        "username": "testuser",
        "phone": "0780000000",  
        "email": "test@example.com",
        "password": "testpassword",
        "re_type_password": "testpassword",
        "role": "Guest"
}

        self.user=CustomUser.objects.create_user(
            first_name="mukunzi",
            last_name="innocent",
            username="mukunzi_innocent",
            email="existing@example.com",
            phone="0780000000",
            password="ngewe001@",
            role="Guest"

        )
    def test_user_registration(self):
        response = self.client.post(self.register_url, data=self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'], 'User created successfully')



    def test_login(self):
        login_response=self.client.post(self.login_url,{
            "username":"mukunzi_innocent",
            "password":"ngewe001@"
        },format='json')
        refresh_token=login_response.data['refresh']
        response=self.client.post(self.logout_url,{
            "refresh": refresh_token
        },format='json')
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)
        self.assertIn('message',response.data)