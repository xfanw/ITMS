from django.db import models

from employee.models import Employee

# Create your models here.


class AccountType(models.Model):
    account_type = models.CharField(max_length=127, unique=True)
    person_in_charge = models.CharField(max_length=127, null=True)
    pic_email = models.CharField(max_length=127, null=True)
    updater = models.CharField(max_length=127, null=True)
    update_date = models.DateTimeField(auto_now=True)


class Account(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    account_type = models.ForeignKey(AccountType, on_delete=models.CASCADE, to_field="account_type")
    account = models.CharField(max_length=127, null=True)
    create_date = models.DateField(null=True)
    create_person = models.CharField(max_length=127)
