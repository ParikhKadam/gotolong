# Create your models here.
from django.db import models


class Goetf(models.Model):
    # index company name
    goetf_scheme = models.TextField(primary_key=True)
    goetf_type = models.TextField(blank=True, null=True)
    # index industry name
    goetf_benchmark = models.TextField(blank=True, null=True)
    goetf_aum = models.FloatField(blank=True, null=True)

    class Meta:
        db_table = 'global_goetf'