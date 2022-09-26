import datetime

import django_filters
import redis
from django.db.models import Q
from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from phonenumber_field.validators import validate_international_phonenumber
from rest_framework import generics, status, filters as f
from rest_framework.filters import SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .permissions import UserPermission
from .serializers import *
from django_filters import rest_framework as filters

from .utils import multiple_images, sql_recursive

''' For views/statistics '''
date = datetime.datetime.now(tz=None)
month = date.month
yaer = date.year
today = date.day


class Pagination(PageNumberPagination):
    '''Pagination for all'''
    def get_paginated_response(self, data):
        return super().get_paginated_response(data)


class CategoryAPIView(generics.ListAPIView):
    '''List of categories'''
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class SubcategoryAPIView(generics.ListAPIView):
    '''List of subcategories'''
    queryset = Subcategory.objects.all()
    serializer_class = SubcategorySerializer


class CityAPIView(generics.ListAPIView):
    '''List of cities'''
    queryset = City.objects.all()
    serializer_class = CitySerializer


class SubscriptionViewSet(ModelViewSet):
    '''List of subscriptions'''
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    # permission_classes = [IsAuthenticated, UserPermission, ]
    permission_classes = [AllowAny]


class PostCreate(generics.CreateAPIView):
    '''Create Post'''
    serializer_class = PostCreateSerializer
    permission_classes = [AllowAny]
    # permission_classes = [IsAuthenticated]


class PostImagesView(APIView):
    '''Adding images to post'''
    permission_classes = [AllowAny]
    # permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request):
        all_images = PostImages.objects.all()
        serializer = PostImagesSerializer(all_images, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request, *args, **kwargs):
        post = request.data['post']
        images = dict((request.data).lists())['image']
        flag = 1
        list_images = []
        for img_name in images:
            modified_data = multiple_images(post, img_name)
            image_serializer = PostImagesSerializer(data=modified_data)
            if image_serializer.is_valid():
                image_serializer.save()
                list_images.append(image_serializer.data)
            else:
                flag = 0

        if flag == 1:
            return Response(list_images, status=status.HTTP_201_CREATED)
        else:
            return Response(list_images, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        pk = request.GET.get('pk')
        image = PostImages.objects.get(id=pk)
        image.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PostContactsView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [AllowAny]
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        all_phones = PostContacts.objects.all()
        serializer = ContactSerializer(all_phones, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request, *args, **kwargs):
        post = request.data['post']
        post = Post.objects.get(pk=post)
        list_contacts = []
        contacts = request.data['phone_number'].split(',')
        for contact in contacts:
            validate_international_phonenumber(contact)
            list_contacts.append(PostContacts(post_number=post, phone_number=contact))

        PostContacts.objects.bulk_create(list_contacts)
        return Response({"status": "created"}, status=status.HTTP_201_CREATED)

    def delete(self, request):
        pk = request.GET.get('pk')
        phone = PostContacts.objects.get(id=pk)
        phone.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PostDelete(generics.RetrieveDestroyAPIView):

    serializer_class = PostEditSerializer
    # permission_classes = [IsAuthenticated, UserPermission, ]
    permission_classes = [AllowAny]
    lookup_field ='pk'
    queryset = Post.objects.all()


class PostEdit(generics.RetrieveUpdateAPIView):

    serializer_class = PostDetailSerializer
    # permission_classes = [IsAuthenticated, UserPermission, ]
    permission_classes = [AllowAny]
    lookup_field ='pk'
    queryset = Post.objects.all()


class PostListHighlightPagination(Pagination):
    '''Pagination for post list by date'''
    page_size = 10


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


class PostList(generics.ListAPIView):
    '''Post List by date'''
    filter_backends = [DjangoFilterBackend]
    serializer_class = PostListSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend, f.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['date_created', 'from_price']
    queryset = Post.objects.filter(Q(subscription__choice='Добавить стикер "Срочно"') | Q(subscription__choice='VIP') |
                                   Q(subscription__choice='Выделить цветом'), is_activated=True)
    pagination_class = PostListHighlightPagination
    filterset_class = ProductFilter


class PostListDatePagination(Pagination):
    '''Pagination for post list by date'''
    page_size = 20


class PostlistDate(generics.ListAPIView):
    '''Post List by date subscription'''
    filter_backends = [DjangoFilterBackend]
    serializer_class = PostListSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend, f.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['date_created', 'from_price']
    queryset = Post.objects.filter(is_activated=True).order_by('-date_created')
    pagination_class = PostListDatePagination
    filterset_class = ProductFilter


class MyPostList(generics.ListAPIView):
    '''Post Filter'''
    filter_backends = [DjangoFilterBackend]
    serializer_class = PostListSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend, f.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['date_created', 'from_price']
    queryset = Post.objects.filter(Q(subscription__choice='highlight') | Q(subscription__choice='VIP') |
                                   Q(subscription__choice='urgent'), is_activated=True)
    pagination_class = PostListHighlightPagination
    filterset_class = ProductFilter
    # permission_classes = [IsAuthenticated, UserPermission, ]
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user.id)


