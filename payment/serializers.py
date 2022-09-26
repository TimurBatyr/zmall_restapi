from rest_framework import serializers

from .models import Payment
from zmall_restapi.adds.models import Post


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
        extra_kwargs = {
            "user": {"required": False}
        }

class PostSubscription(serializers.ModelSerializer):
    class Meta:
        model=Post
        fields = ('id','subscription')

