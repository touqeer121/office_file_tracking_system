from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'student/register/$', views.UserFormView.as_view(), name='student_register'),
    url(r'staff/register/$', views.StaffFormView.as_view(), name='staff_register'),
    url(r'login/$', views.user_login, name='login'),
    url(r'logout/$', views.user_logout, name='logout'),
    url(r'getNames/', views.getNames),
    path('activate_users/', views.Activate_Users, name='Activate_Users'),
    path('activate/<int:uid>', views.Activate, name='Activate'),
    path('deactivate/<int:uid>', views.Deactivate, name='Deactivate'),

]
