from django.urls import path, include
from rest_framework import routers
from rest_framework.routers import DefaultRouter

from . import views
from .views import *

router = DefaultRouter()
router.register('favorite', FavoriteViewSet),

urlpatterns = [

    path("category/", CategoryAPIView.as_view(), name="category"),
    path("subcategory/", SubcategoryAPIView.as_view(), name="subcategory"),
    path("city/", CityAPIView.as_view(), name="city"),
    path("subscription/", SubscriptionAPIView.as_view(), name="subscription"),

    path('createpost/', views.PostCreate.as_view(), name="createpost"), #no
    path('addimages/', views.PostImagesView.as_view()),
    path('addcontacts/', views.PostContactsCreate.as_view()),

    path('detailpost/<int:pk>', views.PostDetail.as_view()),
    path('detailcontacts/<int:pk>', views.PostContactsDetail.as_view()),
    # path('view/<str:pk>', ViewNews.as_view()),

    path('postlist/', views.PostList.as_view(), name="postlist"),
    path('postlistdate/', views.PostlistDate.as_view(), name="postlistdate"),
    path('mypost/', views.MyPostList.as_view(), name="mypost"),

    path("review/", views.ReviewCreateView.as_view(), name="review"),

    # path('favoritecreate/', FavoritesCreateView.as_view()),
    # path('favorite/', FavoritesListView.as_view()),
    # path('favorite/<int:pk>/', FavoriteGetDeleteView.as_view()),

]

urlpatterns = [
    path('', include(router.urls)),
]