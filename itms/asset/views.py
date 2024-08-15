from datetime import datetime
from decimal import *
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from asset.app_function import (
    assign_asset_to_user,
    check_asset,
    remove_asset_from_user,
    laptop_file_handling,
    check_laptop_add,
    check_monitor_add,
    monitor_file_handling,
)

from home.app_function import check_permission, get_paginated_obj, json_error, json_success
from employee.models import Employee, EmployeeAsset
from asset.models import Laptop, Monitor
from logs.models import LaptopLog, MonitorLog, AssetAssignLog


# Create your views here.
@login_required
def laptop(request):
    # can_view = check_permission(request.user, "asset.view_laptop")
    # if not can_view:
    #     messages.error(request, f"You do no have permission to view Laptop. ")
    #     return redirect("home")
    context = {}
    laptop_set = Laptop.objects.all().order_by("status", "brand", "asset_label")

    curr_search = request.GET.get("search", "").strip()
    if curr_search:
        laptop_set = laptop_set.filter(
            Q(asset_type__icontains=curr_search)
            | Q(asset_label__icontains=curr_search)
            | Q(brand__icontains=curr_search)
            | Q(model__icontains=curr_search)
            | Q(serial_number__icontains=curr_search)
            | Q(purchase_date__icontains=curr_search)
            | Q(purchase_cost__icontains=curr_search)
            | Q(status__icontains=curr_search)
            | Q(processor__icontains=curr_search)
            | Q(ram__icontains=curr_search)
            | Q(storage__icontains=curr_search)
        )
        context["curr_search"] = curr_search

    updated_context = get_paginated_obj(
        laptop_set, request.GET.get("page_num", 1), request.GET.get("page_obj_count", 10)
    )
    context.update(updated_context)

    return render(request, "asset/laptop.html", context)


@login_required
@csrf_exempt
def add_laptop(request):
    can_act, msg = check_permission(request.user, "asset.change_asset")
    if not can_act:
        messages.error(request, f"You do no have permission to add Laptop. {msg}")
        return redirect("asset:laptop")

    user_name = request.user.username

    asset_type = request.POST.get("asset_type", "").strip()
    asset_label = request.POST.get("asset_label", "").strip()
    brand = request.POST.get("brand", "").strip()
    model = request.POST.get("model", "").strip()
    serial_number = request.POST.get("serial_number", "").strip()
    processor = request.POST.get("processor", "").strip()
    ram = request.POST.get("ram", "").strip()
    storage = request.POST.get("storage", "").strip()
    purchase_date = request.POST.get("purchase_date", "").strip()
    purchase_cost = request.POST.get("purchase_cost", "").strip()

    status, msg, purchase_date, purchase_cost = check_laptop_add(
        ram, storage, purchase_date, purchase_cost, asset_label, serial_number
    )
    if status == "error":
        messages.error(request, msg)
        return redirect("asset:laptop")

    laptop_ref = Laptop.objects.filter(asset_label=asset_label).first()
    if laptop_ref:
        messages.error(request, f"Laptop {asset_label} already exists, use edit button. ")
        return redirect("asset:laptop")

    Laptop.objects.create(
        asset_type=asset_type,
        asset_label=asset_label,
        brand=brand,
        model=model,
        serial_number=serial_number,
        processor=processor,
        ram=ram,
        storage=storage,
        purchase_date=purchase_date,
        purchase_cost=purchase_cost,
        status="IDLE",
    )

    # create_log
    LaptopLog.create_log(
        "Add",
        asset_label,
        serial_number,
        user_name,
        f"{brand}, {model}, {processor}, {ram}, {storage}, {purchase_date}, {purchase_cost}, IDLE",
    )

    messages.success(request, f"Laptop {asset_label} added successfully.")
    return redirect("asset:laptop")


@login_required
@csrf_exempt
def upload_laptop_file(request):
    laptop_file = request.FILES["laptop_file"] if "laptop_file" in request.FILES else None
    user_name = request.user.username
    status, msg = laptop_file_handling(laptop_file, user_name)
    if status == "error":
        messages.error(request, msg)

    return redirect("asset:laptop")


