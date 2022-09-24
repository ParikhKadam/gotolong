# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

from django.contrib.auth.models import User


class Udepcas(models.Model):
    udepcas_id = models.IntegerField(blank=True, null=True)
    udepcas_user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    udepcas_asset_class = models.TextField(blank=True, null=True)
    udepcas_isin = models.TextField(primary_key=True)
    udepcas_symbol = models.TextField(blank=True, null=True)
    udepcas_name = models.TextField(blank=True, null=True)
    udepcas_qty = models.IntegerField(blank=True, null=True)
    udepcas_cost = models.FloatField(blank=True, null=True)
    udepcas_value = models.FloatField(blank=True, null=True)
    udepcas_txn_date = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'user_depcas'
