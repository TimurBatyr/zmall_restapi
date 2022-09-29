from rest_framework import serializers

from .models import StoreTarsaction
from adds.models import Post


class PostSubscription(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'subscription')


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreTarsaction
        fields = ('type_adverments', 'title', 'date', 'price')