@login_required
@csrf_exempt
def edit_laptop(request):
    can_act, msg = check_permission(request.user, "asset.change_asset")
    if not can_act:
        messages.error(request, f"You do no have permission to edit Laptop. {msg}")
        return redirect("asset:laptop")

    user_name = request.user.username

    asset_label = request.POST.get("asset_label", "").strip()
    brand = request.POST.get("brand", "").strip()
    model = request.POST.get("model", "").strip()
    serial_number = request.POST.get("serial_number", "").strip()
    processor = request.POST.get("processor", "").strip()
    ram = request.POST.get("ram", "").strip()
    storage = request.POST.get("storage", "").strip()
    purchase_date = request.POST.get("purchase_date", "").strip()
    purchase_cost = request.POST.get("purchase_cost", "").strip()
    status = request.POST.get("status", "").strip()

    if len(ram) > 15 or len(storage) > 15:
        messages.error(request, "Ram and Storage should not exceeds the allowed range. ")
        return redirect("asset:laptop")

    if purchase_date:
        purchase_date = datetime.strptime(purchase_date, "%Y-%m-%d").astimezone()
    else:
        purchase_date = None

    if purchase_cost:
        purchase_cost = Decimal(purchase_cost)
        if abs(purchase_cost) >= 10**6:
            messages.error(request, "Purchase Cost should not exceeds the allowed range. ")
            return redirect("asset:laptop")
    else:
        purchase_cost = 0

    if not asset_label:
        messages.error(request, "Asset Label cannot be empty. ")
        return redirect("asset:laptop")

    if not serial_number:
        messages.error(request, "SN cannot be empty. ")
        return redirect("asset:laptop")

    laptop_ref = Laptop.objects.filter(asset_label=asset_label).first()
    if not laptop_ref:
        messages.error(request, f"Laptop {asset_label} does not exist. ")
        return redirect("asset:laptop")

    msg = ""
    # if laptop_ref.status == "IN_USE" and (status == "IDLE" or status == "RETIRED"):
    #     employee_ref = Employee.objects.filter(laptop__asset_label=asset_label).first()
    #     employee_ref.laptop = None
    #     employee_ref.save()
    #     msg = f"(Employee {employee_ref.employee_id} lose Laptop {asset_label})"

    laptop_ref.asset_label = asset_label
    laptop_ref.brand = brand
    laptop_ref.model = model
    laptop_ref.serial_number = serial_number
    laptop_ref.processor = processor
    laptop_ref.ram = ram
    laptop_ref.storage = storage
    laptop_ref.purchase_date = purchase_date
    laptop_ref.purchase_cost = purchase_cost
    if status:
        laptop_ref.status = status
    else:
        status = laptop_ref.status

    laptop_ref.save()
    laptop_ref.refresh_from_db()

    # create_log
    LaptopLog.create_log(
        "Edit",
        asset_label,
        serial_number,
        user_name,
        f"{brand}, {model}, {processor}, {ram}, {storage}, {purchase_date}, {purchase_cost}, {status + msg}",
    )

    messages.success(request, f"Laptop {asset_label} edited successfully. " + msg)
    return redirect("asset:laptop")


@login_required
@csrf_exempt
def delete_laptop(request):
    can_act, msg = check_permission(request.user, "asset.change_asset")
    if not can_act:
        return json_error(f"You do no have permission to delete Laptop. {msg}")

    user_name = request.user.username

    laptop_id = request.POST.get("laptop_id", "").strip()
    comment = request.POST.get("comment", "").strip()

    laptop_ref = Laptop.objects.filter(id=laptop_id).first()
    if not laptop_ref:
        return json_error(f"Laptop {laptop_id} does not exist. ")

    # create_log
    LaptopLog.create_log(
        "Delete",
        laptop_ref.asset_label,
        laptop_ref.serial_number,
        user_name,
        f"comment: ({comment}), {laptop_ref.brand}, {laptop_ref.model},\
        {laptop_ref.processor}, {laptop_ref.ram}, {laptop_ref.storage}, {laptop_ref.purchase_date}, {laptop_ref.purchase_cost}, {laptop_ref.status}",
    )

    laptop_ref.delete()
    return json_success(f"Laptop {laptop_ref.asset_label} deleted successfully.")


# Create your views here.
@login_required
def monitor(request):
    # can_view = check_permission(request.user, "asset.view_monitor")
    # if not can_view:
    #     messages.error(request, f"You do no have permission to view Monitor. ")
    #     return redirect("home")
    context = {}
    monitor_set = Monitor.objects.all().order_by("status", "brand", "asset_label")

    curr_search = request.GET.get("search", "").strip()
    if curr_search:
        monitor_set = monitor_set.filter(
            Q(asset_type__icontains=curr_search)
            | Q(asset_label__icontains=curr_search)
            | Q(brand__icontains=curr_search)
            | Q(model__icontains=curr_search)
            | Q(serial_number__icontains=curr_search)
            | Q(purchase_date__icontains=curr_search)
            | Q(purchase_cost__icontains=curr_search)
            | Q(status__icontains=curr_search)
            | Q(screen_size__icontains=curr_search)
            | Q(resolution__icontains=curr_search)
        )
        context["curr_search"] = curr_search

    updated_context = get_paginated_obj(
        monitor_set, request.GET.get("page_num", 1), request.GET.get("page_obj_count", 10)
    )
    context.update(updated_context)

    return render(request, "asset/monitor.html", context)


