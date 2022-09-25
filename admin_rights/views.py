import django_filters
from django.db.models import Q
from django_filters.rest_framework import filters, DjangoFilterBackend
from rest_framework import filters as f
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser

from account.models import User
from adds.models import Category, Subcategory, Subscription, PostImages, PostContacts, Post, ReviewPost, Views, \
    Favorite, City, PostComplaint
from admin_rights.pagination import PostPagination
from admin_rights.serializers import UserDetailSerializerAd, CategorySerializerAd, SubscriptionSerializerAd, \
    PostImagesSerializerAd, PostContactsSerializerAd, SubcategorySerializerAd, PostSerializerAd, ReviewSerializerAd, \
    ViewsSerializerAd, FavoriteSerializerAd, MessageSerializerAd, CitySerializerAd, PostComplaintSerializerAd
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


class ProductFilter(filters.FilterSet):
    '''Setting filters from and to on prices and cities'''
    min_price = filters.NumberFilter(field_name="from_price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="from_price", lookup_expr='lte')
    city = django_filters.ModelMultipleChoiceFilter(field_name='city', queryset=City.objects.all())
    image = django_filters.BooleanFilter(
        lookup_expr="isnull", field_name="image"
    )

    class Meta:
        model = Post
        fields = ['category', 'subcategory', 'city', 'image']


class PostViewSet(ModelViewSet):
    serializer_class = PostSerializerAd
    permission_classes = [IsAdminUser]

    filter_backends = [DjangoFilterBackend]
    filter_backends = [SearchFilter, DjangoFilterBackend, f.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['date_created', 'from_price']
    queryset = Post.objects.filter(Q(subscription__choice='highlight') | Q(subscription__choice='VIP') |
                                   Q(subscription__choice='urgent'), is_activated=True)
    pagination_class = PostPagination
    filterset_class = ProductFilter


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


class PostComplaintViewSet(ModelViewSet):
    serializer_class = PostComplaintSerializerAd
    queryset = PostComplaint.objects.all()
    permission_classes = [IsAdminUser]




