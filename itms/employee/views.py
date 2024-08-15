from datetime import datetime
from decimal import *
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from account.app_functions import employee_account_needed, employee_leave_company
from account.models import Account, AccountType

from home.app_function import check_permission, get_paginated_obj, json_error, json_success
from employee.models import Employee, EmployeeAsset
from department.models import CostCenter
from logs.models import EmployeeLog


# Create your views here.
@login_required
def employee_list(request):
    can_view, msg = check_permission(request.user, "employee.view_employee")
    if not can_view:
        messages.error(request, f"You do no have permission to view Employee. {msg}")
        return redirect("home")
    context = {}
    employee_set = Employee.objects.all().order_by("department__cc_name", "first_name", "last_name")

    curr_search = request.GET.get("search", "").strip()
    if curr_search:
        employee_set = employee_set.filter(
            Q(employee_id__icontains=curr_search)
            | Q(first_name__icontains=curr_search)
            | Q(middle_name__icontains=curr_search)
            | Q(preferred_name__icontains=curr_search)
            | Q(last_name__icontains=curr_search)
            # | Q(join_date__icontains=curr_search)
            # | Q(leave_date__icontains=curr_search)
            | Q(department__cc_name__icontains=curr_search)
            | Q(department__cc_code__icontains=curr_search)
            | Q(supervisor__icontains=curr_search)
            | Q(active__icontains=curr_search)
        )
        context["curr_search"] = curr_search

    updated_context = get_paginated_obj(
        employee_set, request.GET.get("page_num", 1), request.GET.get("page_obj_count", 10)
    )
    context.update(updated_context)

    return render(request, "employee/employee_list.html", context)


@login_required
@csrf_exempt
def add_employee_form(request):
    can_view, msg = check_permission(request.user, "employee.change_employee")
    if not can_view:
        messages.error(request, f"You do no have permission to Add Employee. {msg}")
        return redirect("employee:employee_list")

    context = {}
    cc_set = CostCenter.objects.all().order_by("bg_name", "bu_id", "cc_name")
    account_type_list = list(AccountType.objects.values_list("account_type", flat=True))
    context["cc_set"] = cc_set
    context["account_type_list"] = account_type_list
    context["curr_date"] = datetime.now().astimezone().strftime("%Y-%m-%d")

    return render(request, "employee/add_employee_form.html", context)


@login_required
@csrf_exempt
def add_employee(request):
    can_view, msg = check_permission(request.user, "employee.change_employee")
    if not can_view:
        messages.error(request, f"You do no have permission to Add Employee. {msg}")
        return redirect("employee:employee_list")
    context = {}

    user_name = request.user.username

    employee_id = request.POST.get("employee_id", "").strip()
    first_name = request.POST.get("first_name", "").strip().capitalize()
    preferred_name = request.POST.get("preferred_name", "").strip().capitalize()
    middle_name = request.POST.get("middle_name", "").strip().capitalize()
    last_name = request.POST.get("last_name", "").strip().capitalize()
    join_date = request.POST.get("join_date", "").strip()
    department = request.POST.get("department", "").strip()
    supervisor = request.POST.get("supervisor", "").strip()
    account_type_list = request.POST.getlist("account_type", [])

    if not department:
        messages.error(request, "Please Select Department. ")
        return redirect("employee:employee_list")

    cc_ref = CostCenter.objects.filter(cc_code=department).first()
    if not cc_ref:
        messages.error(request, f"CC {department} does not exist. ")
        return redirect("employee:employee_list")

    if join_date:
        join_date = datetime.strptime(join_date, "%Y-%m-%d").astimezone()
    else:
        join_date = None

    employee_ref = Employee.objects.filter(employee_id=employee_id).first()
    if employee_ref:
        messages.error(request, f"Employee ID:{employee_id} {employee_ref.name} already exists. ")
        return redirect("employee:employee_list")

    Employee.objects.create(
        employee_id=employee_id,
        first_name=first_name,
        preferred_name=preferred_name,
        middle_name=middle_name,
        last_name=last_name,
        join_date=join_date,
        department=cc_ref,
        supervisor=supervisor,
        active=True,
    )

    # create_log
    EmployeeLog.create_log(
        "Add",
        employee_id,
        f"{first_name} {middle_name}, {last_name} ({preferred_name})",
        f"{cc_ref.cc_code}--{cc_ref.cc_name} ({supervisor})",
        user_name,
        f"{join_date.strftime('%D')}, account_needed: {', '.join(account_type_list)}",
    )

    if account_type_list:
        employee_account_needed(employee_id, account_type_list, request.get_host())

    messages.success(request, f"Employee {employee_id} added successfully.")
    return redirect("employee:employee_list")


