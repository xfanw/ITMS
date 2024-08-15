"""
    Part 1: Cost Center
        cost_center
        add_cost_center
        edit_cost_center
        delete_cost_center
    
    Part 2: Business Unit
        business_unit
        add_business_unit
        edit_business_unit
        delete_business_unit
    
    Part 3: Business Group  (Pending)
        business_group
        add_business_group
        edit_business_group
        delete_business_group
    
    Part 4: Legal Entity (Pending)
        legal_entity
        add_legal_entity
        edit_legal_entity
        delete_legal_entity


"""

from datetime import datetime
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages

from department.models import BusinessUnit, CostCenter, BusinessGroup
from home.app_function import check_permission, get_paginated_obj
from logs.models import CostCenterLog, BusinessUnitLog

"""
    Part 1: Cost Center
        cost_center
        add_cost_center
        edit_cost_center
        delete_cost_center
"""


@login_required
def cost_center(request):
    can_view, msg = check_permission(request.user, "department.view_costcenter")
    if not can_view:
        messages.error(request, f"You do no have permission to View Cost Center. {msg}")
        return redirect("home")
    context = {}
    cost_center_set = CostCenter.objects.order_by("bg_name", "bu_id", "cc_name")

    curr_search = request.GET.get("search", "").strip()
    if curr_search:
        cost_center_set = cost_center_set.filter(
            Q(cc_code__icontains=curr_search)
            | Q(cc_name__icontains=curr_search)
            | Q(cc_manager__icontains=curr_search)
            | Q(bu_name__icontains=curr_search)
            | Q(bg_name__icontains=curr_search)
            | Q(le_name__icontains=curr_search)
        )
        context["curr_search"] = curr_search

    updated_context = get_paginated_obj(
        cost_center_set, request.GET.get("page_num", 1), request.GET.get("page_obj_count", 10)
    )
    context.update(updated_context)

    context["bu_name_list"] = list(BusinessUnit.objects.order_by("bu_name").values_list("bu_name", flat=True))

    return render(request, "department/cost_center.html", context)


@login_required
@csrf_exempt
def add_cost_center(request):
    can_act, msg = check_permission(request.user, "department.change_costcenter")
    if not can_act:
        messages.error(request, f"You do no have permission to Add Cost Center. {msg}")
        return redirect("department:cost_center")

    cc_code = request.POST.get("cc_code", "").strip()
    cc_name = request.POST.get("cc_name", "").strip()
    cc_manager = request.POST.get("cc_manager", "").strip()
    bu_name = request.POST.get("bu_name", "").strip()
    user_name = request.user.username
    # curr_time = datetime.now().astimezone()

    if not cc_code:
        messages.error(request, "CC Code cannot be empty. ")
        return redirect("department:cost_center")

    cc_ref = CostCenter.objects.filter(cc_code=cc_code).first()
    if cc_ref:
        messages.error(request, f"CC {cc_code}[{cc_ref.cc_name}] is already exist. ")
        return redirect("department:cost_center")

    bu_ref = BusinessUnit.objects.filter(bu_name=bu_name).first()
    if bu_ref:
        bg_name = bu_ref.bg_name
        le_name = bu_ref.le_name
    else:
        bg_name = ""
        le_name = ""

    CostCenter.objects.create(
        cc_code=cc_code,
        cc_name=cc_name,
        cc_manager=cc_manager,
        bu=bu_ref,
        bu_name=bu_name,
        bg_name=bg_name,
        le_name=le_name,
    )

    CostCenterLog.create_log("Add", cc_code, user_name, f"{cc_name}({cc_manager}): {bu_name}")

    messages.success(request, f"CC {cc_code} added successfully.")
    return redirect(f"/department/cost_center?search={cc_code}")


@login_required
@csrf_exempt
def edit_cost_center(request):
    can_act, msg = check_permission(request.user, "department.change_costcenter")
    if not can_act:
        messages.error(request, f"You do no have permission to Edit Cost Center. {msg}")
        return redirect("department:cost_center")

    cc_code = request.POST.get("cc_code", "").strip()
    cc_name = request.POST.get("cc_name", "").strip()
    cc_manager = request.POST.get("cc_manager", "").strip()
    bu_name = request.POST.get("bu_name", "").strip()
    user_name = request.user.username
    # curr_time = datetime.now().astimezone()

    if not cc_code:
        messages.error(request, "CC Code cannot be empty. ")
        return redirect("department:cost_center")

    cc_ref = CostCenter.objects.filter(cc_code=cc_code).first()
    if not cc_ref:
        messages.error(request, f"CC {cc_code}[{cc_ref.cc_name}] does not exist. ")
        return redirect("department:cost_center")

    old_cc_name, old_bu_name, old_cc_manager = cc_ref.cc_name, cc_ref.bu_name, cc_ref.cc_manager

    bu_ref = BusinessUnit.objects.filter(bu_name=bu_name).first()

    if bu_ref:
        bg_name = bu_ref.bg_name
        le_name = bu_ref.le_name
    else:
        bg_name = ""
        le_name = ""

    CostCenter.objects.filter(cc_code=cc_code).update(
        cc_code=cc_code,
        cc_name=cc_name,
        cc_manager=cc_manager,
        bu=bu_ref,
        bu_name=bu_name,
        bg_name=bg_name,
        le_name=le_name,
    )

    CostCenterLog.create_log(
        "Edit",
        cc_code,
        user_name,
        f"{old_cc_name}({old_cc_manager}): {old_bu_name} --> {cc_name}({cc_manager}):{bu_name}",
    )

    messages.success(request, f"CC {cc_code} edited successfully.")
    return redirect(f"/department/cost_center?search={cc_code}")


