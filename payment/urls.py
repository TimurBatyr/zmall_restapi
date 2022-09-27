from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import PaymentViewSet, api, api2, Payment, TransactionView

#Payment1

router = DefaultRouter()
router.register("create", PaymentViewSet, basename='payment')

urlpatterns = [
    path("payment/<int:pk>", include(router.urls)),
    path('success', api.as_view()),
    path('failure', api2.as_view()),
    # path('result', api3.as_view()),
    path('pay/<int:pk>/<int:pn>',Payment.as_view()),
    path('storetransaction',TransactionView.as_view())
]
