from django.urls import path, include
from rest_framework import routers
from rest_framework.routers import DefaultRouter

from . import views
from .views import *


urlpatterns = [
    path("category/", CategoryAPIView.as_view(), name="category"),
    path("subcategory/", SubcategoryAPIView.as_view(), name="subcategory"),
    path("city/", CityAPIView.as_view(), name="city"),
    path("subscription/", SubscriptionAPIView.as_view(), name="subscription"),

    path('createpost/', views.PostCreate.as_view(), name="createpost"), #no
    path('addimages/', views.PostImagesView.as_view()),
    path('addcontacts/', views.PostContactsCreate.as_view()),
    path('detailcontacts/<int:pk>', views.PostContactsDetail.as_view()),

    path('detailpost/<int:pk>', views.PostDetail.as_view()),
    path('postlist/', views.PostList.as_view(), name="postlist"),
    path('postlistdate/', views.PostlistDate.as_view(), name="postlistdate"),
    path('mypost/', views.MyPostList.as_view(), name="mypost"),

    path("review/", views.ReviewCreateView.as_view(), name="review"),

    path('favoritecreate/', FavoriteCreateView.as_view()),
    path('favoriteupdate/<int:pk>/', FavoriteUpdateView.as_view()),
    path('favorite/', FavoriteListView.as_view()),
    path('favorite/<int:pk>/', FavoriteGetDeleteView.as_view()),

]
