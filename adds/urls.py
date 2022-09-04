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
    # path('Subscription', SubscriptionApi.as_view()),
    # path('New', NewAdApiView.as_view()),
    # path('Ordering', FilterAPIView.as_view()),
    # path('Filter', ProductList.as_view()),
    # path('Search', SearchAPIListView.as_view()),
    # path('filterCategory', PostFilterList.as_view()),
    # path('sub/<int:pk>', SubcategoryAPIView.as_view()),
    path('createpost/', views.PostCreate.as_view()),
    path('addimages/', views.PostImagesView.as_view()),
    path('addcontacts/', views.PostContactsCreate.as_view()),

    path('detailpost/<int:pk>', views.PostDetail.as_view()),
    path('detailcontacts/<int:pk>', views.PostContactsDetail.as_view()),

    path('postlist/', views.PostListDate.as_view()),
    path('postlisthighlight/', views.PostlistHighlight.as_view()),
    path('mypost/', views.MyPostList.as_view()),

    path("review/", views.ReviewCreateView.as_view())


]