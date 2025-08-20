from  django.urls import path,include
from .views import RegisterUserViewSet,LoginViewSet, LogoutViewSet , StudentProgressViewSet

from .views import RegisterUserViewSet,verifyOtpView
from rest_framework import routers
from .views import StudentProgressViewSet

router=routers.DefaultRouter()
router.register("user",RegisterUserViewSet,basename="user")
router.register("login",LoginViewSet,basename="login")
router.register('logout', LogoutViewSet, basename='logout')
router.register(r'student-progress', StudentProgressViewSet, basename='student-progress')

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("",include(router.urls)),

    path("verify-otp/",verifyOtpView.as_view(), name="verify-otp"),
]