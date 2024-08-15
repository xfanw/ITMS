from django.db import models
from django.db.models import Q
from asset.models import Laptop, Monitor

from department.models import CostCenter


# Create your models here.
class Employee(models.Model):
    employee_id = models.CharField(max_length=31, primary_key=True)
    first_name = models.CharField(max_length=127)
    middle_name = models.CharField(max_length=127, null=True)
    last_name = models.CharField(max_length=127)
    preferred_name = models.CharField(max_length=127, null=True)

    join_date = models.DateTimeField(auto_now_add=True)
    leave_date = models.DateTimeField(null=True)
    active = models.BooleanField(default=True)

    department = models.ForeignKey(CostCenter, on_delete=models.SET_NULL, null=True)
    supervisor = models.CharField(max_length=127)
    email = models.CharField(max_length=127, null=True)
    # laptop = models.ForeignKey(Laptop, on_delete=models.SET_NULL, null=True)
    # monitor = models.ForeignKey(Monitor, on_delete=models.SET_NULL, null=True)

    @property
    def name(self):
        if self.preferred_name:
            return f"{self.preferred_name} {self.last_name}"

        if self.middle_name:
            return f"{self.first_name} {self.middle_name}  {self.last_name}"

        return f"{self.first_name} {self.last_name}"

    @property
    def account_dict(self):
        result = dict(
            self.account_set.exclude(Q(account__isnull=True) | Q(account="")).values_list("account_type_id", "account")
        )
        # print(result)
        return result


class EmployeeAsset(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    asset_type = models.CharField(max_length=127)
    asset_label = models.CharField(max_length=127)
    asset_serial_number = models.CharField(max_length=127)
    asset_brand = models.CharField(max_length=127, null=True)
    asset_model = models.CharField(max_length=127)
    assign_date = models.DateTimeField(auto_now_add=True)
    assign_person = models.CharField(max_length=127)
