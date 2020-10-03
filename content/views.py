from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.views.decorators.csrf import csrf_exempt
from content.decorators import login_required_message
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
import datetime
from accounts.models import Department
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.conf import settings

@csrf_exempt
def checkuserifscrutinyuser(user):
    if user.groups.filter(name="owner").exists() and user.is_superuser:
        return True
    else:
        return False

@csrf_exempt
@login_required_message(message="You should be logged in, in order to perform this")
@login_required(login_url="/login/")
def Show_Scholarships(request):
    response = {}
    response['scholarships'] = Scholarship.objects.all()
    return render(request, 'content/all_scholarships.html', response)

@csrf_exempt
@login_required_message(message="You should be logged in, in order to perform this")
@login_required(login_url="/login/")
def Scholarship_Detail(request, s_id):
    response = {}
    app = Application.objects.filter(request=s_id, applicant=request.user.id)
    if len(app)>0:
        response['alreadyApplied'] = True
        response['app_id'] = app[0].app_id
        print("IF : ",response['app_id'])
    else:
        response['alreadyApplied'] = False
        response['app_id'] = None
        print("ELSE : ", response['app_id'])

    response['scholarship'] = Scholarship.objects.get(pk=s_id)

    return render(request, 'content/scholarship_detail.html', response)

@csrf_exempt
@login_required(login_url="/login/")
def Apply(request):
    print("APPLIED")
    s_id = request.POST.get('scholarship_id')
    sch = get_object_or_404(Scholarship, id = s_id)
    user_id = request.user.id
    user = get_object_or_404(CustomUser,id=user_id)
    app = Application.objects.filter(request=s_id, applicant=user_id)
    if len(app)>0:
        messages.info(request, "You have already applied to this scholarship")
        new_app = app[0]
    else:
        cnt = Application_Count.objects.get()
        year = datetime.datetime.now().year
        yy = str(year)
        p1 = yy[2:]
        p2 = str(cnt.app_cnt).zfill(4)
        Name = "APP"
        app_id = Name + p1 + p2
        cnt.app_cnt += 1
        cnt.save()
        print(app_id)
        new_app = Application.objects.create(app_id=app_id, current_authority=sch.receiver_authority_id)
        new_app.department = user.department
        new_app.category = request.POST.get('application_type')
        new_app.applicant = user
        new_app.request = sch
        new_app.title = sch.name
        new_app.current_step = 1
        new_app.max_step = sch.max_step
        new_app.is_approved = False
        new_app.attached_pdf = request.FILES.get("up_files", False)
        new_app.department_id = user.department
        new_app.save()
        messages.success(request, "You have successfully applied to this scholarship")

    data = {}
    data['alreadyApplied'] = True
    data['scholarship'] = sch
    response = {}
    response['scholarship'] = sch
    response['app_id'] = new_app.app_id
    return render(request, 'content/scholarship_detail.html', response)

@csrf_exempt
@login_required_message(message="You should be logged in, in order to perform this")
@login_required(login_url="/login/")
def Show_Pending_Approvals(request):
    applications = Application.objects.all()
    departments = Department.objects.all()
    response = {}
    response['applications'] = applications
    response['departments'] = departments
    designations = {'T', 'FA', 'DEAN', 'HOD', 'D'}
    response['designations'] = designations
    return render(request, 'content/show_pending_approvals.html', response)


# @csrf_exempt
# @login_required_message(message="You should be logged in, in order to perform this")
# @login_required(login_url="/login/")
# def Show_Pending_Approval_Docs(request, app_id):
#     response = {}
#     app = Application.objects.filter(app_id=app_id)
#     response['app'] = app[0]
#     print(app[0].attached_pdf)
#     return render(request, 'content/show_documents.html', response)

@csrf_exempt
@login_required_message(message="You should be logged in, in order to perform this")
@login_required(login_url="/login/")
def Approve(request):
    app_id = request.POST.get('id_checker')
    app = Application.objects.filter(app_id=app_id)
    app = app[0]
    print('Last Step=',app.current_step)
    app.current_step += 1
    next_id = request.POST.get('names')
    # next = CustomUser.objects.filter(id=next_id)[0]
    app.current_authority = next_id
    if app.current_step>app.max_step:
        print("Got approved")
        app.is_approved = True

    to_email = app.applicant.email
    subject = 'Application Status Updated.'
    message = 'Step: '+ app.current_step
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [to_email]
    send_mail( subject, message, email_from, recipient_list)

    app.save()
    applications = Application.objects.all()
    departments = Department.objects.all()
    response = {}
    response['applications'] = applications
    response['departments'] = departments
    designations = {'Teacher', 'Faculty Advisor', 'Dean', 'Head of Department', 'Director'}
    response['designations'] = designations
    return render(request, 'content/show_pending_approvals.html', response)


@csrf_exempt
@login_required_message(message="You should be logged in, in order to perform this")
@login_required(login_url="/login/")
def Reject(request):
    app_id = request.POST.get('id_checker')
    app_id = str(app_id).strip()
    print(app_id)
    app = Application.objects.get(pk=app_id)
    print('Rejected at Step=',app.current_step)
    app.is_rejected = True
    app.save()
    applications = Application.objects.all()
    departments = Department.objects.all()
    response = {}
    response['applications'] = applications
    response['departments'] = departments
    designations = {'Teacher', 'Faculty Advisor', 'Dean', 'Head of Department', 'Director'}
    response['designations'] = designations
    return render(request, 'content/show_pending_approvals.html', response)


@csrf_exempt
@login_required_message(message="You should be logged in, in order to perform this")
@login_required(login_url="/login/")
def Track_Application(request):
    if request.POST:
        app_id = request.POST.get('app_id')
        application = Application.objects.filter(app_id=app_id)
        for a in application:
            print(a.app_id)
        auth = CustomUser.objects.get(pk=application[0].current_authority)
        response = {
            'application': application[0],
            'auth' : auth
        }

    else:
        response = {
            'application': None,
            'auth': None
        }
    return render(request, 'application/track_application.html', response)

@csrf_exempt
@login_required_message(message="You should be logged in, in order to perform this")
@login_required(login_url="/login/")
def Track_Student_Applications(request):
    if request.POST:
        app_id = request.POST.get('app_id')
        application = Application.objects.filter(app_id=app_id)
        for a in application:
            print(a.app_id)
        response = {
            'application': application[0]
        }
    else:
        response = {
            'application': None
        }
    return render(request, 'application/track_application.html', response)

@csrf_exempt
@login_required_message(message="You should be logged in, in order to perform this")
@login_required(login_url="/login/")
def Add_Scholarship(request):
    user = CustomUser.objects.get(pk=request.user.id)
    response = {}
    if user.role == "Admin":
        return render(request, 'content/add_scholarship.html', response)
    else:
        if user.is_student:
            return render(request, 'student_home.html', response)
        else:
            return render(request, 'staff_home.html', response)

