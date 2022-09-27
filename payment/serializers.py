from rest_framework import serializers

from .models import Payment, StoreTarsaction
from adds.models import Post



class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'subscription'
        ]

class PaymentSerializer(serializers.ModelSerializer):
    post_payment= PostSerializer(many=True, read_only=True)
    class Meta:
        model = Payment
        fields = ('user','amount','description','salt','post_payment')
        extra_kwargs = {
            "user": {"required": False}
        }

class PostSubscription(serializers.ModelSerializer):
    class Meta:
        model=Post
        fields = ('id','subscription')

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model=StoreTarsaction
        fields = ('type_adverments','title','date','price')