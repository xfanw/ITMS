from django.db import models


# Create your models here.
class Asset(models.Model):
    asset_type = models.CharField(max_length=127)
    asset_label = models.CharField(max_length=127, unique=True)
    brand = models.CharField(max_length=127)
    model = models.CharField(max_length=127, null=True)
    serial_number = models.CharField(max_length=127)
    purchase_date = models.DateTimeField(null=True)
    purchase_cost = models.DecimalField(max_digits=9, decimal_places=3)
    status = models.CharField(max_length=15, null=True)  # IDLE, IN_USE, RETIRED
    purchase_order_number = models.CharField(max_length=31, null=True)

    class Meta:
        abstract = True


class Laptop(Asset):
    processor = models.CharField(max_length=127, null=True)
    ram = models.CharField(max_length=15, null=True)
    storage = models.CharField(max_length=15, null=True)


class Monitor(Asset):
    screen_size = models.IntegerField(null=True)
    resolution = models.CharField(max_length=63)
