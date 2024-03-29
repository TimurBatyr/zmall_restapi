from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from .yasg import urlpatterns as doc_urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/account/', include('account.urls')),
    path('api/v1/account/', include('social_auth.urls')),
    path('api/v1/adds/', include('adds.urls')),
    path('api/v1/', include('chat.urls')),
    path('api/v1/', include('admin_rights.urls')),
    path('api/v1/info/', include('info.urls')),
    path('api/v1/', include('payment.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += doc_urls