from django.db import models


# Create your models here.
class LegalEntity(models.Model):
    le_name = models.CharField(max_length=63, null=True, unique=True)


class BusinessGroup(models.Model):
    bg_name = models.CharField(max_length=63, null=True)
    bg_manager = models.CharField(max_length=127, null=True)
    le = models.ForeignKey(
        LegalEntity, on_delete=models.SET_NULL, null=True, to_field="le_name", related_name="bg_set"
    )


class BusinessUnit(models.Model):
    bu_name = models.CharField(max_length=63, null=True)
    bg_name = models.CharField(max_length=63, null=True)
    bg = models.ForeignKey(BusinessGroup, on_delete=models.SET_NULL, null=True, related_name="bu_set")
    bu_manager = models.CharField(max_length=127, null=True)
    le_name = models.CharField(max_length=63, null=True)


class CostCenter(models.Model):
    cc_code = models.CharField(max_length=31)
    cc_name = models.CharField(max_length=63)
    cc_manager = models.CharField(max_length=127, null=True)
    bu = models.ForeignKey(BusinessUnit, on_delete=models.SET_NULL, null=True, related_name="cc_set")
    bu_name = models.CharField(max_length=63, null=True)
    bg_name = models.CharField(max_length=63, null=True)
    le_name = models.CharField(max_length=63, null=True)
