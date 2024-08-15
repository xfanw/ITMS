"""
    Part 1: general functions shared by different module
        check_permission
        check_l6_admin_permission
        get_paginated_obj
        download_excel

    
    Part 2: JsonResponses
        json_msg
        json_error
        json_success
        
    Part 3 Impored From Other Projects
        Dashboard Core API:
            get_request_date_range(Kuan-yu Chen)
"""

# django build-in packages
from datetime import datetime, time, timedelta
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator
from django.contrib.auth.models import User, Group, Permission

from io import BytesIO as IO
import pandas as pd

"""
    Part 1: general functions shared by different module
        check_permission
        get_paginated_obj
        download_excel
"""


def check_permission(user, permission=None):
    """Check if user has permission to continue their action

    Args:
        user: django user object / request.user
        permission: django permission

    Returns:
        has_permission: Boolean

    Logic:
        the user has permission if :
        1. user is super user
        2. user has assigned permission

    """
    if user.is_anonymous:
        return False, ""

    if user.is_active and user.is_superuser:
        return True, ""

    if user.has_perm(permission):
        return True, ""
    code_name = permission.split(".")[-1]
    msg = f"Permission: {code_name}. "
    group_list = list(Group.objects.filter(permissions__codename=code_name).values_list("name", flat=True))
    if group_list:
        msg += f"Perm Group: {', '.join(group_list)}. "
    else:
        msg += "No Groups have this permission. "
    return False, msg


def check_admin_permission(user):
    if user.is_anonymous:
        return False

    if user.is_active and user.is_superuser:
        return True

    if user.groups.filter(name__in=["Admin", "Helpdesk Admin"]).exists():
        return True

    return False


def get_paginated_obj(objs, page_num=1, page_obj_count=17):
    objs = Paginator(objs, page_obj_count).get_page(page_num)
    return {"page_obj_count": page_obj_count, "objs": objs}


def gen_excel_file(sheet_data_dict, file_name):
    """Generate Excel File

    Args:
        data: object to generate from
        file_name: file name
        sheet_name: sheet name (default 'New')

    Returns:
        HttpResonse containing xlsx file

    """
    excel_file = IO()
    xlwriter = pd.ExcelWriter(excel_file, engine="xlsxwriter")

    for sheet_name, data in sheet_data_dict.items():
        my_test = pd.DataFrame(data)
        my_test.to_excel(xlwriter, sheet_name=sheet_name, index=False, header=False)
    xlwriter.save()

    excel_file.seek(0)
    response = HttpResponse(
        excel_file.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = f"attachment; filename={file_name}.xlsx"

    return response


def query_value_set_to_dict(query_set, key_field):
    return_dict = {}
    for query_ref in query_set:
        if key_field in query_ref:
            key_value = query_ref.pop(key_field)
            return_dict[key_value] = query_ref
    return return_dict


"""
    Part 2: JsonResponses
        json_msg
        json_error
        json_success
        
"""


def json_msg(status, msg, **kwargs):
    """Json Message

    Args:
        status: 'error' or 'success
        msg: message

    Returns:
        JsonResponse:  'status': status + msg
    """
    return JsonResponse({"status": status, "msg": msg})


def json_error(msg, **kwargs):
    """Json Error

    Args:
        msg: error message

    Returns:
        JsonResponse: 'status':'error' + msg
    """
    return JsonResponse({"status": "error", "msg": msg, **kwargs})


def json_success(msg="", **kwargs):
    """Json Success

    Args:
        msg (optional): success message. Defaults to ''.

    Returns:
        JsonResponse:  'status': 'success' + msg
    """
    return JsonResponse({"status": "success", "msg": msg, **kwargs})


def json_warning(msg, **kwargs):
    """Json Success

    Args:
        msg (optional): warning message. Defaults to ''.

    Returns:
        JsonResponse:  'status': 'warning' + msg
    """
    return JsonResponse({"status": "warning", "msg": msg, **kwargs})


""" 
    Part 3: Impored From Other Projects
        Dashboard Core API:
            get_request_date_range(Kuan-yu Chen)

"""


def get_request_date_range(start_datetime, end_datetime):
    """Return the datetime range within time zone info. If no time zone provided in datetime object or function parameter will use Central Time

    Args:
        start_datetime (str): Default: 2020-01-01
            str format either YYYY-mm-DD or YYYY-mm-DDTHH:MM. MM represent minutes, T is hardcoded character
        end_datetime (str): Default: Today
            str format either YYYY-mm-DD or YYYY-mm-DDTHH:MM. MM represent minutes, T is hardcoded character

    Returns:
        start_output (datetime)
        end_output (datetime)
    """

    # start datetime part
    if not start_datetime:
        start_output = datetime.strptime("2020-01-01", "%Y-%m-%d").astimezone()
    else:
        try:
            start_output = datetime.strptime(start_datetime, "%Y-%m-%d").astimezone()
        except:
            try:
                start_output = datetime.strptime(start_datetime, "%Y-%m-%dT%H:%M").astimezone()
            except:
                raise TypeError(
                    """Wrong input format for start date. Please either use
                    YYYY-mm-DD or YYYY-mm-DDTHH:MM. MM represent minutes, T is hardcoded character. """
                )

    # end datetime part
    if not end_datetime:
        end_output = datetime.now().replace(hour=23, minute=59, second=59, microsecond=999999).astimezone()

    else:
        try:
            end_output = (
                datetime.strptime(end_datetime, "%Y-%m-%d")
                .replace(hour=23, minute=59, second=59, microsecond=999999)
                .astimezone()
            )
        except Exception as e:
            try:
                end_output = datetime.strptime(end_datetime, "%Y-%m-%dT%H:%M").astimezone()
            except Exception as e2:
                raise TypeError(
                    """Wrong input format for start date. Please either use
                    YYYY-mm-DD or YYYY-mm-DDTHH:MM. MM represent minutes, T is hardcoded character. """
                )

    return start_output, end_output
