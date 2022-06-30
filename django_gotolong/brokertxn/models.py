from django.db import models

from django.contrib.auth.models import User  # new

# Create your models here.

class BrokerTxn(models.Model):
    bt_id = models.AutoField(primary_key=True)
    bt_user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    # bt_user_id = models.IntegerField(blank=True, null=True)
    bt_broker = models.TextField(blank=True, null=True)
    bt_stock_symbol = models.TextField(blank=True, null=True)
    bt_company_name = models.TextField(blank=True, null=True)
    bt_isin_code = models.TextField(blank=True, null=True)
    bt_action = models.TextField(blank=True, null=True)
    bt_quantity = models.IntegerField(blank=True, null=True)
    bt_txn_price = models.FloatField(blank=True, null=True)
    bt_brokerage = models.TextField(blank=True, null=True)
    bt_txn_charges = models.TextField(blank=True, null=True)
    bt_stamp_duty = models.TextField(blank=True, null=True)
    bt_segment = models.TextField(blank=True, null=True)
    bt_stt = models.TextField(blank=True, null=True)
    bt_remarks = models.TextField(blank=True, null=True)
    bt_txn_date = models.DateField(blank=True, null=True)
    bt_exchange = models.TextField(blank=True, null=True)
    bt_unused1 = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'broker_txn'
        unique_together = (('bt_user', 'bt_company_name', 'bt_txn_date'),)