@login_required
@csrf_exempt
def edit_employee_form(request, employee_id):
    can_view, msg = check_permission(request.user, "employee.change_employee")
    if not can_view:
        messages.error(request, f"You do no have permission to Edit Employee. {msg}")
        return redirect("employee:employee_list")

    context = {}
    employee_ref = Employee.objects.filter(employee_id=employee_id).first()
    context["employee_ref"] = employee_ref

    cc_set = CostCenter.objects.all().order_by("bg_name", "bu_id", "cc_name")
    context["cc_set"] = cc_set

    employee_account_set = Account.objects.filter(employee_id=employee_id).order_by("id")
    employee_no_account_list = list(
        AccountType.objects.exclude(account_type__in=employee_account_set.values("account_type")).values_list(
            "account_type", flat=True
        )
    )
    context["asset_set"] = EmployeeAsset.objects.filter(employee=employee_ref).order_by("-id")
    context["employee_account_set"] = employee_account_set
    context["employee_no_account_list"] = employee_no_account_list
    return render(request, "employee/edit_employee_form.html", context)


@login_required
@csrf_exempt
def edit_employee(request):
    can_view, msg = check_permission(request.user, "employee.change_employee")
    if not can_view:
        messages.error(request, f"You do no have permission to Edit Employee. {msg}")
        return redirect("employee:employee_list")
    context = {}

    user_name = request.user.username

    employee_id = request.POST.get("employee_id", "").strip()
    first_name = request.POST.get("first_name", "").strip()
    preferred_name = request.POST.get("preferred_name", "").strip()
    middle_name = request.POST.get("middle_name", "").strip()
    last_name = request.POST.get("last_name", "").strip()
    join_date = request.POST.get("join_date", "").strip()
    department = request.POST.get("department", "").strip()
    supervisor = request.POST.get("supervisor", "").strip()
    account_type_list = request.POST.getlist("account_type", [])

    if not department:
        messages.error(request, "Please Select Department. ")
        return redirect("employee:employee_list")

    cc_ref = CostCenter.objects.filter(cc_code=department).first()
    if not cc_ref:
        messages.error(request, f"CC {department} does not exist. ")
        return redirect("employee:employee_list")

    if join_date:
        join_date = datetime.strptime(join_date, "%Y-%m-%d").astimezone()
    else:
        join_date = None

    employee_ref = Employee.objects.filter(employee_id=employee_id).first()
    if not employee_ref:
        messages.error(request, f"Employee {employee_id} does not exist. ")
        return redirect("employee:employee_list")

    employee_ref.employee_id = employee_id
    employee_ref.first_name = first_name
    employee_ref.middle_name = middle_name
    employee_ref.last_name = last_name
    employee_ref.join_date = join_date
    employee_ref.department = cc_ref
    employee_ref.supervisor = supervisor
    employee_ref.preferred_name = preferred_name

    employee_ref.save()
    # employee_ref.refresh_from_db()

    # create_log
    EmployeeLog.create_log(
        "Add",
        employee_id,
        f"{first_name} {middle_name}, {last_name} ({preferred_name})",
        f"{cc_ref.cc_code}--{cc_ref.cc_name} ({supervisor})",
        user_name,
        f"{join_date.strftime('%D')}, account_needed: {', '.join(account_type_list)}",
    )

    if account_type_list:
        employee_account_needed(employee_id, account_type_list, request.get_host())

    messages.success(request, f"Employee {employee_id} edited successfully.")
    return redirect("employee:employee_list")


