from django.urls import path
from .views import *

app_name = "logs"
urlpatterns = [
    path("cost_center_log", cost_center_log, name="cost_center_log"),
    path("business_unit_log", business_unit_log, name="business_unit_log"),
]
