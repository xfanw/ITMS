# Generated by Django 4.2.7 on 2024-02-08 02:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0004_rename_last_name_employee_last_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='preferred_name',
            field=models.CharField(max_length=127, null=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='middle_name',
            field=models.CharField(max_length=127, null=True),
        ),
    ]
