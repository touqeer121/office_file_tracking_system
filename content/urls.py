from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import include, path
from . import  views
from office_file_tracking_system import  settings


urlpatterns = [
                  # url(r'^meetOurTeam/$', views.More_info, name='login')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
