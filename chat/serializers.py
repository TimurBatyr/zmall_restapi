from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated, AllowAny

from account.models import UserProfile
from chat.models import Message


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = UserProfile
        fields = ['email', 'password']


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.ReadOnlyField(source='sender.email')
    receiver = serializers.SlugRelatedField(many=False, slug_field='email', queryset=UserProfile.objects.all())

    # permission_classes = [IsAuthenticated, ]
    permission_classes = [AllowAny, ]

    class Meta:
        model = Message
        fields = '__all__'

    def create(self, validated_data):
        print(self.context['request'])
        request = self.context.get('request')
        sender = request.user
        validated_data['sender'] = sender
        return super().create(validated_data)
