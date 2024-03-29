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
        representation['count_category_posts'] = Post.objects.filter(category=instance, is_activated=True).count()
        return representation


class SubcategorySerializer(serializers.ModelSerializer):
    '''List of subcategories'''
    class Meta:
        model = Subcategory
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['count_subcategory_posts'] = Post.objects.filter(subcategory=instance, is_activated=True).count()
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
        fields = '__all__'


class PostCreateSerializer(serializers.ModelSerializer):
    ''' Create Post '''
    user = serializers.SlugRelatedField(slug_field='email', queryset=User.objects.all())

    class Meta:
        model = Post
        fields = ('id', 'user', 'category', 'subcategory', 'city', 'subscription', 'title', 'description',
                  'from_price', 'to_price', 'image', 'email', 'phone_number', 'wa_number',
                  'is_activated')


class PostImagesSerializer(serializers.ModelSerializer):
    ''' Create images for a post'''
    class Meta:
        model = PostImages
        fields = "__all__"


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostContacts
        fields = "__all__"

    # def create(self, validated_data):
    #     return PostContacts.objects.create(**validated_data)


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
        model = ReviewPost
        fields = ('id', 'text', 'children', 'email')


class FavoriteSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')
    post_title = serializers.ReadOnlyField(source='post.title')
    post_price = serializers.ReadOnlyField(source='post.from_price')

    class Meta:
        model = Favorite
        fields = ['id', 'user', 'post', 'favorites', 'post_title', 'post_price']

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        post = validated_data.get('post')
        favorite= Favorite.objects.get_or_create(user=user, post=post)[0]
        favorite.favorites = True if favorite.favorites is False else False
        favorite.save()
        return favorite


# class PostEditSerializer(serializers.ModelSerializer):
#     ''' Editing(detail, delete, update(just for post) post'''
#     images = PostImagesSerializer(many=True)
#     # phone = ContactSerializer(many=True)
#     subscription = SubscriptionSerializer(read_only=True)
#     reviews = ReviewSerializer(many=True, read_only=True)
#     user_email = serializers.ReadOnlyField(source='user.email')
#     user_username = serializers.ReadOnlyField(source='user.username')
#
#
#     class Meta:
#         model = Post
#         fields = ('id', 'user_email', 'user_username', 'category', 'subcategory', 'city', 'subscription', 'title',
#                   'description', 'from_price', 'to_price', 'image', 'images', 'email', 'phone_number', 'wa_number',
#                   'is_activated', 'reviews', 'date_created', 'status')

class PostEditSerializer(serializers.ModelSerializer):
    ''' Editing(detail, delete, update(just for post) post'''
    images = PostImagesSerializer(many=True)
    subscription = SubscriptionSerializer(read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    user_email = serializers.ReadOnlyField(source='user.email')
    user_username = serializers.ReadOnlyField(source='user.username')
    views = serializers.IntegerField(read_only=True)
    class Meta:
        model = Post
        fields = ('id', 'user_email', 'user_username', 'category', 'subcategory', 'city', 'subscription', 'title',
                  'description', 'from_price', 'to_price', 'image', 'images', 'email', 'phone_number', 'wa_number',
                  'is_activated', 'reviews', 'date_created', 'status', 'views')


class PostDetailSerializer(serializers.ModelSerializer):
    ''' Editing(detail, delete, update(just for post) post'''

    class Meta:
        model = Post
        fields = fields = ('id', 'user', 'category', 'subcategory', 'city', 'subscription', 'title', 'description',
                           'from_price', 'to_price', 'email', 'phone_number', 'wa_number',
                           'is_activated', 'date_created')
        # read_only_fields = ['user']


class PostListSerializer(serializers.ModelSerializer):
    ''' List of posts'''
    subscription = SubscriptionSerializer(read_only=True)
    city = CitySerializer(read_only=True)
    class Meta:
        model = Post
        fields = ('id', 'title', 'subscription', 'from_price', 'subcategory', 'category', 'image',
                  'description', 'date_created', 'city', 'is_activated', 'status')


class PostComplaintSerializer(serializers.ModelSerializer):
    '''List complaints'''
    class Meta:
        model = PostComplaint
        fields = '__all__'


#Views
class ViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Views
        fields = ['date', 'views']



# Статистика просмотров
class StatisticsPostSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['views']


class ContactViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ViewsContact
        fields = ['views']


class StatisticsViewSerializer(serializers.ModelSerializer):
    view_contact = ContactViewSerializer(many=True,read_only=True)
    class Meta:
        model = Views
        fields = ['views', 'date', 'view_contact']


class StaticsNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostContacts
        fields = ['view']


class TodaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Views
        fields =['views', 'date']


