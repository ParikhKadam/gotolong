from django.db import models


# Create your models here.

class Trendlyne(models.Model):
    tl_stock_name = models.TextField(blank=True, null=True)
    tl_nse = models.TextField(primary_key=True)
    tl_isin = models.TextField(blank=True, null=True)
    tl_bat = models.FloatField(blank=True, null=True)
    tl_der = models.FloatField(blank=True, null=True)
    tl_roce3 = models.FloatField(blank=True, null=True)
    tl_roe3 = models.FloatField(blank=True, null=True)
    tl_dpr2 = models.FloatField(blank=True, null=True)
    tl_sales2 = models.FloatField(blank=True, null=True)
    tl_profit5 = models.FloatField(blank=True, null=True)
    tl_icr = models.FloatField(blank=True, null=True)
    tl_pledge = models.FloatField(blank=True, null=True)
    tl_low_3y = models.FloatField(blank=True, null=True)
    tl_low_5y = models.FloatField(blank=True, null=True)

    class Meta:
        db_table = 'global_trendlyne'
