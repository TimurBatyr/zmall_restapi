import datetime

import django_filters
import redis
from django.db.models import Q
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets, status, filters as f
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .permissions import UserPermission
from .serializers import *
from django_filters import rest_framework as filters

from .utils import multiple_images


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


class SubscriptionAPIView(generics.ListAPIView):
    '''List of subscriptions'''
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer


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


class PostContactsCreate(generics.CreateAPIView):
    '''Adding/updating contacts to the post'''

    serializer_class = PostContactsSerializer
    permission_classes = [AllowAny]
    # permission_classes = [IsAuthenticated]


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    '''Post Update/delete/detail'''

    serializer_class = PostEditSerializer
    # permission_classes = [IsAuthenticated, UserPermission, ]
    permission_classes = [AllowAny]
    lookup_field ='pk'
    queryset = Post.objects.all()


class PostContactsDetail(generics.RetrieveUpdateDestroyAPIView):
    '''Contacts Update/delete/detail'''
    serializer_class = PostContactsSerializer
    # permission_classes = [IsAuthenticated, UserPermission, ]
    permission_classes = [AllowAny]
    lookup_field = 'pk'
    queryset = PostContacts.objects.all()


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
    # filterset_fields = ['category', ]
    ordering_fields = ['date_created', 'from_price']
    queryset = Post.objects.filter(Q(subscription__choice='highlight') | Q(subscription__choice='VIP') |
                                   Q(subscription__choice='urgent'), is_activated=True)
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
    serializer_class = PostListSerializer
    # permission_classes = [IsAuthenticated, UserPermission, ]
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user.id)

    '''Post Filter'''
    filter_backends = [DjangoFilterBackend]
    serializer_class = PostListSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend, f.OrderingFilter]
    search_fields = ['title', 'description']
    # filterset_fields = ['category', ]
    ordering_fields = ['date_created', 'from_price']
    queryset = Post.objects.filter(Q(subscription__choice='highlight') | Q(subscription__choice='VIP') |
                                   Q(subscription__choice='urgent'), is_activated=True)
    pagination_class = PostListHighlightPagination
    filterset_class = ProductFilter


class ReviewCreateView(APIView):
    '''Adding comment to the post'''
    def post(self, request):
        review = ReviewCreateSerializer(data=request.data)
        if review.is_valid():
            review.save()
        return Response(status=201)


class FavoriteCreateView(generics.CreateAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated, UserPermission, ]
    # permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        qs = self.request.user
        queryset = Favorite.objects.filter(user=qs, favorites=True)
        return queryset

class FavoriteUpdateView(generics.UpdateAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated, UserPermission, ]
    # permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



class FavoriteListView(generics.ListAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    # permission_classes = [IsAuthenticated, UserPermission, ]
    permission_classes = [AllowAny]


class FavoriteGetDeleteView(generics.RetrieveDestroyAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    # permission_classes = [IsAuthenticated, UserPermission, ]
    permission_classes = [AllowAny]


class FavoriteViewSet(ModelViewSet):
    serializer_class = FavoriteSerializer
    queryset = Favorite.objects.all()
    # permission_classes = [IsAuthenticated, UserPermission, ]
    permission_classes = [AllowAny]


"""---Views---"""
def get_post(client, title, pk):
    data = redis.Redis()
    data_value = data.get(str(client))
    if data_value is None or data_value.decode('utf-8') != title:
        data.mset({str(client): title})
        date = datetime.datetime.now(tz=None)
        today = date.date()
        # today = datetime.date(year=2022, month=9, day=9)
        post_object = Post.objects.get(pk=pk)  #4
        view_object = Views.objects.filter(post=post_object).filter(date=today).exists()

        if view_object == False:
            Views.objects.create(post=post_object, date=today)

        name = Views.objects.filter(post=post_object).filter(date=today).values('pk')
        name = Views.objects.get(pk=name[0]['pk'])
        name.date = today
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
        posts = get_object_or_404(Post, pk=pk)#1
        title = Post.objects.values('title').filter(pk=pk)#2
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

        post_object = Post.objects.get(pk=pk)#3
        date = datetime.datetime.now(tz=None)
        today = date.date()
        view = Views.objects.filter(post=post_object).filter(date=today).exists()

        if not view:
            Views.objects.create(post=post_object, date=today)

        view = Views.objects.filter(post=post_object).filter(date=today)
        view = view[0]

        serializer_view = ViewSerializer(view, many=False).data
        serializer = AddPostSerializer(posts, many=False).data

        context = {
            'add': serializer,
            'view': serializer_view
        }
        return Response(context)

class StatistictsApi(APIView):
    def get(self, requests, pk):
        post = Post.objects.get(pk=pk)
        serializer_post = StatisticsPostSerilizer(post, many=False).data
        date = datetime.datetime.now(tz=None)
        month = date.month
        yaer = date.year
        today = date.day

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

        post_object =Post.objects.get(pk=pk)
        phone_object=PhoneNumber.objects.get(post_number=post_object)
        view_contact_objects=ViewsContact.objects.get(phone=phone_object)
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
    print(number)

    if data_value is None or data_value.decode('utf-8') != number[0]['phone_number']:
        data.mset({client: number[0]['phone_number']})

        date = datetime.datetime.now(tz=None)
        today = date.date()




        post_object = Post.objects.get(pk=pk)
        number = PhoneNumber.objects.get(post_number=post_object)
        viewscontact_object = ViewsContact.objects.filter(phone=number).filter(date=today).exists()
        print('ooooooooooooooooooo')
        if viewscontact_object ==False:
            object_view=Views.objects.get(post=post_object)
            ViewsContact.objects.create(phone=number,date=today,view_key=object_view)


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


        post_object = Post.objects.get(pk=pk)
        number = PhoneNumber.objects.get(post_number=post_object)

        print(number,"<<<<<<<<<<<<<<<<<www")

        value_number = PhoneNumber.objects.filter(post_number=post_object).values('phone_number')
        ip = get_client_ip(request)
        print('<<<<<<<<<<<<<<<<')
        if request.user.is_authenticated:
            if not get_post_number(request.user, value_number, pk):
                number.view += 1
                number.save(update_fields=["view"])
        else:
            if not get_post_number(ip, value_number, pk):
                number.view += 1
                number.save(update_fields=["view"])
        print('-------------------------')

        post_object=Post.objects.get(pk=pk)
        object=PhoneNumber.objects.get(post_number=post_object)
        queryset = object
        serializer = ContactSerializer(queryset, many=False).data

        return Response(serializer)

