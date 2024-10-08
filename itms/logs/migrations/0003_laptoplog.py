# Generated by Django 4.2.7 on 2024-01-19 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logs', '0002_assetassignlog'),
    ]

    operations = [
        migrations.CreateModel(
            name='LaptopLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(max_length=31, null=True)),
                ('user', models.CharField(max_length=255, null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('memo', models.TextField(null=True)),
                ('asset_label', models.CharField(max_length=127)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
