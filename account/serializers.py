from django.contrib import auth
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from adds.models import Post
from .utils import send_new_password, get_activation_code, send_activation_mail

User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(min_length=6, required=True)
    password_confirm = serializers.CharField(min_length=6, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password_confirm',)

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Email has already been taken')
        return email

    def validate(self, validated_data):
        password = validated_data.get('password')
        password_confirm = validated_data.pop('password_confirm')
        if password != password_confirm:
            raise serializers.ValidationError('Passwords do not match')
        return validated_data

    def save(self):
        data = self.validated_data
        user = User.objects.create_user(**data)
        activation_code = get_activation_code()
        user.activation_code = activation_code
        user.save(update_fields=['activation_code'])
        send_activation_mail(activation_code, user.email)


class ActivationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    activation_code = serializers.CharField(max_length=8,
                                            min_length=8)

    def validate(self, attrs):
        email = attrs.get('email')
        activation_code = attrs.get('activation_code')

        if not User.objects.filter(email=email,
                                   activation_code=activation_code).exists():
            raise serializers.ValidationError('User not found')
        return attrs

    def activate(self):
        email = self.validated_data.get('email')
        user = User.objects.get(email=email)
        user.is_active = True
        user.activation_code = ''
        user.save()


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(
        max_length=100, min_length=5, write_only=True)
    username = serializers.CharField(
        max_length=255, min_length=3, read_only=True)

    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = User.objects.get(email=obj['email'])

        return {
            'email': user.email,
            'username': user.username,
            'refresh': user.tokens()['refresh'],
            'access': user.tokens()['access']
        }

    class Meta:
        model = User
        fields = ['email', 'password', 'username', 'tokens']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        filtered_user_by_email = User.objects.filter(email=email)
        user = auth.authenticate(email=email, password=password)

        if filtered_user_by_email.exists() and filtered_user_by_email[0].auth_provider != 'email':
            raise AuthenticationFailed(
                detail='Please continue your login using ' + filtered_user_by_email[0].auth_provider)

        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')

        return {
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens
        }

        return super().validate(attrs)


class ChangePasswordSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=255, min_length=3, allow_blank=True)
    email = serializers.EmailField(allow_blank=True)
    phone = PhoneNumberField(allow_blank=True)
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    password_confirm = serializers.CharField(required=True)

    def validate_old_password(self, old_password):
        user = self.context['request'].user
        if not user.check_password(old_password):
            raise serializers.ValidationError('Type correct password')
        return old_password

    def validate(self, attrs):
         password = attrs.get('new_password')
         password_confirm = attrs.get('password_confirm')
         if password != password_confirm:
             raise serializers.ValidationError('Passwords do not match')
         return attrs

    def set_new_password(self):
         user = self.context['request'].user
         password = self.validated_data.get('new_password')
         user.set_password(password)
         user.save()


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('User not found')
        return email

    def create_new_password(self, email):

        user = User.objects.get(email=email)
        random_password = get_random_string(8)
        user.set_password(random_password)
        user.save()
        send_new_password(random_password, email)

