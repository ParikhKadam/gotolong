# Create your models here.
from django.db import models


class Gmutfun(models.Model):
    # index company name
    gmutfun_scheme = models.TextField(primary_key=True)
    gmutfun_type = models.TextField(blank=True, null=True)
    gmutfun_subtype = models.TextField(blank=True, null=True)
    # index industry name
    gmutfun_benchmark = models.TextField(blank=True, null=True)

    gmutfun_ret_1y_reg = models.FloatField(blank=True, null=True)
    gmutfun_ret_1y_bench = models.FloatField(blank=True, null=True)
    gmutfun_ret_3y_reg = models.FloatField(blank=True, null=True)
    gmutfun_ret_3y_bench = models.FloatField(blank=True, null=True)
    gmutfun_ret_5y_reg = models.FloatField(blank=True, null=True)
    gmutfun_ret_5y_bench = models.FloatField(blank=True, null=True)
    gmutfun_ret_10y_reg = models.FloatField(blank=True, null=True)
    gmutfun_ret_10y_bench = models.FloatField(blank=True, null=True)

    gmutfun_aum = models.FloatField(blank=True, null=True)

    gmutfun_alpha_grade = models.IntegerField(blank=True, null=True)
    gmutfun_alpha_pct = models.FloatField(blank=True, null=True)

    class Meta:
        db_table = 'global_mutfun'