class ReviewView(ModelViewSet):
    queryset = ReviewPost.objects.all()
    serializer_class = ReviewCreateSerializer

    def list(self, request, *args, **kwargs):
        comments = sql_recursive()
        # print(list(comments))
        serializer = ReviewSerializer(comments, many=True)
        return Response(serializer.data)


class FavoriteCreateView(generics.CreateAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    # permission_classes = [IsAuthenticated, UserPermission, ]
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FavoriteListView(generics.ListAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    # permission_classes = [IsAuthenticated, UserPermission, ]
    permission_classes = [AllowAny]

    def get_queryset(self):
        qs = self.request.user
        queryset = Favorite.objects.filter(user=qs, favorites=True)
        return queryset


class FavoriteGetDeleteView(generics.RetrieveDestroyAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    # permission_classes = [IsAuthenticated, UserPermission, ]
    permission_classes = [AllowAny]


class PostComplaintView(generics.ListCreateAPIView):
    queryset = PostComplaint.objects.all()
    serializer_class = PostComplaintSerializer


# Views
def get_post(client, title, pk):
    data = redis.Redis()
    data_value = data.get(str(client))

    if data_value is None or data_value.decode('utf-8') != title:
        data.mset({str(client): title})
        post_object = Post.objects.get(pk=pk)  # 4
        view_object = Views.objects.filter(post=post_object).filter(date=date).exists()

        if view_object == False:
            Views.objects.create(post=post_object, date=date)

        name = Views.objects.filter(post=post_object).filter(date=date).values('pk')
        name = Views.objects.get(pk=name[0]['pk'])
        name.date = date
        name.save(update_fields=["date"])
        name.views += 1
        name.save(update_fields=["views"])

        return False
    else:
        return True


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')
    else:
        ip = request.META.get('REMOTE_ADDR')

    return ip


class DetailPost(APIView):
    def get(self, request, pk):
        get_object_or_404(Post, pk=pk)  # 1
        posts = Post.objects.select_related('category').get(pk=pk)
        title = Post.objects.values('title').filter(pk=pk)  # 2

        title = title[0]['title']
        ip = get_client_ip(request)

        if request.user.is_authenticated:
            if not get_post(request.user, title, pk):
                posts.views += 1
                posts.save(update_fields=["views"])
        else:
            if not get_post(ip, title, pk):
                posts.views += 1
                posts.save(update_fields=["views"])

        post_object = Post.objects.get(pk=pk)  # 3
        view = Views.objects.filter(post=post_object).filter(date=date)
        view = view[0]
        serializer_view = ViewSerializer(view, many=False).data
        serializer = PostEditSerializer(posts, many=False).data
        post_sub = Post.objects.prefetch_related('subcategory').get(pk=pk)
        context = {
            'add': {**serializer, 'category': posts.category.title,
                    'subcategory': post_sub.subcategory.title},
            'view': serializer_view
        }
        return Response(context)


class StatistictsApi(APIView):
    def get(self, requests, pk):
        post=get_object_or_404(Post,pk=pk)
        serializer_post = StatisticsPostSerilizer(post, many=False).data
        id_post = Post.objects.filter(pk=pk).values('pk')
        view_every_day = Views.objects.filter(post=id_post[0]['pk']).filter(date__year=yaer, date__month=month)
        serializer_view_every_day = StatisticsViewSerializer(view_every_day, many=True).data
        view_today_id = Views.objects.filter(post=id_post[0]['pk']).filter(date__year=yaer,
                                                                           date__month=month,
                                                                           date__day=today).values('pk').exists()
        object_post = Post.objects.get(pk=pk)
        if view_today_id == False:
            Views.objects.create(post=object_post, date=date)
            view_today_id = Views.objects.filter(post=object_post).filter(date=date).values('pk')
        else:
            view_today_id = Views.objects.filter(post=object_post).filter(date=date).values('pk')

        view_today = Views.objects.get(pk=view_today_id[0]['pk'])
        serializer_view_today = TodaySerializer(view_today, many=False).data
        post_object = Post.objects.get(pk=pk)
        phone_object = PostContacts.objects.filter(post_number=post_object).exists()

        if phone_object ==False:
            serializer_view_number = 'Контакты отсутствую!'

        else:
            phone_object = PostContacts.objects.get(post_number=post_object)
            serializer_view_number = StaticsNumberSerializer(phone_object, many=False).data

        context = {
            'common post view': serializer_post,
            'view post today': serializer_view_today,
            'common view number of contacts': serializer_view_number,
            'view post every day': serializer_view_every_day,

        }
        return Response(context)


def get_post_number(client, number, pk):
    data = redis.Redis()
    data_value = data.get(str(client))
    client = str(client)

    if data_value is None or data_value.decode('utf-8') != number[0]['phone_number']:
        data.mset({client: number[0]['phone_number']})

        date = datetime.datetime.now(tz=None)
        today = date.date()
        post_object = Post.objects.get(pk=pk)
        number = PostContacts.objects.get(post_number=post_object)
        viewscontact_object = ViewsContact.objects.filter(phone=number).filter(date=today).exists()
        if viewscontact_object == False:
            object_view = Views.objects.get(post=post_object)
            ViewsContact.objects.create(phone=number, date=today, view_key=object_view)

        name = ViewsContact.objects.filter(phone=number).filter(date=today).values('pk')
        name = ViewsContact.objects.get(pk=name[0]['pk'])
        name.date = today
        name.save(update_fields=["date"])
        name.views += 1
        name.save(update_fields=["views"])

        return False
    else:
        return True


class Contacts(APIView):
    def get(self, request, pk):
        get_object_or_404(Post, pk=pk)
        post_object = Post.objects.get(pk=pk)
        value_number_check = PostContacts.objects.filter(post_number=post_object).exists()

        if value_number_check == False:
            return Response('Контакты отсутсвуют!')

        number = PostContacts.objects.get(post_number=post_object)
        value_number = PostContacts.objects.filter(post_number=post_object).values('phone_number')
        ip = get_client_ip(request)

        if request.user.is_authenticated:
            if not get_post_number(request.user, value_number, pk):
                number.view += 1
                number.save(update_fields=["view"])
        else:
            if not get_post_number(ip, value_number, pk):
                number.view += 1
                number.save(update_fields=["view"])

        post_object = Post.objects.get(pk=pk)
        view = Views.objects.filter(post=pk).filter(date=date).exists()

        if view == False:
            Views.objects.create(post=post_object, date=date)

        object = PostContacts.objects.get(post_number=post_object)
        queryset = object
        serializer = ContactSerializer(queryset, many=False).data
        return Response(serializer)