@login_required
@csrf_exempt
def add_monitor(request):
    can_act, msg = check_permission(request.user, "asset.change_asset")
    if not can_act:
        messages.error(request, f"You do no have permission to add Monitor. {msg}")
        return redirect("asset:monitor")

    user_name = request.user.username

    asset_type = request.POST.get("asset_type", "").strip()
    asset_label = request.POST.get("asset_label", "").strip()
    brand = request.POST.get("brand", "").strip()
    model = request.POST.get("model", "").strip()
    serial_number = request.POST.get("serial_number", "").strip()
    screen_size = request.POST.get("screen_size", "").strip()
    resolution = request.POST.get("resolution", "").strip()
    purchase_date = request.POST.get("purchase_date", "").strip()
    purchase_cost = request.POST.get("purchase_cost", "").strip()

    status, msg, screen_size, purchase_date, purchase_cost = check_monitor_add(
        screen_size, resolution, purchase_date, purchase_cost, asset_label, serial_number
    )
    if status == "error":
        messages.error(request, msg)
        return redirect("asset:monitor")

    monitor_ref = Monitor.objects.filter(asset_label=asset_label).first()
    if monitor_ref:
        messages.error(request, f"Monitor {asset_label} already exists, use edit button. ")
        return redirect("asset:monitor")

    Monitor.objects.create(
        asset_type=asset_type,
        asset_label=asset_label,
        brand=brand,
        model=model,
        serial_number=serial_number,
        screen_size=screen_size,
        resolution=resolution,
        purchase_date=purchase_date,
        purchase_cost=purchase_cost,
        status="IDLE",
    )

    # create_log
    MonitorLog.create_log(
        "Add",
        asset_label,
        serial_number,
        user_name,
        f"{brand}, {model}, {resolution}, {screen_size}, {purchase_date}, {purchase_cost}, IDLE",
    )

    messages.success(request, f"Monitor {asset_label} added successfully.")
    return redirect("asset:monitor")


@login_required
@csrf_exempt
def upload_monitor_file(request):
    monitor_file = request.FILES["monitor_file"] if "monitor_file" in request.FILES else None
    user_name = request.user.username
    status, msg = monitor_file_handling(monitor_file, user_name)
    if status == "error":
        messages.error(request, msg)

    return redirect("asset:monitor")


@login_required
@csrf_exempt
def edit_monitor(request):
    can_act, msg = check_permission(request.user, "asset.change_asset")
    if not can_act:
        messages.error(request, f"You do no have permission to edit Monitor. {msg}")
        return redirect("asset:monitor")

    user_name = request.user.username

    asset_label = request.POST.get("asset_label", "").strip()
    brand = request.POST.get("brand", "").strip()
    model = request.POST.get("model", "").strip()
    serial_number = request.POST.get("serial_number", "").strip()
    screen_size = request.POST.get("screen_size", "").strip()
    resolution = request.POST.get("resolution", "").strip()
    purchase_date = request.POST.get("purchase_date", "").strip()
    purchase_cost = request.POST.get("purchase_cost", "").strip()
    status = request.POST.get("status", "").strip()

    if not screen_size:
        messages.error(request, "Please select a Screen Scize. ")
        return redirect("asset:monitor")
    else:
        screen_size = int(screen_size)

    if not resolution:
        messages.error(request, "Please select a Resolution. ")
        return redirect("asset:monitor")

    if purchase_date:
        purchase_date = datetime.strptime(purchase_date, "%Y-%m-%d").astimezone()
    else:
        purchase_date = None

    if purchase_cost:
        purchase_cost = Decimal(purchase_cost)
        if abs(purchase_cost) >= 10**6:
            messages.error(request, "Purchase Cost should not exceeds the allowed range. ")
            return redirect("asset:monitor")
    else:
        purchase_cost = 0

    if not asset_label:
        messages.error(request, "Asset Label cannot be empty. ")
        return redirect("asset:monitor")

    if not serial_number:
        messages.error(request, "SN cannot be empty. ")
        return redirect("asset:monitor")

    monitor_ref = Monitor.objects.filter(asset_label=asset_label).first()
    if not monitor_ref:
        messages.error(request, f"Monitor {asset_label} does not exist. ")
        return redirect("asset:monitor")

    msg = ""
    # if monitor_ref.status == "IN_USE" and (status == "IDLE" or status == "RETIRED"):
    #     employee_ref = Employee.objects.filter(monitor__asset_label=asset_label).first()
    #     employee_ref.monitor = None
    #     employee_ref.save()
    #     msg = f"(Employee {employee_ref.employee_id} lose Monitor {asset_label})"

    monitor_ref.asset_label = asset_label
    monitor_ref.brand = brand
    monitor_ref.model = model
    monitor_ref.serial_number = serial_number
    monitor_ref.screen_size = screen_size
    monitor_ref.resolution = resolution
    monitor_ref.purchase_date = purchase_date
    monitor_ref.purchase_cost = purchase_cost
    if status:
        monitor_ref.status = status
    else:
        status = monitor_ref.status

    monitor_ref.save()
    monitor_ref.refresh_from_db()

    # create_log
    MonitorLog.create_log(
        "Edit",
        asset_label,
        serial_number,
        user_name,
        f"{brand}, {model}, {screen_size}, {resolution}, {purchase_date}, {purchase_cost}, {status + msg}",
    )

    messages.success(request, f"Monitor {asset_label} edited successfully. " + msg)
    return redirect("asset:monitor")


