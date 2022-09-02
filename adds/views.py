from django.http import Http404, JsonResponse
from rest_framework import generics, viewsets, status, filters as f
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .permissions import UserPermission
from .serializers import *
from django_filters import rest_framework as filters

from .utils import multiple_images


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


class PostContacts(generics.CreateAPIView):
    '''Adding/updating contacts to the post'''

    serializer_class = PostContactsSerializer
    permission_classes = [AllowAny]
    # permission_classes = [IsAuthenticated]


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    '''Post Update/delete/detail View'''

    serializer_class = PostEditSerializer
    # permission_classes = [IsAuthenticated, UserPermission, ]
    permission_classes = [AllowAny]
    lookup_field ='pk'
    queryset = Post.objects.all()



# # Create your views here.
# # Просмотр каталога и обьявления
#
# class CategoryAPIView(generics.ListAPIView):
#     queryset = Category.objects.all()[0:9]
#     serializer_class = CategorySerializer
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