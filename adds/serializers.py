from rest_framework import serializers

from .models import *


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('title', 'icon_image')


class Subscription(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['choice']


class SubscriptionSerializer(serializers.ModelSerializer):
    Subscription = Subscription(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ('title', 'from_price', 'image', 'subcategory', 'Subscription')


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('title', 'from_price', 'image', 'subscription')


class ImageSerializer(serializers.ModelSerializer):
    """Фотографии для товаров"""
    class Meta:
        model = PostImages
        fields = ('images',)



class PostCRUDSerializer(serializers.ModelSerializer):
    images = ImageSerializer(source='images.image', many=True, read_only=True)


    class Meta:
        model = Post
        fields = ('title', 'description', 'images')
        # exclude = ('user', 'status',)

    def create(self, validated_data):
        images_data = self.context.get('view').request.FILES
        task = Post.objects.create(title=validated_data.get('title', 'no-title'),
                                   user_id=1)
        for image_data in images_data.values():
            PostImages.objects.create(task=task, image=image_data)
        return task



# class DetailPostSerializer(serializers.ModelSerializer):
#     category = CategorySerializer
#
#     class Meta:
#         model = Post
#         fields = '__all__'
#
#     exclude = ('status',)


class NewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('title', 'from_price', 'image', 'subcategory', 'date_created')

class SearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields =('title','image','from_price','subcategory')