@login_required
@csrf_exempt
def delete_monitor(request):
    can_act, msg = check_permission(request.user, "asset.change_asset")
    if not can_act:
        return json_error(f"You do no have permission to delete Monitor. {msg}")

    user_name = request.user.username

    monitor_id = request.POST.get("monitor_id", "").strip()
    comment = request.POST.get("comment", "").strip()

    monitor_ref = Monitor.objects.filter(id=monitor_id).first()
    if not monitor_ref:
        return json_error(f"Monitor {monitor_id} does not exist. ")

    # create_log
    MonitorLog.create_log(
        "Delete",
        monitor_ref.asset_label,
        monitor_ref.serial_number,
        user_name,
        f"comment: ({comment}), {monitor_ref.brand}, {monitor_ref.model},\
        {monitor_ref.screen_size}, {monitor_ref.resolution}, {monitor_ref.purchase_date}, {monitor_ref.purchase_cost}, {monitor_ref.status}",
    )

    monitor_ref.delete()
    return json_success(f"Monitor {monitor_ref.asset_label} deleted successfully.")


@login_required
def asset_assign(request):
    context = {}
    # can_view = check_permission(request.user, "asset.view_laptop") and check_permission(
    #     request.user, "asset.view_monitor"
    # )
    # if not can_view:
    #     messages.error(request, f"You do no have permission to view assign asset page. ")
    #     return redirect("home")

    employee_set = (
        Employee.objects.all()
        # .select_related("laptop", "monitor")
        .order_by("department__cc_name", "first_name", "last_name")
    )

    curr_search = request.GET.get("search", "").strip()
    if curr_search:
        employee_set = employee_set.filter(
            Q(employee_id__icontains=curr_search)
            | Q(first_name__icontains=curr_search)
            | Q(preferred_name__icontains=curr_search)
            | Q(middle_name__icontains=curr_search)
            | Q(last_name__icontains=curr_search)
            # | Q(laptop__asset_label__icontains=curr_search)
            # | Q(monitor__asset_label__icontains=curr_search)
            | Q(department__cc_code__icontains=curr_search)
            | Q(department__cc_name__icontains=curr_search)
        )
        context["curr_search"] = curr_search

    updated_context = get_paginated_obj(
        employee_set, request.GET.get("page_num", 1), request.GET.get("page_obj_count", 17)
    )
    context.update(updated_context)

    return render(request, "asset/asset_assign.html", context)


@login_required
@csrf_exempt
def assign_asset_action(request):
    can_act, msg = check_permission(request.user, "asset.change_asset")
    if not can_act:
        messages.error(request, f"You do no have permission to assign assset. {msg}")
        return redirect("asset:asset_assign")

    employee_id = request.POST.get("employee_id", "")
    asset_label = request.POST.get("asset_label", "").strip()
    user_name = request.user.username

    if not asset_label:
        messages.error(request, f"Please Scan Asset Label. ")
        return redirect("asset:asset_assign")

    employee_ref = Employee.objects.filter(employee_id=employee_id).first()
    if not employee_ref:
        messages.error(request, f"Employee {employee_id} does not exist. ")
        return redirect("asset:asset_assign")

    asset_ref = check_asset(asset_label)
    if not asset_ref:
        messages.error(request, f"Asset {asset_label} does not exist. ")
        return redirect("asset:asset_assign")

    if asset_ref.status != "IDLE":
        messages.error(request, f"Asset {asset_label} status is not IDLE. ")
        return redirect("asset:asset_assign")

    assign_asset_to_user(employee_ref, asset_ref, user_name)

    return redirect(f"/asset/asset_assign?search={employee_id}")


