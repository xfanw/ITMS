from time import sleep
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash

from home.form import ChangePasswordForm, SignUpForm
from home.models import UserProfile


# Create your views here.
def itms_login(request):
    if request.POST:
        user = authenticate(username=request.POST.get("username"), password=request.POST.get("password"))
        if user:
            login(request, user)
            return redirect(request.POST.get("next", "home"))
        else:
            messages.error(request, "Username/Password Incorect.")

    return render(request, "account/login.html", {"next": request.GET.get("next", "home")})


def itms_logout(request):
    logout(request)
    return redirect("home")


def itms_signup(request):
    user_form = SignUpForm()
    if request.POST:
        user_form = SignUpForm(request.POST)
        if user_form.is_valid():
            user_ref = user_form.save()
            UserProfile.objects.create(user=user_ref, department=request.POST.get("department", ""))
            login(request, user_ref)
            return redirect("home")

    return render(request, "account/signup.html", {"form": user_form})


@login_required
def itms_change_password(request):
    # sleep(1000)
    password_form = ChangePasswordForm(request.user)
    if request.POST:
        password_form = ChangePasswordForm(request.user, request.POST)
        if password_form.is_valid():
            user_ref = password_form.save()
            update_session_auth_hash(request, user_ref)  # Important!
            messages.success(request, "Your password was successfully updated!")
            return redirect("home")

    return render(request, "account/change_password.html", {"form": password_form})


@login_required
def profile(request):
    if request.POST:
        login_user = request.user.username
        input_username = request.POST.get("username")
        email = request.POST.get("email", "")
        first_name = request.POST.get("firstname", "")
        last_name = request.POST.get("lastname", "")
        department = request.POST.get("department", "")
        user_ref = User.objects.filter(username=login_user).first()
        try:
            User.objects.filter(username=login_user).update(
                username=input_username, email=email, first_name=first_name, last_name=last_name
            )
            user_profile = user_ref.profile
            user_profile.department = department
            user_profile.save()

        except:
            UserProfile.objects.create(user=user_ref, department=department)

    return render(request, "account/profile.html", {})
