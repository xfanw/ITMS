from datetime import datetime
from decimal import *
from asset.models import Laptop, Monitor
from employee.models import EmployeeAsset
from logs.models import AssetAssignLog, LaptopLog, MonitorLog
import pandas


def check_asset(asset_label):
    asset_ref = Laptop.objects.filter(asset_label=asset_label).first()
    if asset_ref:
        return asset_ref

    asset_ref = Monitor.objects.filter(asset_label=asset_label).first()
    if asset_ref:
        return asset_ref

    return None


def assign_asset_to_user(employee_ref, asset_ref, user_name):
    asset_ref.status = "IN_USE"
    asset_ref.save()

    EmployeeAsset.objects.create(
        employee=employee_ref,
        asset_type=asset_ref.asset_type,
        asset_label=asset_ref.asset_label,
        asset_serial_number=asset_ref.serial_number,
        asset_brand=asset_ref.brand,
        asset_model=asset_ref.model,
        assign_date=datetime.now().astimezone(),
        assign_person=user_name,
    )

    AssetAssignLog.create_log(
        "Assign",
        employee_ref.employee_id,
        employee_ref.name,
        asset_ref.asset_type,
        asset_ref.serial_number,
        asset_ref.asset_label,
        user_name,
        "",
    )


def remove_asset_from_user(employee_ref, asset_ref, user_name):
    asset_ref.status = "IDLE"
    asset_ref.save()

    EmployeeAsset.objects.filter(
        employee=employee_ref, asset_type=asset_ref.asset_type, asset_label=asset_ref.asset_label
    ).delete()

    AssetAssignLog.create_log(
        "Remove",
        employee_ref.employee_id,
        employee_ref.name,
        asset_ref.asset_type,
        asset_ref.serial_number,
        asset_ref.asset_label,
        user_name,
        "",
    )


def check_laptop_add(ram, storage, purchase_date, purchase_cost, asset_label, serial_number):
    if ram:
        if len(ram) > 15 or not ram.isnumeric():
            return 'error', 'Ram should not exceeds the allowed range and only contain integer value.', None, None

    if storage:
        if len(storage) > 15 or not storage.isnumeric():
            return 'error', 'Storage should not exceeds the allowed range and only contain integer value.', None, None

    if purchase_date:
        purchase_date = datetime.strptime(purchase_date, '%Y-%m-%d').astimezone()
    else:
        purchase_date = None

    if purchase_cost:
        purchase_cost = Decimal(purchase_cost)
        if abs(purchase_cost) >= 10**6:
            return 'error', 'Purchase Cost should not exceeds the allowed range.', None, None
    else:
        purchase_cost = 0

    if not asset_label:
        return 'error', 'Asset Label cannot be empty.', None, None
    
    if not serial_number:
        return 'error', 'SN cannot be empty.', None, None

    return 'success', 'OK', purchase_date, purchase_cost 


def laptop_file_handling(laptop_file, user_name):
    df = pandas.read_excel(laptop_file)
    curr_time = datetime.now().astimezone()
    df = df.where(pandas.notnull(df), "")
    
    required_columns = ["Asset Label", "Brand", "Model", "SN", "Processor", "Ram(GB)", "Storage(GB)", "Purchase Cost"]
    if not all(col in df.columns for col in required_columns):
        return "error", 'Wrong Laptop file uploaded.'
    
    row_list = []
    log_list = []
    for _, row in df.iterrows():
        asset_label=row["Asset Label"]
        brand=row["Brand"]
        model=row["Model"]
        serial_number=row["SN"]
        processor=row["Processor"]
        ram=row["Ram(GB)"]
        storage=row["Storage(GB)"]
        purchase_cost=row["Purchase Cost"]

        status, msg, purchase_date, purchase_cost = check_laptop_add(str(ram), str(storage), "", str(purchase_cost), asset_label, serial_number)
        if status == "error":
            return "error", msg

        row_list.append(
            Laptop(
                asset_type="Laptop",
                asset_label=asset_label,
                brand=brand,
                model=model,
                serial_number=serial_number,
                processor=processor,
                ram=str(ram),
                storage=str(storage),
                purchase_date=curr_time,
                purchase_cost=purchase_cost,
                status="IDLE",
            )
        )

        log_list.append(
            LaptopLog(
                action="Add",
                asset_label=asset_label,
                serial_number=serial_number,
                user=user_name,
                memo=f"{brand}, {model}, {processor}, {str(ram)}, {str(storage)}, {curr_time}, {purchase_cost}, IDLE",
            )
        )
    
    try:
        Laptop.objects.bulk_create(row_list)
        LaptopLog.objects.bulk_create(log_list)
    except Exception as e:
        return "error", f'{e}'
    
    return "success", "OK"


def check_monitor_add(screen_size, resolution, purchase_date, purchase_cost, asset_label, serial_number):
    if not screen_size:
        return 'error', 'Please select a Screen Scize.', None, None, None
    else:
        screen_size = int(screen_size)

    if not resolution:
        return 'error', 'Please select a Resolution.', None, None, None

    if purchase_date:
        purchase_date = datetime.strptime(purchase_date, "%Y-%m-%d").astimezone()
    else:
        purchase_date = None

    if purchase_cost:
        purchase_cost = Decimal(purchase_cost)
        if abs(purchase_cost) >= 10**6:
           return 'error', 'Purchase Cost should not exceeds the allowed range.', None, None, None
    else:
        purchase_cost = 0

    if not asset_label:
        return 'error', 'Asset Label cannot be empty.', None, None, None

    if not serial_number:
        return 'error', 'SN cannot be empty.', None, None, None
    
    return 'success', 'OK', screen_size, purchase_date, purchase_cost 


def monitor_file_handling(monitor_file, user_name):
    df = pandas.read_excel(monitor_file)
    curr_time = datetime.now().astimezone()
    df = df.where(pandas.notnull(df), "")

    required_columns = ["Asset Label", "Brand", "Model", "SN", "Screen Size", "Resolution", "Purchase Cost"]
    if not all(col in df.columns for col in required_columns):
        return "error", 'Wrong Monitor file uploaded.'

    row_list = []
    log_list = []
    for _, row in df.iterrows():
        asset_label=row["Asset Label"]
        brand=row["Brand"]
        model=row["Model"]
        serial_number=row["SN"]
        screen_size=row["Screen Size"]
        resolution=row["Resolution"]
        purchase_cost=row["Purchase Cost"]

        status, msg, screen_size, purchase_date, purchase_cost = check_monitor_add(str(screen_size), str(resolution), "", str(purchase_cost), asset_label, serial_number)
        if status == "error":
            return "error", msg

        row_list.append(
            Monitor(
                asset_type="Monitor",
                asset_label=asset_label,
                brand=brand,
                model=model,
                serial_number=serial_number,
                screen_size=screen_size,
                resolution=resolution,
                purchase_date=curr_time,
                purchase_cost=purchase_cost,
                status="IDLE",
            )
        )

        log_list.append(
            MonitorLog(
                action="Add",
                asset_label=asset_label,
                serial_number=serial_number,
                user=user_name,
                memo=f"{brand}, {model}, {resolution}, {screen_size}, {curr_time}, {purchase_cost}, IDLE",
            )
        )
    
    try:
        Monitor.objects.bulk_create(row_list)
        MonitorLog.objects.bulk_create(log_list)
    except Exception as e:
        return "error", f'{e}'
    
    return "success", "OK"
