from datetime import datetime
from django.contrib import messages
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt

from django.db.models import Q
from account.models import Account, AccountType
from home.app_function import check_admin_permission, check_permission, get_paginated_obj, json_error, json_success
from logs.models import AdminLog


# Create your views here.
@login_required
def admin_home(request):
    can_act = check_admin_permission(request.user)
    if not can_act:
        messages.error(request, f"You do no have admin permission.")
        return redirect("home")

    context = {}
    return render(request, "admin_itms/admin_home.html", context)


@login_required
def admin_reset_user_password(request):
    """Password Reset

    Args:
        request: front end request

    Returns:
        HTML page
    """
    if not check_admin_permission(request.user):
        return redirect("admin_itms:admin_home")

    search_val = request.GET.get("search", "").strip()

    context = {"curr_search": search_val, "action": "Action Password Reset"}

    if search_val:
        context["user_list"] = User.objects.filter(
            Q(username__icontains=search_val)
            | Q(first_name__icontains=search_val)
            | Q(last_name__icontains=search_val)
            | Q(profile__department__icontains=search_val)
            | Q(email__icontains=search_val)
        ).order_by("-id")
    return render(request, "admin_itms/admin_reset_user_password.html", context)


@login_required
def admin_reset_password(request):
    if not check_admin_permission(request.user):
        return json_error("You cannot reset password for other user accounts. ")

    user_id = request.POST.get("user_id", "")
    password = request.POST.get("password", "")

    user = User.objects.filter(id=user_id).first()
    if user:
        user.set_password(password)
        user.save()
        msg = f'Reset success. Account: "{user.username}", Password: "{password}". '
        AdminLog.create_log("Reset Password", user.username, request.user.username, msg)
        return json_success(msg)
    else:
        return json_error("User is not in CIMS. ")


@login_required
def admin_auth(request):
    if not check_admin_permission(request.user):
        return redirect("admin_itms:admin_home")

    group_list = Group.objects.exclude(name__icontains="admin").order_by("id")
    search_val = request.GET.get("search", "").strip()
    group_name = request.GET.get("group_name", "").strip()

    context = {
        "group_list": group_list,
        "curr_search": search_val,
        "curr_group": group_name,
        "action": "Action Editing User Auth",
    }

    if group_name:
        group_user_list = User.objects.filter(groups__name=group_name)
        context["group_user_list"] = group_user_list

    if search_val:
        context["user_list"] = User.objects.filter(
            Q(username__icontains=search_val)
            | Q(first_name__icontains=search_val)
            | Q(last_name__icontains=search_val)
            | Q(profile__department__icontains=search_val)
            | Q(email__icontains=search_val)
        ).order_by("-id")

    return render(request, "admin_itms/admin_auth.html", context)


@login_required
def admin_add_user_auth(request):
    """Bind user email to a function

    Args:
        request: ajax

    Returns:
        json response
    """
    if not check_admin_permission(request.user):
        return json_error("You do not have permission to bind email")

    user_id = request.GET.get("user_id", "").strip()
    user_ref = User.objects.filter(id=user_id).first()
    user_name = request.user.username

    if not user_ref:
        return json_error(f"User does not exist in CIMS. ")

    group_name = request.GET.get("auth_group", "").strip()
    group_ref = Group.objects.filter(name=group_name).first()

    if not group_ref:
        return json_error(f"Auth Group does not exist in CIMS. ")

    if user_ref.groups.filter(name=group_name).exists():
        return json_error(f"Email {user_ref.email} is already in Auth Group {group_name}. ")

    user_ref.groups.add(group_ref)

    AdminLog.create_log(f"Add User Auth", group_name, user_name, f"Add {user_ref.username}")

    return json_success(f"Add User {user_ref.username} to {group_name} successfully. ")


@login_required
def admin_remove_user_auth(request):
    """Remove bound user email from a function

    Args:
        request: ajax

    Returns:
        json response
    """
    if not check_admin_permission(request.user):
        return json_error("You do not have permission to remove bound email. ")

    user_id = request.GET.get("user_id", "").strip()
    user_ref = User.objects.filter(id=user_id).first()
    user_name = request.user.username

    if not user_ref:
        return json_error(f"User does not exist in CIMS. ")

    group_name = request.GET.get("auth_group", "").strip()
    group_ref = Group.objects.filter(name=group_name).first()

    user_ref.groups.remove(group_ref)
    AdminLog.create_log(f"Remove User Auth", group_name, user_name, f"Remove {user_ref.username}")

    return json_success(f"Remove User {user_ref.username} from {group_name} successfully. ")