@login_required
@csrf_exempt
def delete_asset_action(request):
    can_act, msg = check_permission(request.user, "asset.change_asset")
    if not can_act:
        messages.error(request, f"You do no have permission to assign assset. {msg}")
        return redirect("asset:asset_assign")

    employee_id = request.POST.get("employee_id", "")
    asset_label = request.POST.get("asset_label", "").strip()
    user_name = request.user.username

    employee_ref = Employee.objects.filter(employee_id=employee_id).first()
    if not employee_ref:
        messages.error(request, f"Employee {employee_id} does not exist. ")
        return redirect("asset:asset_assign")

    if not asset_label:
        messages.error(request, f"Please Scan Asset Label. ")
        return redirect("asset:employee_asset_overview", employee_id)

    asset_ref = check_asset(asset_label)
    if not asset_ref:
        messages.error(request, f"Asset {asset_label} does not exist. ")
        return redirect("asset:employee_asset_overview", employee_id)

    if asset_ref.status != "IN_USE":
        messages.error(request, f"Asset {asset_label} status is not IN_USE. ")
        return redirect("asset:employee_asset_overview", employee_id)

    remove_asset_from_user(employee_ref, asset_ref, user_name)

    return redirect("asset:employee_asset_overview", employee_id)


@login_required
@csrf_exempt
def replace_asset_action(request):
    can_act, msg = check_permission(request.user, "asset.change_asset")
    if not can_act:
        messages.error(request, f"You do no have permission to assign assset. {msg}")
        return redirect("asset:asset_assign")

    employee_id = request.POST.get("employee_id", "")
    asset_label = request.POST.get("asset_label", "").strip()
    old_asset_label = request.POST.get("old_asset_label", "").strip()
    user_name = request.user.username

    employee_ref = Employee.objects.filter(employee_id=employee_id).first()
    if not employee_ref:
        messages.error(request, f"Employee {employee_id} does not exist. ")
        return redirect("asset:asset_assign")

    if not old_asset_label:
        messages.error(request, f"Please Scan Asset Label. ")
        return redirect("asset:employee_asset_overview", employee_id)

    old_asset_ref = check_asset(old_asset_label)
    if not old_asset_ref:
        messages.error(request, f"Prev Asset {old_asset_label} does not exist. ")
        return redirect("asset:employee_asset_overview", employee_id)

    if old_asset_ref.status != "IN_USE":
        messages.error(request, f"Prev Asset {old_asset_label} status is not IN_USE. ")
        return redirect("asset:employee_asset_overview", employee_id)

    new_asset_ref = check_asset(asset_label)
    if not new_asset_ref:
        messages.error(request, f"New Asset {asset_label} does not exist. ")
        return redirect("asset:employee_asset_overview", employee_id)

    if new_asset_ref.status != "IDLE":
        messages.error(request, f"New Asset {asset_label} status is not IDLE. ")
        return redirect("asset:employee_asset_overview", employee_id)

    remove_asset_from_user(employee_ref, old_asset_ref, user_name)
    assign_asset_to_user(employee_ref, new_asset_ref, user_name)

    return redirect("asset:employee_asset_overview", employee_id)


@login_required
def employee_asset_overview(request, employee_id):
    context = {}
    employee_ref = Employee.objects.filter(employee_id=employee_id).first()
    if not employee_ref:
        messages.error(request, f"Employee {employee_id} does not exist. ")
        return redirect("asset:assign_asset")

    context["employee_ref"] = employee_ref
    context["asset_set"] = EmployeeAsset.objects.filter(employee=employee_ref).order_by("-id")

    return render(request, "asset/employee_asset_overview.html", context)


@login_required
def print_asset_hand_receipt(request, employee_id):
    employee_ref = Employee.objects.filter(employee_id=employee_id).first()
    if not employee_ref:
        messages.error(request, f"Employee {employee_id} does not exist. ")
        return redirect("asset:employee_asset_overview")
    context = {}
    context["employee_ref"] = employee_ref
    context["curr_time"] = datetime.now().astimezone().strftime("%D %T")
    context["asset_set"] = EmployeeAsset.objects.filter(employee=employee_ref).order_by("-id")

    return render(request, "asset/print_asset_hand_receipt.html", context)
