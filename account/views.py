import datetime

import jwt
from django.conf import settings
from django.contrib import auth
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .serializers import RegistrationSerializer, ActivationSerializer, ForgotPasswordSerializer, \
    ChangePasswordSerializer, LoginSerializer, UserDetailSerializer


class RegistrationAPIView(generics.GenericAPIView):

    serializer_class = RegistrationSerializer
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('Успешно зарегистрирован. Проверьте свою электронную почту, чтобы подтвердить', status=status.HTTP_201_CREATED)


class ActivateView(generics.GenericAPIView):

    serializer_class = ActivationSerializer
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.activate()
        return Response('Ваш аккаунт успешно активирован!', status=status.HTTP_200_OK)


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        data = request.data
        serializer = ChangePasswordSerializer(data=data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.set_new_password()
            return Response('Вы успешно обновили свой учетные данные')


class ForgotPasswordView(APIView):
    def post(self, request):
        data = request.data
        serializer = ForgotPasswordSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.create_new_password(serializer.data['email'])
        return Response('Новый пароль отправлен на вашу электронную почту')


class UserView(generics.RetrieveAPIView):
    serializer_class = UserDetailSerializer
    queryset = User.objects.all()


class UserAccount(generics.GenericAPIView):
    serializer_class = UserDetailSerializer
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        user = User.objects.get(pk=self.request.user.id)
        serializer = UserDetailSerializer(user)
        if user:
            return Response(serializer.data)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def patch(self, request):
        user = User.objects.get(pk=self.request.user.id)
        serializer = UserDetailSerializer(user, data=request.data)
        if user and serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        user = User.objects.get(pk=self.request.user.id)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# """"Эта вьюшка используется для логина с JWT"""
# class LoginAPIView(generics.GenericAPIView):
#     serializer_class = LoginSerializer
#
#     def post(self, request):
#         data = request.data
#         email = data.get('email', '')
#         password = data.get('password', '')
#         user = auth.authenticate(email=email, password=password)
#         # print(user.email)
#         # print(type(user.email))
#         # print(settings.JWT_SECRET_KEY)
#         if user:
#             auth_token = jwt.encode(
#                 {"email": str(user.email),
#                  'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=30)},
#                 settings.JWT_SECRET_KEY, algorithm="HS256")
#             print(auth_token)
#
#             serializer = LoginSerializer(user)
#
#             data = {'user': serializer.data, 'token': auth_token}
#
#             return Response(data, status=status.HTTP_200_OK)
#
#         return Response({'detail': 'Неправильные данные'}, status=status.HTTP_401_UNAUTHORIZED)