from django.urls import path
from .views import *

app_name = "asset"

urlpatterns = [
    path("laptop", laptop, name="laptop"),
    path("add_laptop", add_laptop, name="add_laptop"),
    path("upload_laptop_file", upload_laptop_file, name="upload_laptop_file"),
    path("edit_laptop", edit_laptop, name="edit_laptop"),
    path("delete_laptop", delete_laptop, name="delete_laptop"),
]

urlpatterns += [
    path("monitor", monitor, name="monitor"),
    path("add_monitor", add_monitor, name="add_monitor"),
    path("upload_monitor_file", upload_monitor_file, name="upload_monitor_file"),
    path("edit_monitor", edit_monitor, name="edit_monitor"),
    path("delete_monitor", delete_monitor, name="delete_monitor"),
]

urlpatterns += [
    path("asset_assign", asset_assign, name="asset_assign"),
    path("assign_asset_action", assign_asset_action, name="assign_asset_action"),
    path("delete_asset_action", delete_asset_action, name="delete_asset_action"),
    path("replace_asset_action", replace_asset_action, name="replace_asset_action"),
]

urlpatterns += [
    path("employee_asset_overview/<slug:employee_id>", employee_asset_overview, name="employee_asset_overview"),
    path("print_asset_hand_receipt/<slug:employee_id>", print_asset_hand_receipt, name="print_asset_hand_receipt"),
]
