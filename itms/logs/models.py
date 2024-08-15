""" 
    Log System:
    UserActionDateMemo is base model for all Logs
    All Logs should have a static method called create_log(action, other_parameters, user_name, memo)

    Part 1: Department Log
        CostCenterLog
        BusinessUnitLog
        BusinessGroupLog
        LegalEntityLog

    Part 2: Asset Log
        AssetAssignLog
        LaptopLog
        MonitorLog
        OtherAssetLog
        SubAssetLog
    
    Part 3: Employee Log
        EmployeeLog
    
    Part 4: Account Log
        AccoutTypeLog
        AccountAssignLog

    
"""

from django.db import models

from employee.models import Employee


# Create your models here.
class UserActionDateMemo(models.Model):
    """Notice: This is a real Example of how to use Abstract Class"""

    action = models.CharField(max_length=31, null=True)
    user = models.CharField(max_length=255, null=True)
    date = models.DateTimeField(auto_now_add=True)
    memo = models.TextField(null=True)

    class Meta:
        abstract = True


class CostCenterLog(UserActionDateMemo):
    cc_code = models.CharField(max_length=15, null=True)

    @staticmethod
    def create_log(action, cc_code, user_name, memo):
        CostCenterLog.objects.create(action=action, cc_code=cc_code, user=user_name, memo=memo)


class BusinessUnitLog(UserActionDateMemo):
    bu_name = models.CharField(max_length=15, null=True)

    @staticmethod
    def create_log(action, bu_name, user_name, memo):
        BusinessUnitLog.objects.create(action=action, bu_name=bu_name, user=user_name, memo=memo)


class BusinessGroupLog(UserActionDateMemo):
    bg_name = models.CharField(max_length=15, null=True)

    @staticmethod
    def create_log(action, user_name, memo):
        BusinessGroupLog.objects.create(action=action, user=user_name, memo=memo)


class LegalEntityLog(UserActionDateMemo):
    le_name = models.CharField(max_length=15, null=True)

    @staticmethod
    def create_log(action, user_name, memo):
        LegalEntityLog.objects.create(action=action, user=user_name, memo=memo)


class AssetAssignLog(UserActionDateMemo):
    employee_id = models.CharField(max_length=127, null=True)
    employee_name = models.CharField(max_length=127, null=True)
    asset_type = models.CharField(max_length=127)
    asset_serial_number = models.CharField(max_length=127)
    asset_label = models.CharField(max_length=127)
    # action : Add Remove
    # memeo: reason

    @staticmethod
    def create_log(
        action,
        employee_id,
        employee_name,
        asset_type,
        asset_serial_number,
        asset_label,
        user_name,
        memo,
    ):
        AssetAssignLog.objects.create(
            action=action,
            employee_id=employee_id,
            employee_name=employee_name,
            asset_type=asset_type,
            asset_serial_number=asset_serial_number,
            asset_label=asset_label,
            user=user_name,
            memo=memo,
        )


class LaptopLog(UserActionDateMemo):
    asset_label = models.CharField(max_length=127, null=True)
    serial_number = models.CharField(max_length=127, null=True)

    @staticmethod
    def create_log(action, asset_label, serial_number, user_name, memo):
        LaptopLog.objects.create(
            action=action, asset_label=asset_label, serial_number=serial_number, user=user_name, memo=memo
        )


class MonitorLog(UserActionDateMemo):
    asset_label = models.CharField(max_length=127, null=True)
    serial_number = models.CharField(max_length=127, null=True)

    @staticmethod
    def create_log(action, asset_label, serial_number, user_name, memo):
        MonitorLog.objects.create(
            action=action, asset_label=asset_label, serial_number=serial_number, user=user_name, memo=memo
        )


class AssetLog(UserActionDateMemo):
    asset_type = models.CharField(max_length=127, null=True)
    asset_label = models.CharField(max_length=127, null=True)
    serial_number = models.CharField(max_length=127, null=True)

    @staticmethod
    def create_log(action, asset_type, asset_label, serial_number, user_name, memo):
        AssetLog.objects.create(
            action=action,
            asset_type=asset_type,
            asset_label=asset_label,
            serial_number=serial_number,
            user=user_name,
            memo=memo,
        )


class EmployeeLog(UserActionDateMemo):
    employee_id = models.CharField(max_length=31)
    employee_name = models.CharField(max_length=255, null=True)
    department = models.CharField(max_length=127, null=True)
    # action: Add, Edit, Delete
    # memo: account_type

    @staticmethod
    def create_log(action, employee_id, employee_name, department, user_name, memo):
        EmployeeLog.objects.create(
            action=action,
            employee_id=employee_id,
            employee_name=employee_name,
            department=department,
            user=user_name,
            memo=memo,
        )


class AccountTypeLog(UserActionDateMemo):
    # action: Create, Edit, Delete

    @staticmethod
    def create_log(action, user_name, memo):
        AccountTypeLog.objects.create(
            action=action,
            user=user_name,
            memo=memo,
        )


class AccountAssignLog(UserActionDateMemo):
    # action: Create, Edit, Delete
    account_type = models.CharField(max_length=127, null=True)
    employee_id = models.CharField(max_length=127, null=True)

    @staticmethod
    def create_log(action, employee_id, account_type, user_name, memo):
        AccountAssignLog.objects.create(
            action=action,
            account_type=account_type,
            employee_id=employee_id,
            user=user_name,
            memo=memo,
        )


class AdminLog(UserActionDateMemo):
    target_user = models.CharField(max_length=127)

    @staticmethod
    def create_log(action, target_user, user_name, memo):
        AdminLog.objects.create(
            action=action,
            target_user=target_user,
            user=user_name,
            memo=memo,
        )
