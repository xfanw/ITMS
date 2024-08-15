from django.urls import path
from .views import *

app_name = "admin_itms"

# Account List
urlpatterns = [
    path("", admin_home, name="admin_home"),
    path("admin_reset_user_password", admin_reset_user_password, name="admin_reset_user_password"),
    path("admin_reset_password", admin_reset_password, name="admin_reset_password"),
]

urlpatterns += [
    path("admin_auth", admin_auth, name="admin_auth"),
    path("admin_add_user_auth", admin_add_user_auth, name="admin_add_user_auth"),
    path("admin_remove_user_auth", admin_remove_user_auth, name="admin_remove_user_auth"),
]

urlpatterns += [
    path("admin_auth_group", admin_auth_group, name="admin_auth_group"),
    path("admin_create_group_auth", admin_create_group_auth, name="admin_create_group_auth"),
    path("admin_add_group_auth", admin_add_group_auth, name="admin_add_group_auth"),
    path("admin_remove_group_auth", admin_remove_group_auth, name="admin_remove_group_auth"),
]
