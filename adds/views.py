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



class PostListDatePagination(Pagination):
    '''Pagination for post list by date'''
    page_size = 20


class PostListDate(generics.ListAPIView):
    '''Post List by date'''
    filter_backends = [DjangoFilterBackend]
    serializer_class = PostListSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['title', 'description', 'sub']
    filterset_fields = ['category', ]
    queryset = Post.objects.all().order_by('-date_created')
    pagination_class = PostListDatePagination


class PostListHighlightPagination(Pagination):
    '''Pagination for post list by date'''
    page_size = 10


class PostlistHighlight(generics.ListAPIView):
    '''Post List by highlighted subscription'''
    serializer_class = PostListSerializer
    queryset = Post.objects.filter(subscription__choice='highlight').order_by('-date_created')
    pagination_class = PostListHighlightPagination

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


# # Create your views here.
# # Просмотр каталога и обьявления
#

#
#
# # def get(self, request, pr):
# #        movie = Product.objects.filter(category=pr)
# #        serializer = ListProductSerializer
# #        return Response(serializer(movie, many=True).data)
# #
# class SubscriptionApi(APIView):
#
#     def get(self, request):
#         x = Subscription.objects.values('post')
#         print(x)
#         wer = []
#         for i in x:
#             print(i['post'])
#
#             qq = Post.objects.get(pk=i['post'])
#             wer.append(qq)
#
#         movie = Post.objects.all()[0:10]
#         print(wer)
#
#         serializer = SubscriptionSerializer
#         return Response(serializer(wer, many=True).data)
#
#
# class NewAdApiView(generics.ListAPIView):
#     queryset = Post.objects.all().order_by('-date_created')[0:20]
#     serializer_class = NewSerializer
#
#
# # _________
# # Поиск
# class SearchAPIListView(generics.ListAPIView):
#     queryset = Post.objects.all()
#     serializer_class = SearchSerializer
#     filter_backends = [f.SearchFilter]
#     search_fields = ['title']
#
#
# # ---------
# # Фильтр по категориям
# class Filter(filters.FilterSet):
#     class Meta:
#         model = Post
#         fields = ['category']
#
#
# class PostFilterList(generics.ListAPIView):
#     queryset = Post.objects.all()
#     serializer_class = SearchSerializer
#     filter_backends = (filters.DjangoFilterBackend,)
#     filterset_class = Filter
#
#
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
#
#
# class ProductList(generics.ListAPIView):
#     queryset = Post.objects.all()
#     serializer_class = SearchSerializer
#     filter_backends = (filters.DjangoFilterBackend,)
#     filterset_class = ProductFilter
#
#
# # class DetailPostViewSet(viewsets.ModelViewSet):
# #     """Товар"""
# #     queryset = Post.objects.all()
# #     serializer_class = DetailPostSerializer
#
#
# class PostCRUDViewSet(viewsets.ModelViewSet):
#     serializer_class = PostSerializer
#     queryset = Post.objects.all()
#     # permission_classes = [IsAuthenticated]
#
#     # def perform_create(self, serializer):
#     #     return serializer.save(user=self.request.user)
#
#     # def get_serializer_class(self):
#     #     serializer_class = super().get_serializer_class()
#     #     if self.action == 'list':
#     #         serializer_class = PostCRUDSerializer
#     #     return serializer_class
#
#
#
# # ____________________________
#
# class SubcategoryAPIView(APIView):
#     def get(self, request, pk):
#
#         posts = Post.objects.filter(category=pk)
#         serializer222 = SearchSerializer(posts, many=True).data
#
#         count = dict()
#         for i in Subcategory.objects.values('id', 'title', 'category').filter(category=pk):
#             count[i['title']] = Post.objects.filter(subcategory=i['id']).count()
#             idcategory = i['category']
#
#         try:
#             NameCategory = Category.objects.filter(id=idcategory).values('title')
#             Name = NameCategory[0]['title']
#         except:
#             Name = None
#             raise Http404
#
#         context = {
#             'Category': Name,
#             'Subcategory': count,
#             Name: serializer222
#         }
#         return Response(context)