from django.urls import path

from info.views import IssueAPIView, HelpAPIView, DetailHelpAPIView

urlpatterns = [
    path("issue/", IssueAPIView.as_view(), name="issue"),
    path("help/", HelpAPIView.as_view(), name="help"),
    path("detailhelp/<int:pk>", DetailHelpAPIView.as_view(), name="detailhelp"),

]