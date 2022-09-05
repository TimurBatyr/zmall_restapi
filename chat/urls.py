from django.urls import path

from .views import MessageAPIView

urlpatterns = [
    path('chat/', MessageAPIView.as_view()),
]