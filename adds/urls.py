from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views
from .views import *

router = DefaultRouter()
router.register('subscription', SubscriptionViewSet, basename='subscription')
router.register("review", ReviewView, basename='review')


urlpatterns = [
    path('', include(router.urls)),
    path("category/", CategoryAPIView.as_view(), name="category"),
    path("subcategory/", SubcategoryAPIView.as_view(), name="subcategory"),
    path("city/", CityAPIView.as_view(), name="city"),

    path('postimages/', views.PostImagesView.as_view()),

    path('postcontacts/', views.PostContactsView.as_view()),
    path('postcontactlist/<int:pk>', PostContactlist.as_view()),

    path('createpost/', views.PostCreate.as_view(), name="createpost"), #no
    path('deletepost/<int:pk>', views.PostDelete.as_view()),
    path('editpost/<int:pk>', views.PostEdit.as_view()),
    path('postlist/', views.PostList.as_view(), name="postlist"),
    path('postlistdate/', views.PostlistDate.as_view(), name="postlistdate"),
    path('mypost/', views.MyPostList.as_view(), name="mypost"),

    # path("review/", views.ReviewCreateView.as_view(), name="review"),

    path('favoritecreate/', FavoriteCreateView.as_view()),
    path('favorite/', FavoriteListView.as_view()),
    path('favorite/<int:pk>', FavoriteGetDeleteView.as_view()),

    path('postcomplaint/', PostComplaintView.as_view()),

#views
    path('view/<int:pk>', DetailPost.as_view()),
    path('viewstatistics/<int:pk>', StatistictsApi.as_view()),
    path('viewcontact/<int:pk>', Contacts.as_view()),
]
