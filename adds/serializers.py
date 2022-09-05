from rest_framework import serializers
from rest_framework.validators import ValidationError

from .models import *


class CategorySerializer(serializers.ModelSerializer):
    '''List of categories'''
    class Meta:
        model = Category
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['count_category_posts'] = Post.objects.filter(category=instance).count()
        return representation


class SubcategorySerializer(serializers.ModelSerializer):
    '''List of subcategories'''
    class Meta:
        model = Subcategory
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['count_subcategory_posts'] = Post.objects.filter(subcategory=instance).count()
        return representation


class CitySerializer(serializers.ModelSerializer):
    '''List of cities'''
    class Meta:
        model = City
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):
    '''List of subscriptions'''
    class Meta:
        model = Subscription
        fields = ['choice', 'price']


class PostImagesSerializer(serializers.ModelSerializer):
    ''' Create images for a post'''
    class Meta:
        model = PostImages
        fields = "__all__"

    def validate(self, attrs):
        if PostImages.objects.filter(post=attrs['post']).count() > 8:
            raise ValidationError('Number of images should not exceed 7')
        return attrs


class PostContactsSerializer(serializers.ModelSerializer):
    ''' Adding images for a post'''
    class Meta:
        model = PostContacts
        fields = "__all__"


class PostCreateSerializer(serializers.ModelSerializer):
    ''' Create Post '''
    user = serializers.SlugRelatedField(slug_field='email', queryset=UserProfile.objects.all())

    class Meta:
        model = Post
        fields = ('user', 'category', 'subcategory', 'city', 'subscription', 'title', 'description',
                  'from_price', 'to_price', 'image', 'email', 'phone_number', 'wa_number',
                  'is_activated')


class FilterReviewListSerializer(serializers.ListSerializer):
    '''Review filter, only parents'''
    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)


class ReviewRecursiveSerializer(serializers.Serializer):
    '''Display recursive children'''
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class ReviewCreateSerializer(serializers.ModelSerializer):
    '''Create review to the post'''
    class Meta:
        model = ReviewPost
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    '''Display reviews'''
    children = ReviewRecursiveSerializer(many=True)
    class Meta:
        list_serializer_class = FilterReviewListSerializer
        model = ReviewPost
        fields = ('id', 'title', 'text', 'children')


class PostEditSerializer(serializers.ModelSerializer):
    ''' Editing(detail, delete, update(just for post) post'''
    images = PostImagesSerializer(many=True)
    phone = PostContactsSerializer(many=True)
    subscription = SubscriptionSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True)


    class Meta:
        model = Post
        fields = ('id', 'user', 'category', 'subcategory', 'city', 'subscription', 'title', 'description',
                  'from_price', 'to_price', 'image', 'images', 'email', 'phone_number', 'wa_number', 'phone',
                  'is_activated', 'reviews')
        read_only_fields = ['user']


class PostListSerializer(serializers.ModelSerializer):
    ''' List of posts'''
    subscription = SubscriptionSerializer(many=True, read_only=True)
    class Meta:
        model = Post
        fields = ('title', 'subscription', 'from_price', 'subcategory', 'image')


# class AddPostSerializer(serializers.ModelSerializer):
#     '''Watches of posts'''
#     images = serializers.StringRelatedField(many=True)
#
#     class Meta:
#         model = Post
#         fields = ('id', 'category', 'subcategory',
#                   'title', 'from_price', 'to_price',
#                   'description', 'images', 'city',
#                   'email', 'phone_number','views'
#                   )