@login_required
@csrf_exempt
def delete_cost_center(request, cc_id):
    can_act, msg = check_permission(request.user, "department.change_costcenter")
    if not can_act:
        messages.error(request, f"You do no have permission to Delete Cost Center. {msg}")
        return redirect("department:cost_center")

    user_name = request.user.username

    cc_ref = CostCenter.objects.filter(id=cc_id).first()
    cc_code = cc_ref.cc_code
    CostCenterLog.create_log(
        "Delete",
        cc_code,
        user_name,
        f"{cc_ref.cc_name}({cc_ref.cc_manager}): {cc_ref.bu_name}: {cc_ref.bg_name}: {cc_ref.le_name}",
    )

    cc_ref.delete()
    messages.success(request, f"CC {cc_code} deleted successfully.")
    return redirect("department:cost_center")


"""
    Part 2: Business Unit
        business_unit
        add_business_unit
        edit_business_unit
        delete_business_unit
"""


@login_required
def business_unit(request):
    can_view, msg = check_permission(request.user, "department.view_businessunit")
    if not can_view:
        messages.error(request, f"You do no have permission to View Business Unit. {msg}")
        return redirect("home")
    context = {}
    business_unit_set = BusinessUnit.objects.order_by("bg_name", "bu_name")

    curr_search = request.GET.get("search", "").strip()
    if curr_search:
        business_unit_set = business_unit_set.filter(
            Q(bu_name__icontains=curr_search)
            | Q(bu_manager__icontains=curr_search)
            | Q(bg_name__icontains=curr_search)
            | Q(le_name__icontains=curr_search)
        )
        context["curr_search"] = curr_search

    updated_context = get_paginated_obj(
        business_unit_set, request.GET.get("page_num", 1), request.GET.get("page_obj_count", 10)
    )
    context.update(updated_context)

    context["bg_name_list"] = list(BusinessGroup.objects.order_by("bg_name").values_list("bg_name", flat=True))

    return render(request, "department/business_unit.html", context)


@login_required
@csrf_exempt
def add_business_unit(request):
    can_act, msg = check_permission(request.user, "department.change_businessunit")
    if not can_act:
        messages.error(request, f"You do no have permission to Add Business Unit. {msg}")
        return redirect("department:business_unit")

    bu_name = request.POST.get("bu_name", "").strip()
    bg_name = request.POST.get("bg_name", "").strip()
    bu_manager = request.POST.get("bu_manager", "").strip()
    le_name = request.POST.get("le_name", "").strip()
    user_name = request.user.username
    # curr_time = datetime.now().astimezone()

    if not bg_name:
        messages.error(request, "Business Group cannot be empty. ")
        return redirect("department:business_unit")

    if not bu_name:
        messages.error(request, "Business Unit cannot be empty. ")
        return redirect("department:business_unit")

    bu_ref = BusinessUnit.objects.filter(bu_name=bu_name).first()
    if bu_ref:
        messages.error(request, f"Business Unit {bu_name} is already exist. ")
        return redirect("department:business_unit")

    bg_ref = BusinessGroup.objects.filter(bg_name=bg_name).first()
    if bg_ref:
        le_name = bg_ref.le.le_name
    else:
        le_name = ""

    BusinessUnit.objects.create(
        bu_name=bu_name,
        bg_name=bg_name,
        bg=bg_ref,
        bu_manager=bu_manager,
        le_name=le_name,
    )

    BusinessUnitLog.create_log("Add", bu_name, user_name, f"{bu_manager}, {bg_name}, {le_name}")

    messages.success(request, f"BU {bu_name} added successfully.")
    return redirect(f"/department/business_unit?search={bu_name}")


@login_required
@csrf_exempt
def edit_business_unit(request):
    can_act, msg = check_permission(request.user, "department.change_businessunit")
    if not can_act:
        messages.error(request, f"You do no have permission to Edit Business Unit. {msg}")
        return redirect("department:business_unit")

    bu_name = request.POST.get("bu_name", "").strip()
    bg_name = request.POST.get("bg_name", "").strip()
    bu_manager = request.POST.get("bu_manager", "").strip()
    user_name = request.user.username
    # curr_time = datetime.now().astimezone()

    bu_ref = BusinessUnit.objects.filter(bu_name=bu_name).first()
    if not bu_ref:
        messages.error(request, f"BU {bu_name} does not exist. ")
        return redirect("department:business_unit")

    bg_ref = BusinessGroup.objects.filter(bg_name=bg_name).first()
    if bg_ref:
        le_name = bg_ref.le.le_name
    else:
        le_name = ""

    BusinessUnit.objects.filter(bu_name=bu_name).update(
        bu_name=bu_name,
        bg_name=bg_name,
        bg=bg_ref,
        bu_manager=bu_manager,
        le_name=le_name,
    )

    BusinessUnitLog.create_log("Edit", bu_name, user_name, f"{bu_manager}, {bg_name}, {le_name}")

    messages.success(request, f"BU {bu_name} edited successfully.")
    return redirect(f"/department/business_unit?search={bu_name}")


@login_required
@csrf_exempt
def delete_business_unit(request, bu_id):
    can_act, msg = check_permission(request.user, "department.change_businessunit")
    if not can_act:
        messages.error(request, f"You do no have permission to Delete Business Unit. {msg}")
        return redirect("department:business_unit")

    user_name = request.user.username

    bu_ref = BusinessUnit.objects.filter(id=bu_id).first()
    bu_name = bu_ref.bu_name

    BusinessUnitLog.create_log(
        "Delete", bu_name, user_name, f"{bu_ref.bu_manager}, {bu_ref.bg_name}, {bu_ref.le_name}"
    )

    bu_ref.delete()
    messages.success(request, f"BU {bu_name} deleted successfully.")
    return redirect("department:business_unit")
