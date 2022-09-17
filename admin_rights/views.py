from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser

from account.models import User
from adds.models import Category, Subcategory, Subscription, PostImages, PostContacts, Post, ReviewPost, Views, \
    Favorite, City
from admin_rights.serializers import UserDetailSerializerAd, CategorySerializerAd, SubscriptionSerializerAd, \
    PostImagesSerializerAd, PostContactsSerializerAd, SubcategorySerializerAd, PostSerializerAd, ReviewSerializerAd, \
    ViewsSerializerAd, FavoriteSerializerAd, MessageSerializerAd, CitySerializerAd
from chat.models import Message


class UserViewSet(ModelViewSet):
    serializer_class = UserDetailSerializerAd
    queryset = User.objects.all()
    permission_classes = [IsAdminUser]


class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializerAd
    queryset = Category.objects.all()
    permission_classes = [IsAdminUser]


class SubcategoryViewSet(ModelViewSet):
    serializer_class = SubcategorySerializerAd
    queryset = Subcategory.objects.all()
    permission_classes = [IsAdminUser]


class CityViewSet(ModelViewSet):
    serializer_class = CitySerializerAd
    queryset = City.objects.all()
    permission_classes = [IsAdminUser]


class SubscriptionViewSet(ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializerAd
    permission_classes = [IsAdminUser]


class PostImagesViewSet(ModelViewSet):
    queryset = PostImages.objects.all()
    serializer_class = PostImagesSerializerAd
    permission_classes = [IsAdminUser]


class PostContactsViewSet(ModelViewSet):
    queryset = PostContacts.objects.all()
    serializer_class = PostContactsSerializerAd
    permission_classes = [IsAdminUser]


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializerAd
    permission_classes = [IsAdminUser]


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializerAd
    queryset = ReviewPost.objects.all()
    permission_classes = [IsAdminUser]


class ViewsViewSet(ModelViewSet):
    serializer_class = ViewsSerializerAd
    queryset = Views.objects.all()
    permission_classes = [IsAdminUser]


class FavoriteViewSet(ModelViewSet):
    serializer_class = FavoriteSerializerAd
    queryset = Favorite.objects.all()
    permission_classes = [IsAdminUser]


class MessageViewSet(ModelViewSet):
    serializer_class = MessageSerializerAd
    queryset = Message.objects.all()
    permission_classes = [IsAdminUser]


