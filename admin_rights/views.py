from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser

from account.models import User
from adds.models import Category, Subcategory, Subscription, PostImages, PostContacts, Post, ReviewPost, Views, \
    Favorite, City
from admin_rights.serializers import UserDetailSerializer, CategorySerializer, SubscriptionSerializer, \
    PostImagesSerializer, PostContactsSerializer, SubcategorySerializer, PostSerializer, ReviewSerializer, \
    ViewsSerializer, FavoriteSerializer, MessageSerializer, CitySerializer
from chat.models import Message



class UserViewSet(ModelViewSet):
    serializer_class = UserDetailSerializer
    queryset = User.objects.all()
    permission_classes = [IsAdminUser]


class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [IsAdminUser]


class SubCategoryViewSet(ModelViewSet):
    serializer_class = SubcategorySerializer
    queryset = Subcategory.objects.all()
    permission_classes = [IsAdminUser]


class CityViewSet(ModelViewSet):
    serializer_class = CitySerializer
    queryset = City.objects.all()
    permission_classes = [IsAdminUser]


class SubscriptionViewSet(ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAdminUser]


class PostImageViewSet(ModelViewSet):
    queryset = PostImages.objects.all()
    serializer_class = PostImagesSerializer
    permission_classes = [IsAdminUser]


class PostContactsViewSet(ModelViewSet):
    queryset = PostContacts.objects.all()
    serializer_class = PostContactsSerializer
    permission_classes = [IsAdminUser]


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAdminUser]


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    queryset = ReviewPost.objects.all()
    permission_classes = [IsAdminUser]


class ViewsViewSet(ModelViewSet):
    serializer_class = ViewsSerializer
    queryset = Views.objects.all()
    permission_classes = [IsAdminUser]


class FavoriteViewSet(ModelViewSet):
    serializer_class = FavoriteSerializer
    queryset = Favorite.objects.all()
    permission_classes = [IsAdminUser]


class MessageViewSet(ModelViewSet):
    serializer_class = MessageSerializer
    queryset = Message.objects.all()
    permission_classes = [IsAdminUser]


