import os

from decouple import config
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from social_auth import google, facebook
from social_auth.register import register_social_user


class GoogleSocialAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):

        user_data = google.Google.validate(auth_token)
        try:
            user_data["sub"]
        except:
            raise serializers.ValidationError(
                "The token is invalid or expired. Please login again."
            )

        if user_data["aud"] != config("GOOGLE_CLIENT_ID"):

            raise AuthenticationFailed("oops, who are you?")

        email = user_data["email"]
        provider = "google"
        return register_social_user(provider=provider, email=email, user=user_data)


class FacebookSocialAuthSerializer(serializers.Serializer):
    """Handles serialization of facebook related data"""
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        user_data = facebook.Facebook.validate(auth_token)

        try:
            email = user_data['email']
            name = user_data['name']
            provider = 'facebook'
            return register_social_user(
                provider=provider,
                email=email,
                name=name
            )
        except Exception as identifier:

            raise serializers.ValidationError(
                'The token  is invalid or expired. Please login again.'
            )