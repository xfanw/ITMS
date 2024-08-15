"""
    Part 1: Account Type maintaince
        account_type
        add_account_type
        edit_account_type
        delete_account_type
    
    Part 2: Account Assign 

"""

from datetime import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt

from django.db.models import Q
from account.models import Account, AccountType
from home.app_function import check_permission, get_paginated_obj, json_success
from logs.models import AccountAssignLog, AccountTypeLog


"""
    Part 1: Account Type maintaince
        account_type
        add_account_type
        edit_account_type
        delete_account_type
"""


@login_required
def account_type(request):
    context = {}
    account_type_set = AccountType.objects.order_by("-id").prefetch_related("account_set")
    context["account_type_set"] = account_type_set
    return render(request, "account/account_type.html", context)


@login_required
@csrf_exempt
def add_account_type(request):
    can_act, msg = check_permission(request.user, "account.change_accounttype")
    if not can_act:
        messages.error(request, f"You do no have permission to change acount type. {msg}")
        return redirect("account:account_type")

    account_type = request.POST.get("account_type", "").strip()
    person_in_charge = request.POST.get("person_in_charge", "").strip()
    pic_email = request.POST.get("pic_email", "").strip()
    user_name = request.user.username

    if not account_type or not person_in_charge or not pic_email:
        messages.error(request, f"All fields are needed. ")
        return redirect("account:account_type")

    account_type_ref = AccountType.objects.filter(account_type=account_type).first()
    if account_type_ref:
        messages.error(request, f"{account_type} already exists. ")
        return redirect("account:account_type")

    AccountType.objects.create(
        account_type=account_type, person_in_charge=person_in_charge, pic_email=pic_email, updater=user_name
    )
    AccountTypeLog.create_log("Create", user_name, f"{account_type}:{person_in_charge}:{pic_email}")
    return redirect("account:account_type")


@login_required
@csrf_exempt
def edit_account_type(request):
    can_act, msg = check_permission(request.user, "account.change_accounttype")
    if not can_act:
        messages.error(request, f"You do no have permission to change acount type. {msg}")
        return redirect("account:account_type")

    account_type = request.POST.get("account_type", "").strip()
    person_in_charge = request.POST.get("person_in_charge", "").strip()
    pic_email = request.POST.get("pic_email", "").strip()
    user_name = request.user.username

    if not account_type or not person_in_charge or not pic_email:
        messages.error(request, f"All fields are needed. ")
        return redirect("account:account_type")

    account_type_ref = AccountType.objects.filter(account_type=account_type).first()
    if not account_type_ref:
        messages.error(request, f"{account_type} does not exist. ")
        return redirect("account:account_type")

    AccountType.objects.filter(
        account_type=account_type,
    ).update(person_in_charge=person_in_charge, pic_email=pic_email, updater=user_name)

    AccountTypeLog.create_log("Edit", user_name, f"{account_type}:{person_in_charge}:{pic_email}")

    return redirect("account:account_type")


@login_required
@csrf_exempt
def delete_account_type(request, account_type_id):
    can_act, msg = check_permission(request.user, "account.change_accounttype")
    if not can_act:
        messages.error(request, f"You do no have permission to change acount type. {msg}")
        return redirect("account:account_type")

    user_name = request.user.username

    account_type_ref = AccountType.objects.filter(id=account_type_id).first()
    if not account_type_ref:
        messages.error(request, f"{account_type_ref.account_type} does not exist. ")
        return redirect("account:account_type")

    account_type = account_type_ref.account_type
    AccountTypeLog.create_log(
        "Edit",
        user_name,
        f"{account_type}:{account_type_ref.person_in_charge}:{account_type_ref.pic_email}",
    )

    account_type_ref.delete()
    messages.success(request, f"{account_type} deleted successfully.")
    return redirect("account:account_type")


"""
    Part 2: Account Assign 
        account_assign
"""


@login_required
def account_assign(request):
    context = {}
    # can_view = check_permission(request.user, "account.view_account")
    # if not can_view:
    #     messages.error(request, f"You do no have permission to view account page. ")
    #     return redirect("home")

    account_set = Account.objects.order_by("-id").prefetch_related("employee", "employee__department")

    curr_search = request.GET.get("search", "").strip()
    if curr_search:
        account_set = account_set.filter(
            Q(employee__employee_id__icontains=curr_search)
            | Q(employee__first_name__icontains=curr_search)
            | Q(employee__preferred_name__icontains=curr_search)
            | Q(employee__middle_name__icontains=curr_search)
            | Q(employee__last_name__icontains=curr_search)
            | Q(account_type__account_type__icontains=curr_search)
            | Q(employee__department__cc_code__icontains=curr_search)
            | Q(employee__department__cc_name__icontains=curr_search)
        )
        context["curr_search"] = curr_search

    updated_context = get_paginated_obj(
        account_set, request.GET.get("page_num", 1), request.GET.get("page_obj_count", 17)
    )
    context.update(updated_context)

    return render(request, "account/account_assign.html", context)


@login_required
@csrf_exempt
def assign_account_action(request):
    can_act, msg = check_permission(request.user, "account.change_account")
    if not can_act:
        messages.error(request, f"You do no have permission to assign account. {msg}")
        return redirect("account:account_assign")

    account_id = request.POST.get("account_id", "")
    employee_name = request.POST.get("employee", "")
    account_type = request.POST.get("account_type", "")
    account = request.POST.get("account", "").strip()
    user_name = request.user.username

    if not account_id or not account:
        messages.error(request, f"Missing account ID or detail. ")
        return redirect("account:account_assign")

    account_ref = Account.objects.filter(id=account_id).first()

    if not account_ref or account_ref.employee.name != employee_name or account_ref.account_type_id != account_type:
        messages.error(request, f"Information mismatch, refresh page and try again. ")
        return redirect("account:account_assign")

    Account.objects.filter(id=account_id).update(
        account=account, create_person=user_name, create_date=datetime.now().astimezone()
    )

    if account_type == "MS Account":
        employee_ref = account_ref.employee
        employee_ref.email = account
        employee_ref.save()

    AccountAssignLog.create_log("Assign", account_ref.employee_id, account_type, user_name, account)
    return redirect(f"/account/account_assign?search={account_ref.employee_id}")


@login_required
@csrf_exempt
def delete_account_action(request):
    can_act, msg = check_permission(request.user, "account.change_account")
    if not can_act:
        messages.error(request, f"You do no have permission to delete accout. {msg}")
        return redirect("account:account_assign")

    account_id = request.POST.get("account_id", "")
    user_name = request.user.username

    if not account_id:
        messages.error(request, f"Missing account ID. ")
        return redirect("account:account_assign")

    account_ref = Account.objects.filter(id=account_id).first()

    AccountAssignLog.create_log(
        "Delete", account_ref.employee_id, account_ref.account_type_id, user_name, account_ref.account
    )

    account_ref.delete()

    return redirect(f"/account/account_assign?search={account_ref.employee_id}")
