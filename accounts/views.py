from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.views import generic
from django.contrib.auth import authenticate, login, logout
# from django.http import HttpResponse
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import  json
from content.decorators import login_required_message
# from django.shortcuts import resolve_url
# from django.conf import settings
# from django.utils.decorators import method_decorator
# from django.views.decorators.csrf import csrf_protect
# from django.views.generic.base import TemplateView
# from django.views.decorators.debug import sensitive_post_parameters
# from django.contrib.auth.tokens import default_token_generator
# from django.views.decorators.cache import never_cache
# from django.views.generic import UpdateView
from django.utils.http import is_safe_url
# from content.views import logout, checkuserifscrutinyuser
# from django.template.loader import render_to_string
# from base64 import urlsafe_b64encode
# from django.contrib.sites.shortcuts import get_current_site
# from django.utils.encoding import force_bytes, force_text
# from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
# from django.views.generic.edit import FormView
# from django.contrib.auth.forms import (
#     AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm,
# )

from .admin import UserCreationForm, StaffCreationForm
from django.contrib import messages
from .models import *
from django.core.mail import EmailMessage


def index(request):
    response = {}
    print(request.user, " logged in : RENDER HOME ")
    user = CustomUser.objects.filter(id=request.user.id)
    print("User : ",user)
    if not user or (user and user[0].is_student):
        return render(request, 'student_home.html', response)

    else:
        return render(request, 'staff_home.html', response)


class UserFormView(generic.View):
    form_class = UserCreationForm
    template_name = 'accounts/student_register.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            user = form.save(commit=False)
            print(user)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user.set_password(password)
            user.save()
            # current_site = get_current_site(request)
            # mail_subject = 'Activate your NITADDA account.'
            # to_email = form.cleaned_data.get('email')
            # email = EmailMessage(
            #     mail_subject, message, to=[to_email]
            # )
            # email.content_subtype = 'html'
            # try:
            #     email.send()
            #     messages.success(request,
            #                      f'Your account has been created and you are logged in.Please confirm your email address to complete the registration')
            # except:
            #     messages.success(request, f'Please enter valid email for registration')
            return redirect('/')

        return render(request, self.template_name, {'form': form})

class StaffFormView(generic.View):
    form_class = StaffCreationForm
    template_name = 'accounts/staff_register.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            user = form.save(commit=False)
            print(user)
            user.is_student = False
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user.set_password(password)
            user.save()
            return redirect('/')

        return render(request, self.template_name, {'form': form})


# class UserUpdateFormView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
#     model = CustomUser
#     fields = ['email', 'first_name', 'last_name', 'mobile', 'gender', 'image']
#     template_name = 'account/registration_form.html'
#
#     def form_valid(self, form):
#         form.instance.by = str(self.request.user)
#         messages.success(self.request, f'Your account has been updated!')
#         return super().form_valid(form)
#
#     def test_func(self):
#         customUser = str(self.get_object())
#         user = str(self.request.user)
#         if user == customUser:
#             return True
#         return False

@csrf_exempt
def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return HttpResponseRedirect('/login/')

@csrf_exempt
def user_login(request):
    response = {}
    if request.user.is_authenticated:
        logout(request)
    else:
        response = {}
    if request.method == 'POST':
        next_post = request.POST.get('next')
        redirect_path = next_post
        username = request.POST['username']
        try:
            username = CustomUser.objects.get(email=username).username
        except CustomUser.DoesNotExist:
            username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, 'You have been successfully logged in.')
                if is_safe_url(redirect_path, request.get_host()):
                    return redirect(redirect_path)
                else:
                    return redirect('accounts:index')
            else:
                messages.warning(request, 'User is not active yet')
                response['message'] = 'User is not active yet'
        else:
            messages.warning(request, 'User is invalid')
            response['message'] = 'User is invalid'

    return render(request, 'accounts/login.html', response)

@csrf_exempt
def getNames(request):
    print("INSIDE GET NAMES")
    if request.method == 'POST':
        designation = request.POST.get('d')
        result_set = []
        trimmed_role= str(designation).strip()
        all_users = CustomUser.objects.filter(role=trimmed_role, is_student=False)
        print('..',trimmed_role,'..')
        for user in all_users:
            print(user.first_name,' ', user.id)
            result_set.append({'first_name': user.first_name,'last_name': user.last_name, 'id': user.id})
        return HttpResponse(json.dumps(result_set), content_type='application/json')

    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )

@csrf_exempt
@login_required_message(message="You should be logged in, in order to perform this")
@login_required(login_url="/login/")
def Activate_Users(request):
    users = CustomUser.objects.all()
    response = {}
    response['users'] = users
    return render(request, 'accounts/activate_users.html', response)

@csrf_exempt
@login_required_message(message="You should be logged in, in order to perform this")
@login_required(login_url="/login/")
def Activate(request, uid):
    user = CustomUser.objects.get(pk=uid)
    user.is_active = True
    user.save()
    response = {}
    users = CustomUser.objects.all()
    response['users'] = users
    print("activate")
    return render(request, 'accounts/activate_users.html', response)

@csrf_exempt
@login_required_message(message="You should be logged in, in order to perform this")
@login_required(login_url="/login/")
def Deactivate(request, uid):
    user = CustomUser.objects.get(pk=uid)
    user.is_active = False
    user.save()
    response = {}
    users = CustomUser.objects.all()
    response['users'] = users
    print("deactivate")
    return render(request, 'accounts/activate_users.html', response)