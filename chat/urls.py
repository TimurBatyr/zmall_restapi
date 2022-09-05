from django.urls import path

from .views import ChatAPIView, message_list, user_list

urlpatterns = [

    path("chat/", ChatAPIView.as_view()),
    path('messages/<int:sender>/<int:receiver>/', message_list),
    path('messages/', message_list),
    path('users/', user_list),

]