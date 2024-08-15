from datetime import datetime
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.models import User

from department.models import BusinessUnit, CostCenter
from home.app_function import check_permission, get_paginated_obj
from logs.models import CostCenterLog, BusinessUnitLog


# Create your views here.
@login_required
def cost_center_log(request):
    context = {}
    curr_search = request.GET.get("search", "").strip()
    cc_log_set = CostCenterLog.objects.filter(cc_code__icontains=curr_search).order_by("-id")

    if curr_search and not cc_log_set.exists():
        messages.error(request, f"No logs for {curr_search}. ")

    # 3. add paginator
    updated_context = get_paginated_obj(
        cc_log_set, request.GET.get("page_num", 1), request.GET.get("page_obj_count", 17)
    )
    context = {"curr_search": curr_search, **updated_context}
    return render(request, "logs/department/cost_center_log.html", context)


@login_required
def business_unit_log(request):
    context = {}
    curr_search = request.GET.get("search", "").strip()
    bu_log_set = BusinessUnitLog.objects.filter(bu_name__icontains=curr_search).order_by("-id")

    if curr_search and not bu_log_set.exists():
        messages.error(request, f"No logs for {curr_search}. ")

    # 3. add paginator
    updated_context = get_paginated_obj(
        bu_log_set, request.GET.get("page_num", 1), request.GET.get("page_obj_count", 17)
    )
    context = {"curr_search": curr_search, **updated_context}
    return render(request, "logs/department/business_unit_log.html", context)