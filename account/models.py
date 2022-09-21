from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from rest_framework_simplejwt.tokens import RefreshToken


class UserManager(BaseUserManager):
    def _create(self, email, password, **kwargs):
        if not email:
            raise ValueError('Укажите почту')
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, password, **kwargs):
        kwargs.setdefault('is_active', False)
        kwargs.setdefault('is_staff', False)
        kwargs.setdefault('is_superuser', False)
        return self._create(email, password, **kwargs)

    def create_superuser(self, email, password, **kwargs):
        kwargs.setdefault('is_active', True)
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        return self._create(email, password, **kwargs)


AUTH_PROVIDERS = {'facebook': 'facebook', 'google': 'google', 'email': 'email'}


class User(AbstractUser):
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    username = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = PhoneNumberField(blank=True)
    auth_provider = models.CharField(
        max_length=255, blank=False,
        null=False, default=AUTH_PROVIDERS.get('email'))

    activation_code = models.CharField(max_length=8, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
