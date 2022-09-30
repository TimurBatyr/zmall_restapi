import google
from google.oauth2 import id_token
from google.auth.transport import requests
from decouple import config

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from account.models import User
from social_auth.serializers import GoogleSocialAuthSerializer, FacebookSocialAuthSerializer


class GoogleSocialAuthView(GenericAPIView):

    serializer_class = GoogleSocialAuthSerializer

    def post(self, request):
        """
        POST with "auth_token"
        Send an idtoken as from google to get user information
        """
        user = id_token.verify_oauth2_token(
            request.data["auth_token"], requests.Request(), config("GOOGLE_CLIENT_ID")
        )
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = (serializer.validated_data)["auth_token"]
        user_by_email = User.objects.get(email=data["email"])
        tokens = user_by_email.tokens()

        data = {
            "email": user_by_email.email,
            "username": user_by_email.username,
            "user_id": user_by_email.id,
            "phone": user_by_email.phone,
            "tokens": tokens,
        }
        print(data)
        return Response(data, status=status.HTTP_200_OK)


class FacebookSocialAuthView(GenericAPIView):

    serializer_class = FacebookSocialAuthSerializer

    def post(self, request):


        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = ((serializer.validated_data)['auth_token'])
        return Response(data, status=status.HTTP_200_OK)