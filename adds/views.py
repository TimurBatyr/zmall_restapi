from django.http import Http404, JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets, status, filters as f
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

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

    class Meta:
        model = Post
        fields = ['category', 'city']


class PostListHighlight(generics.ListAPIView):
    '''Post List by date'''
    filter_backends = [DjangoFilterBackend]
    serializer_class = PostListSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend, f.OrderingFilter]
    search_fields = ['title', 'description']
    # filterset_fields = ['category', ]
    ordering_fields = ['date_created', 'from_price']
    queryset = Post.objects.filter(is_activated=True).order_by('-date_created')
    pagination_class = PostListHighlightPagination
    filterset_class = ProductFilter


class PostListDatePagination(Pagination):
    '''Pagination for post list by date'''
    page_size = 20


class PostlistDate(generics.ListAPIView):
    '''Post List by highlighted subscription'''
    serializer_class = PostListSerializer
    queryset = Post.objects.filter(subscription__choice='highlight').order_by('-date_created')
    pagination_class = PostListDatePagination

    # def get_queryset(self):
    #     return Post.objects.filter(subscription__choice='highlight')
        # return Post.objects.select_related('city', 'subcategory').filter(subscription__choice='highlight') ^ Post.objects.filter(subscription__choice='VIP')


class MyPostList(generics.ListAPIView):
    serializer_class = PostListSerializer
    # permission_classes = [IsAuthenticated, UserPermission, ]
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user.id)


class ReviewCreateView(APIView):
    '''Adding comment to the post'''
    def post(self, request):
        review = ReviewCreateSerializer(data=request.data)
        if review.is_valid():
            review.save()
        return Response(status=201)




# # Фильтры
# class FilterAPIView(generics.ListAPIView):
#     queryset = Post.objects.all()
#     serializer_class = SearchSerializer
#     filter_backends = [f.OrderingFilter]
#     ordering_fields = ['date_created', 'from_price']
#
#
# class ProductFilter(filters.FilterSet):
#     min_price = filters.NumberFilter(field_name="from_price", lookup_expr='gte')
#     max_price = filters.NumberFilter(field_name="from_price", lookup_expr='lte')
#
#     class Meta:
#         model = Post
#         fields = ['category', 'city']

# class ProductList(generics.ListAPIView):
#     queryset = Post.objects.all()
#     serializer_class = SearchSerializer
#     filter_backends = (filters.DjangoFilterBackend,)
#     filterset_class = ProductFilter