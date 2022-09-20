from django.urls import path, include
from rest_framework.routers import DefaultRouter

from admin_rights.views import UserViewSet, CategoryViewSet, SubcategoryViewSet, CityViewSet, SubscriptionViewSet, \
    PostImagesViewSet, PostContactsViewSet, PostViewSet, ReviewViewSet, ViewsViewSet, FavoriteViewSet, MessageViewSet, \
    PostComplaintViewSet

router = DefaultRouter()
router.register('user', UserViewSet)
router.register('category', CategoryViewSet)
router.register('subcategory', SubcategoryViewSet)
router.register('city', CityViewSet)
router.register('subscription', SubscriptionViewSet)
router.register('postimages', PostImagesViewSet)
router.register('postcontacts', PostContactsViewSet)
router.register('post', PostViewSet)
router.register('review', ReviewViewSet)
router.register('views', ViewsViewSet)
router.register('message', MessageViewSet)
router.register('favorite', FavoriteViewSet)
router.register('complaint', PostComplaintViewSet)

urlpatterns = [
    path('admin/', include(router.urls)),
]
