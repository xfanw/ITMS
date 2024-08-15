from django.core.mail import send_mail
from account.models import Account, AccountType
from api.email_service import ITMS_MSG, new_account_content, remove_account_content, remove_asset_content
from asset.models import Laptop
from employee.models import Employee


def employee_account_needed(employee_id, account_type_list, host):
    if not employee_id or not account_type_list:
        return "error", "No account need to be created. "

    pending_account_list = []

    for account_type in account_type_list:
        pending_account_list.append(
            Account(
                employee_id=employee_id,
                account_type_id=account_type,
            )
        )
    Account.objects.bulk_create(pending_account_list)

    account_type_set = AccountType.objects.filter(account_type__in=account_type_list)
    employee_ref = Employee.objects.filter(employee_id=employee_id).first()

    email_ref = ITMS_MSG(host=host, title="New Account Needed")
    email_ref.set_email(list(account_type_set.values_list("pic_email", flat=True)))

    email_ref.build_content(new_account_content, employee_ref, account_type_set)
    email_ref.send()

    return "success", "OK"


def employee_leave_company(user_name, employee_id, host):
    employee_ref = Employee.objects.filter(employee_id=employee_id).first()

    emplyee_account_set = Account.objects.filter(employee_id=employee_id)

    if emplyee_account_set.exists():
        account_type_list = emplyee_account_set.values_list("account_type")
        account_type_set = AccountType.objects.filter(account_type__in=account_type_list)
        email_ref = ITMS_MSG(host=host, title=f"Delete Account for {employee_ref.name}")
        email_ref.set_email(list(account_type_set.values_list("pic_email", flat=True)))

        email_ref.build_content(remove_account_content, employee_ref, emplyee_account_set, user_name)
        email_ref.send()

    # if employee_ref.laptop or employee_ref.monitor:
    #     asset_list = []
    #     if employee_ref.laptop:
    #         asset_list.append(
    #             {
    #                 "asset_type": employee_ref.laptop.asset_type,
    #                 "asset_id": employee_ref.laptop.asset_label,
    #             }
    #         )

    #     if employee_ref.monitor:
    #         asset_list.append(
    #             {
    #                 "asset_type": employee_ref.monitor.asset_type,
    #                 "asset_id": employee_ref.monitor.asset_label,
    #             }
    #         )
    #     # send email
    #     email_ref = ITMS_MSG(host=host, title=f"Delete Asset for {employee_ref.name}")
    #     email_ref.set_email(["xuefan.wang@fii-usa.com"])

    #     email_ref.build_content(remove_asset_content, employee_ref, asset_list, user_name)
    #     email_ref.send()
