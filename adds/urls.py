from django.urls import path, include
from rest_framework import routers
from rest_framework.routers import DefaultRouter

from . import views
from .views import *


urlpatterns = [

    path("category/", CategoryAPIView.as_view()),
    path("subcategory/", SubcategoryAPIView.as_view()),
    path("city/", CityAPIView.as_view()),
    path("subscription/", SubscriptionAPIView.as_view()),

    path('createpost/', views.PostCreate.as_view()),
    path('addimages/', views.PostImagesView.as_view()),
    path('addcontacts/', views.PostContactsCreate.as_view()),

    path('detailpost/<int:pk>', views.PostDetail.as_view()),
    path('detailcontacts/<int:pk>', views.PostContactsDetail.as_view()),
    # path('view/<str:pk>', ViewNews.as_view()),

    path('postlist/', views.PostListHighlight.as_view()),
    path('postlistdate/', views.PostlistDate.as_view()),
    path('mypost/', views.MyPostList.as_view()),

    path("review/", views.ReviewCreateView.as_view())


]