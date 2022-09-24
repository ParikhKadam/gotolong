# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

from django.contrib.auth.models import User

from django_gotolong.amfi.models import Amfi

class DematSum(models.Model):
    ds_id = models.IntegerField(blank=True, null=True)
    ds_user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    ds_broker = models.TextField(blank=True, null=True)
    ds_ticker = models.TextField(primary_key=True)
    # isin_code = models.TextField(blank=True, null=True)
    ds_name = models.TextField(blank=True, null=True)
    ds_isin = models.TextField(blank=True, null=True)
    ds_qty = models.IntegerField(blank=True, null=True)
    ds_acp = models.FloatField(blank=True, null=True)
    ds_costvalue = models.FloatField(blank=True, null=True)
    ds_mktvalue = models.FloatField(blank=True, null=True)

    # amfis = models.ManyToManyField(Amfi)

    class Meta:
        db_table = 'user_demat_sum'

def dematsum_load_stocks(dematsum_list):
    # load list of demat symbols
    for dematsum in DematSum.objects.all():
        dematsum_list.append(dematsum.ds_ticker)
