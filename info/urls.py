from django.urls import path

from info.views import IssueAPIView, HelpAPIView, HelpGetAPIView, AdminContactListAPIView, AdminContactGetAPIView, \
    AdminContactCreateAPIView, AdminHatAPIView, ConfPoliticsAPIView, FooterListAPIView, AdminThemeAPIView

urlpatterns = [
    path("issue/", IssueAPIView.as_view(), name="issue"),

    path("help/", HelpAPIView.as_view(), name="help"),
    path("helpget/<int:pk>", HelpGetAPIView.as_view(), name="detailhelp"),

    path("adminhat/", AdminHatAPIView.as_view(), name="adminhat"),
    path("admintheme/", AdminThemeAPIView.as_view(), name="admintheme"),
    path("admincontact/", AdminContactCreateAPIView.as_view(), name="admincontact"),
    path("admincontactlist/", AdminContactListAPIView.as_view(), name="admincontactlist"),
    path("admincontactget/<int:pk>", AdminContactGetAPIView.as_view(), name="admincontactget"),

    path("confpolitics/", ConfPoliticsAPIView.as_view(), name="confpolitics"),

    path("footer/", FooterListAPIView.as_view(), name="footer"),

]