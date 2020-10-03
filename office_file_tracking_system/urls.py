from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.conf.urls.static import static
from office_file_tracking_system import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^', include(('accounts.urls', 'accounts'), namespace='accounts')),
    url(r'content/', include(('content.urls', 'content'), namespace='content')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