@login_required
def admin_auth_group(request):
    if not check_admin_permission(request.user):
        return redirect("admin_itms:admin_home")

    group_list = Group.objects.order_by("name")
    search_val = request.GET.get("search", "").strip()
    group_name = request.GET.get("group_name", "").strip()

    context = {
        "group_list": group_list,
        "curr_search": search_val,
        "curr_group": group_name,
        "action": "Action Editing User Auth",
    }
    permission_set = None
    if search_val:
        permission_set = (
            Permission.objects.filter(content_type_id__gt=6)
            .filter(
                Q(name__icontains=search_val)
                | Q(codename__icontains=search_val)
                | Q(content_type__app_label__icontains=search_val)
                | Q(content_type__model__icontains=search_val)
            )
            .exclude(codename__icontains="delete")
            .exclude(codename__icontains="add")
            .order_by("id")
        )

    if group_name:
        group_ref = Group.objects.filter(name=group_name).first()
        if not group_ref:
            return json_error(f"Auth Group {group_name} does not exist in CIMS. ")

        group_perm_set = group_ref.permissions.order_by("id")
        if permission_set:
            permission_set = permission_set.exclude(id__in=group_ref.permissions.values_list("id"))
        context["group_perm_list"] = group_perm_set

    context["permission_list"] = permission_set

    return render(request, "admin_itms/admin_auth_group.html", context)


@login_required
def admin_create_group_auth(request):
    if not check_admin_permission(request.user):
        return redirect("admin_itms:admin_home")

    group_name = request.GET.get("new_group_name", "").strip()

    Group.objects.update_or_create(name=group_name)

    return redirect(f"/admin_itms/admin_auth_group?group_name={group_name}")


@login_required
def admin_add_group_auth(request):
    """Bind user email to a function

    Args:
        request: ajax

    Returns:
        json response
    """
    if not check_admin_permission(request.user):
        return json_error("You do not have permission to bind email")

    user_name = request.user.username

    perm_id = request.GET.get("perm_id", "").strip()
    perm_ref = Permission.objects.filter(id=perm_id).first()
    if not perm_ref:
        return json_error(f"Permission does not exist in CIMS. ")

    group_name = request.GET.get("auth_group", "").strip()
    if not group_name:
        return json_error(f"Select Group before continue. ")

    group_ref = Group.objects.filter(name=group_name).first()
    if not group_ref:
        return json_error(f"Auth Group {group_name} does not exist in CIMS. ")

    if group_ref.permissions.filter(id=perm_id):
        return json_error(f"Permission {perm_ref.codename} is already in Group {group_name}. ")

    group_ref.permissions.add(perm_ref)

    AdminLog.create_log(f"Add Group Auth", group_name, user_name, f"Add {perm_ref.codename}")

    return json_success(f"Add permission {perm_ref.codename} to {group_name} successfully. ")


@login_required
def admin_remove_group_auth(request):
    """Remove bound user email from a function

    Args:
        request: ajax

    Returns:
        json response
    """
    if not check_admin_permission(request.user):
        return json_error("You do not have permission to bind email")

    user_name = request.user.username

    perm_id = request.GET.get("perm_id", "").strip()
    perm_ref = Permission.objects.filter(id=perm_id).first()
    if not perm_ref:
        return json_error(f"Permission does not exist in CIMS. ")

    group_name = request.GET.get("auth_group", "").strip()
    if not group_name:
        return json_error(f"Select Group before continue. ")

    group_ref = Group.objects.filter(name=group_name).first()
    if not group_ref:
        return json_error(f"Auth Group {group_name} does not exist in CIMS. ")

    if not group_ref.permissions.filter(id=perm_id):
        return json_error(f"Permission {perm_ref.codename} is not in Group {group_name}. ")

    group_ref.permissions.remove(perm_ref)

    AdminLog.create_log(f"Remove Group Auth", group_name, user_name, f"Remove {perm_ref.codename}")

    return json_success(f"Remove permission {perm_ref.codename} from {group_name} successfully. ")
