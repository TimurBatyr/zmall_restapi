from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions


schema_view = get_schema_view(
    openapi.Info(
        title='zmall_restapi',
        description='zmall',
        default_version='v1'
    ),
    public=True,
    permission_classes=(permissions.AllowAny, ),
)


urlpatterns = [
    path('api/v1/docs/', schema_view.with_ui('swagger')),

]