@login_required
@csrf_exempt
def delete_employee(request):
    can_act, msg = check_permission(request.user, "asset.change_employee")
    if not can_act:
        return json_error(request, f"You do no have permission to delete Employee. {msg}")

    user_name = request.user.username

    employee_id = request.POST.get("employee_id", "").strip()
    comment = request.POST.get("comment", "").strip()

    employee_ref = Employee.objects.filter(employee_id=employee_id).first()
    if not employee_ref:
        return json_error(f"Employee {employee_id} does not exist. ")

    # create_log
    EmployeeLog.create_log(
        "Delete",
        employee_id,
        f"{employee_ref.first_name} {employee_ref.middle_name}, {employee_ref.last_name} ({employee_ref.preferred_name})",
        f"{employee_ref.department.cc_code}--{employee_ref.department.cc_name} ({employee_ref.supervisor})",
        user_name,
        f"{employee_ref.join_date.strftime('%D')}-{datetime.now().strftime('%D')}, Comment: {comment}",
    )

    employee_ref.delete()
    return json_success(f"Employee {employee_id} deleted successfully.")


@login_required
@csrf_exempt
def deactivate_employee(request):
    can_act, msg = check_permission(request.user, "asset.change_employee")
    if not can_act:
        return json_error(f"You do no have permission to delete Employee. {msg}")

    user_name = request.user.username

    employee_id = request.POST.get("employee_id", "").strip()
    comment = request.POST.get("comment", "").strip()

    employee_ref = Employee.objects.filter(employee_id=employee_id).first()
    if not employee_ref:
        return json_error(f"Employee {employee_id} does not exist. ")

    # create_log
    EmployeeLog.create_log(
        "Deactivate",
        employee_id,
        f"{employee_ref.name}",
        f"{employee_ref.department.cc_name}",
        user_name,
        f"{employee_ref.join_date.strftime('%D')}-{datetime.now().strftime('%D')}, Comment: {comment}",
    )

    employee_leave_company(user_name, employee_id, request.get_host())
    employee_ref.active = False
    employee_ref.leave_date = datetime.now().astimezone()
    employee_ref.save()
    return json_success(f"Employee {employee_id} deactivated successfully.")


@login_required
@csrf_exempt
def activate_employee(request):
    can_act, msg = check_permission(request.user, "asset.change_employee")
    if not can_act:
        return json_error(f"You do no have permission to delete Employee. {msg}")

    user_name = request.user.username

    employee_id = request.POST.get("employee_id", "").strip()
    comment = request.POST.get("comment", "").strip()

    employee_ref = Employee.objects.filter(employee_id=employee_id).first()
    if not employee_ref:
        return json_error(f"Employee {employee_id} does not exist. ")

    # create_log
    EmployeeLog.create_log(
        "Activate",
        employee_id,
        f"{employee_ref.name}",
        f"{employee_ref.department.cc_name}",
        user_name,
        f"{employee_ref.join_date.strftime('%D')}-{datetime.now().strftime('%D')}, Comment: {comment}",
    )

    employee_ref.active = True
    employee_ref.leave_date = None
    employee_ref.save()

    return json_success(f"Employee {employee_id} reactivate successfully. ")


@login_required
def employee_overview(request, employee_id):
    context = {}
    employee_ref = Employee.objects.filter(employee_id=employee_id).first()
    employee_account_set = Account.objects.filter(employee_id=employee_id).order_by("id")

    context["employee_ref"] = employee_ref
    context["employee_account_set"] = employee_account_set
    context["asset_set"] = EmployeeAsset.objects.filter(employee=employee_ref).order_by("-id")

    return render(request, "employee/employee_overview.html", context)
