from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import PaymentViewSet

router = DefaultRouter()
router.register("create", PaymentViewSet, basename='payment')

urlpatterns = [
    path("payment/", include(router.urls)),
]