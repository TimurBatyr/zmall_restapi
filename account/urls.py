from django.urls import path, include

from .views import RegistrationAPIView, ActivateView, ForgotPasswordView, ChangePasswordView, LoginAPIView, UserView, \
    UserAccount
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('register/', RegistrationAPIView.as_view(), name="register"),
    path('login/', LoginAPIView.as_view(), name="login"),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('activate/', ActivateView.as_view(), name="activate"),
    path('userview/<int:pk>/', UserView.as_view(), name='userview'),
    path('userdetail/', UserAccount.as_view(), name='userdetail'),
    path('change_password/', ChangePasswordView.as_view(), name="change-password"),
    path('forgot_password/', ForgotPasswordView.as_view(), name="forgot-password"),

]