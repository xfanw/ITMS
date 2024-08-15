from django.urls import path
from .views import *

app_name = "department"

# Cost Center
urlpatterns = [
    path("cost_center", cost_center, name="cost_center"),
    path("add_cost_center", add_cost_center, name="add_cost_center"),
    path("edit_cost_center", edit_cost_center, name="edit_cost_center"),
    path("delete_cost_center/<slug:cc_id>", delete_cost_center, name="delete_cost_center"),
]

# Business Unit
urlpatterns += [
    path("business_unit", business_unit, name="business_unit"),
    path("add_business_unit", add_business_unit, name="add_business_unit"),
    path("edit_business_unit", edit_business_unit, name="edit_business_unit"),
    path("delete_business_unit/<slug:bu_id>", delete_business_unit, name="delete_business_unit"),
]
