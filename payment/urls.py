from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import api, Payment, TransactionView, Failure

#Payment1

urlpatterns = [
    path('success', api.as_view()),
    path('failure', Failure.as_view()),
    path('pay/<int:pk>/<int:pn>',Payment.as_view()),
    path('storetransaction',TransactionView.as_view())
]
