from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated, AllowAny

from account.models import UserProfile
from chat.models import Message


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = '__all__'


    def create(self, validated_data):
        message = Message.objects.create(**validated_data)
        message.save()
        self.message = message
        return message
