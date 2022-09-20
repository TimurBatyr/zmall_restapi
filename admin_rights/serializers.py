from rest_framework import serializers

from account.models import User
from adds.models import Category, Subcategory, City, Subscription, PostImages, PostContacts, Post, ReviewPost, Views, \
    Favorite, PostComplaint
from chat.models import Message


class UserDetailSerializerAd(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class CategorySerializerAd(serializers.ModelSerializer):
    '''List of categories'''
    class Meta:
        model = Category
        fields = '__all__'


class SubcategorySerializerAd(serializers.ModelSerializer):
    '''List of subcategories'''
    class Meta:
        model = Subcategory
        fields = '__all__'


class CitySerializerAd(serializers.ModelSerializer):
    '''List of cities'''
    class Meta:
        model = City
        fields = '__all__'


class SubscriptionSerializerAd(serializers.ModelSerializer):
    '''List of subscriptions'''
    class Meta:
        model = Subscription
        fields = '__all__'


class PostImagesSerializerAd(serializers.ModelSerializer):
    ''' Create images for a post'''
    class Meta:
        model = PostImages
        fields = "__all__"


class PostContactsSerializerAd(serializers.ModelSerializer):
    ''' Adding images for a post'''
    class Meta:
        model = PostContacts
        fields = "__all__"


class PostSerializerAd(serializers.ModelSerializer):
    ''' Create Post '''
    class Meta:
        model = Post
        fields = "__all__"


class ReviewSerializerAd(serializers.ModelSerializer):
    '''Display reviews'''
    class Meta:
        model = ReviewPost
        fields = "__all__"


class ViewsSerializerAd(serializers.ModelSerializer):
    '''Display reviews'''
    class Meta:
        model = Views
        fields = "__all__"


class FavoriteSerializerAd(serializers.ModelSerializer):
    '''Display reviews'''
    class Meta:
        model = Favorite
        fields = "__all__"


class MessageSerializerAd(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = '__all__'


class PostComplaintSerializerAd(serializers.ModelSerializer):
    '''List complaints'''
    class Meta:
        model = PostComplaint
        fields = '__all__'