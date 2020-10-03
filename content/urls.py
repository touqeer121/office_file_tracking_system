from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import include, path
from . import  views
from office_file_tracking_system import  settings

app_name='content'

urlpatterns = [
                url(r'^scholarships/$', views.Show_Scholarships, name=''),
                url(r'^scholarships/(?P<s_id>\w+)', views.Scholarship_Detail, name='Scholarship_Detail'),
                path('track_application/', views.Track_Application, name='Track_Application'),
                url('apply/', views.Apply, name='Apply'),
                path('add_scholarship', views.Add_Scholarship, name='Add_Scholarship'),
                path('pending_approvals/', views.Show_Pending_Approvals, name='Show_Pending_Approvals'),
                path('track_student_applications/', views.Track_Student_Applications, name='Track_Student_Applications'),
                # url(r'^pending_approvals/(?P<app_id>\w+)', views.Show_Pending_Approval_Docs, name='Show_Pending_Approval_Docs'),
                path('approve/', views.Approve, name='Approve'),
                path('reject/', views.Reject, name='Reject'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
