from django.urls import path
from .views import *

app_name = "account"

# Account List
urlpatterns = [
    path("account_assign", account_assign, name="account_assign"),
    path("assign_account_action", assign_account_action, name="assign_account_action"),
    path("delete_account_action", delete_account_action, name="delete_account_action"),
]

# Account Type
urlpatterns += [
    path("account_type", account_type, name="account_type"),
    path("add_account_type", add_account_type, name="add_account_type"),
    path("edit_account_type", edit_account_type, name="edit_account_type"),
    path("delete_account_type/<slug:account_type_id>", delete_account_type, name="delete_account_type"),
]
