# Generated by Django 4.2.7 on 2024-02-10 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logs', '0007_accountassignlog_accounttypelog_businessgrouplog_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='accountassignlog',
            name='account_type',
            field=models.CharField(max_length=127, null=True),
        ),
        migrations.AddField(
            model_name='accountassignlog',
            name='employee_id',
            field=models.CharField(max_length=127, null=True),
        ),
    ]
