from rest_framework import serializers
from rest_framework.validators import ValidationError

from .models import *


class PostCreateSerializer(serializers.ModelSerializer):
    ''' Create Post '''
    user = serializers.SlugRelatedField(slug_field='email', queryset=UserProfile.objects.all())

    class Meta:
        model = Post
        exclude = ['status']


class PostImagesSerializer(serializers.ModelSerializer):
    ''' Create images for a post'''
    class Meta:
        model = PostImages
        fields = '__all__'

    def validate(self, attrs):
        if PostImages.objects.filter(post=attrs['post']).count() > 8:
            raise ValidationError('Number of images should not exceed 7')
        return attrs


class PostContactsSerializer(serializers.ModelSerializer):
    ''' Adding images for a post'''
    class Meta:
        model = PostContacts
        fields = '__all__'


class PostEditSerializer(serializers.ModelSerializer):
    ''' Editing(detail, delete, update) post'''
    class Meta:
        model = Post
        exclude = ['status']
        read_only_fields = ['user']


# class CategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Category
#         fields = ('title', 'icon_image')


#
# class PostSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Post
#         exclude = ('status', )
#
#
#
#
#
#
#
# class Subscription(serializers.ModelSerializer):
#     class Meta:
#         model = Subscription
#         fields = ['choice']
#
#
# class SubscriptionSerializer(serializers.ModelSerializer):
#     Subscription = Subscription(many=True, read_only=True)
#
#     class Meta:
#         model = Post
#         fields = ('title', 'from_price', 'image', 'subcategory', 'Subscription')
#
#
# class PostSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Post
#         fields = ('title', 'from_price', 'image', 'subscription')
#
#
# class ImageSerializer(serializers.ModelSerializer):
#     """Фотографии для товаров"""
#     class Meta:
#         model = PostImages
#         fields = ('image',)
#
#
#
# class NewSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Post
#         fields = ('title', 'from_price', 'image', 'subcategory', 'date_created')
#
# class SearchSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Post
#         fields =('title','image','from_price','subcategory')