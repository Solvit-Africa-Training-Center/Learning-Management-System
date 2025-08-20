from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from accounts.models import CustomUser, PasswordResetCode
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from datetime import timedelta

# ---------------------------
# Auth Tests
# ---------------------------

class AuthTest(APITestCase):
    def setUp(self):
        self.register_url = reverse("user-list")
        self.login_url = reverse("login-list")
        self.logout_url = reverse("logout-list")
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

        self.user = CustomUser.objects.create_user(
            first_name="mukunzi",
            last_name="innocent",
            username="mukunzi_innocent",
            email="existing@example.com",
            phone="0780000000",
            password="ngewe001@",
            role="Guest",
            is_verified=True
        )

    def test_user_registration(self):
        response = self.client.post(self.register_url, data=self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'], 'User created successfully')

    def test_login(self):
        login_response = self.client.post(self.login_url, {
            "username": "mukunzi_innocent",
            "password": "ngewe001@"
        }, format='json')
        refresh_token = login_response.data['refresh']
        response = self.client.post(self.logout_url, {
            "refresh": refresh_token
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)
        self.assertIn('message', response.data)

# ---------------------------
# Password Reset Tests
# ---------------------------

class PasswordResetFlowTest(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            first_name="Test",
            last_name="User",
            username="testuser2",
            email="test2@example.com",
            password="oldpassword123",
            is_verified=True
        )

        # Correct URL names
        self.forgot_url = reverse("forgot-password-list")
        self.verify_url = reverse("verify-code-list")
        self.reset_url = reverse("reset-password-list")
        self.login_url = reverse("login-list")

    # ---------- Forgot Password ----------
    def test_forgot_password_success(self):
        response = self.client.post(self.forgot_url, {"email": self.user.email}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("message", response.data)
        self.assertEqual(response.data["message"], "Verification code sent to email")
        self.assertTrue(PasswordResetCode.objects.filter(user=self.user).exists())

    def test_forgot_password_invalid_email(self):
        response = self.client.post(self.forgot_url, {"email": "wrong@example.com"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)

    # ---------- Verify Code ----------
    def test_verify_code_success(self):
        PasswordResetCode.objects.create(user=self.user, code="123456")
        response = self.client.post(self.verify_url, {"email": self.user.email, "code": "123456"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Code is valid")

    def test_verify_code_invalid_code(self):
        PasswordResetCode.objects.create(user=self.user, code="123456")
        response = self.client.post(self.verify_url, {"email": self.user.email, "code": "000000"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("non_field_errors", response.data)

    def test_verify_code_expired(self):
        code = PasswordResetCode.objects.create(user=self.user, code="123456")
        code.created_at = timezone.now() - timedelta(minutes=15)
        code.save()
        response = self.client.post(self.verify_url, {"email": self.user.email, "code": "123456"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("non_field_errors", response.data)

    # ---------- Reset Password ----------
    def test_reset_password_success(self):
        PasswordResetCode.objects.create(user=self.user, code="123456")
        response = self.client.post(self.reset_url, {
            "email": self.user.email,
            "code": "123456",
            "new_password": "newpassword123",
            "confirm_password": "newpassword123"
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Password reset successful")
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("newpassword123"))

    def test_reset_password_mismatch(self):
        PasswordResetCode.objects.create(user=self.user, code="123456")
        response = self.client.post(self.reset_url, {
            "email": self.user.email,
            "code": "123456",
            "new_password": "abc123",
            "confirm_password": "xyz456"
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("non_field_errors", response.data)

    def test_reset_password_expired_code(self):
        code = PasswordResetCode.objects.create(user=self.user, code="123456")
        code.created_at = timezone.now() - timedelta(minutes=15)
        code.save()
        response = self.client.post(self.reset_url, {
            "email": self.user.email,
            "code": "123456",
            "new_password": "newpassword123",
            "confirm_password": "newpassword123"
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("non_field_errors", response.data)

    # ---------- Full Flow Test ----------
    def test_full_password_reset_flow(self):
        # Step 1: Forgot Password
        forgot_resp = self.client.post(self.forgot_url, {"email": self.user.email}, format="json")
        self.assertEqual(forgot_resp.status_code, status.HTTP_200_OK)
        self.assertIn("message", forgot_resp.data)

        # Step 2: Get latest reset code
        code = PasswordResetCode.objects.filter(user=self.user).latest("created_at").code

        # Step 3: Verify Code
        verify_resp = self.client.post(self.verify_url, {"email": self.user.email, "code": code}, format="json")
        self.assertEqual(verify_resp.status_code, status.HTTP_200_OK)

        # Step 4: Reset Password
        reset_resp = self.client.post(self.reset_url, {
            "email": self.user.email,
            "code": code,
            "new_password": "finalpassword123",
            "confirm_password": "finalpassword123"
        }, format="json")
        self.assertEqual(reset_resp.status_code, status.HTTP_200_OK)

        # Step 5: Confirm password updated
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("finalpassword123"))
