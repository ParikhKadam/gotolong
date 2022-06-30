# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

from django.contrib.auth.models import User  # new

from django_gotolong.amfi.models import Amfi


class BrokerSum(models.Model):
    bs_id = models.AutoField(primary_key=True)
    bs_user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    # bs_user_id = models.IntegerField(blank=True, null=True)
    bs_broker = models.TextField(blank=True, null=True)
    bs_stock_symbol = models.TextField(blank=True, null=True)
    bs_company_name = models.TextField(blank=True, null=True)
    # db table will have suffix of _id for foreign key
    # isin_code = models.TextField(blank=True, null=True)
    bs_isin_code = models.ForeignKey(Amfi, on_delete=models.DO_NOTHING)
    bs_qty = models.IntegerField(blank=True, null=True)
    bs_acp = models.FloatField(blank=True, null=True)
    bs_cmp = models.TextField(blank=True, null=True)
    bs_pct_change = models.TextField(blank=True, null=True)
    bs_value_cost = models.FloatField(blank=True, null=True)
    bs_value_market = models.FloatField(blank=True, null=True)
    bs_days_gain = models.TextField(blank=True, null=True)
    bs_days_gain_pct = models.TextField(blank=True, null=True)
    bs_realized_pl = models.TextField(blank=True, null=True)
    bs_unrealized_pl = models.TextField(blank=True, null=True)
    bs_unrealized_pl_pct = models.TextField(blank=True, null=True)
    bs_unused1 = models.TextField(blank=True, null=True)

    # amfis = models.ManyToManyField(Amfi)

    class Meta:
        db_table = 'broker_sum'
        unique_together = (('bs_user_id', 'bs_company_name'),)

def broker_idirect_sum_load_stocks(brokersum_list):
    # load list of demat symbols
    for brokersum in BrokerSum.objects.all():
        brokersum_list.append(brokersum.stock_symbol)
