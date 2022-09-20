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

    def validate(self, attrs,pk):
        # post=PostImages.objects.filter(post=pk).values('pk')
        # post=Post.objects.get(pk=post[0]['pk'])
        if PostImages.objects.filter(post='post.id').count() > 8:
            raise ValidationError('Number of images should not exceed 7')
        return attrs


# class AdsImage(models.Model):
#     image = CloudinaryField('Фотография')
#     advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE, verbose_name='Объявление',
#                                       help_text='Объявления с фото получают в среднем в 3-5 раз больше '
#                                                 'откликов. Вы можете загрузить до 8 фотографий',
#                                       related_name='images')
#
#     def __str__(self):
#         return self.image.url
#
#     class Meta:
#         verbose_name = 'Изображение объявления'
#         verbose_name_plural = 'Изображения объявлений'



class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostContacts
        fields = "__all__"


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
        fields = ('id', 'title', 'text', 'children', 'email')


class FavoriteSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = Favorite
        fields = ['id', 'post', 'user']



class PostEditSerializer(serializers.ModelSerializer):
    ''' Editing(detail, delete, update(just for post) post'''
    images = PostImagesSerializer(many=True)
    phone = ContactSerializer(many=True)
    subscription = SubscriptionSerializer(read_only=True)
    reviews = ReviewSerializer(many=True)
    user_email = serializers.ReadOnlyField(source='user.email')
    user_username = serializers.ReadOnlyField(source='user.username')


    class Meta:
        model = Post
        fields = ('id', 'user_email', 'user_username', 'category', 'subcategory', 'city', 'subscription', 'title', 'description',
                  'from_price', 'to_price', 'image', 'images', 'email', 'phone_number', 'wa_number', 'phone',
                  'is_activated', 'reviews', 'date_created', 'status')
        # read_only_fields = ['user']



class PostListSerializer(serializers.ModelSerializer):
    ''' List of posts'''
    subscription = SubscriptionSerializer(read_only=True)
    city = CitySerializer(read_only=True)
    class Meta:
        model = Post
        fields = ('id', 'title', 'subscription', 'from_price', 'subcategory', 'category', 'image',
                  'description', 'date_created', 'city')



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


