# Generated by Django 4.2.7 on 2024-02-11 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logs', '0008_accountassignlog_account_type_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='employeelog',
            name='department',
            field=models.CharField(max_length=127, null=True),
        ),
        migrations.AddField(
            model_name='employeelog',
            name='employee_name',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
