from account.models import User
from adds import serializers
from adds.models import Category, Subcategory, City, Subscription, PostImages, PostContacts, Post, ReviewPost, Views, \
    Favorite
from chat.models import Message


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    '''List of categories'''
    class Meta:
        model = Category
        fields = '__all__'


class SubcategorySerializer(serializers.ModelSerializer):
    '''List of subcategories'''
    class Meta:
        model = Subcategory
        fields = '__all__'


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


class PostImagesSerializer(serializers.ModelSerializer):
    ''' Create images for a post'''
    class Meta:
        model = PostImages
        fields = "__all__"


class PostContactsSerializer(serializers.ModelSerializer):
    ''' Adding images for a post'''
    class Meta:
        model = PostContacts
        fields = "__all__"


class PostSerializer(serializers.ModelSerializer):
    ''' Create Post '''
    class Meta:
        model = Post
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    '''Display reviews'''
    class Meta:
        model = ReviewPost
        fields = "__all__"


class ViewsSerializer(serializers.ModelSerializer):
    '''Display reviews'''
    class Meta:
        model = Views
        fields = "__all__"


class FavoriteSerializer(serializers.ModelSerializer):
    '''Display reviews'''
    class Meta:
        model = Favorite
        fields = "__all__"


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = '__all__'