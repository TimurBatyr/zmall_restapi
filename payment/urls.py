from django.urls import path

from .views import Success, Payment, TransactionView, Failure


urlpatterns = [
    path('success', Success.as_view()),
    path('failure', Failure.as_view()),
    path('pay/<int:pk>/<int:pn>',Payment.as_view()),
    path('storetransaction',TransactionView.as_view())
]