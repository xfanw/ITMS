from django.urls import path
from .views import *

app_name = "employee"

urlpatterns = [
    path("employee_list", employee_list, name="employee_list"),
    path("add_employee_form", add_employee_form, name="add_employee_form"),
    path("add_employee", add_employee, name="add_employee"),
    path("edit_employee_form/<slug:employee_id>", edit_employee_form, name="edit_employee_form"),
    path("edit_employee", edit_employee, name="edit_employee"),
    path("delete_employee", delete_employee, name="delete_employee"),
    path("deactivate_employee", deactivate_employee, name="deactivate_employee"),
    path("activate_employee", activate_employee, name="activate_employee"),
    path("employee_overview/<slug:employee_id>", employee_overview, name="employee_overview"),
]
