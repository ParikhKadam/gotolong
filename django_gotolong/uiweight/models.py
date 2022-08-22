# Create your models here.
from django.db import models

from django.contrib.auth.models import User  # new


# Create your models here.

class Uiweight(models.Model):
    uiw_user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    uiw_name = models.TextField(primary_key=True)
    uiw_value = models.FloatField(blank=True, null=True)
    uiw_value_pct = models.FloatField(blank=True, null=True)
    uiw_constituents = models.IntegerField(blank=True, null=True)
    uiw_tickers = models.TextField(blank=True, null=True)
    uiw_companies = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'user_iweight'
