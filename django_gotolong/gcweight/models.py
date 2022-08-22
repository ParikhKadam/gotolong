# Create your models here.
from django.db import models


# Create your models here.

class Gcweight(models.Model):
    gcw_cap_type = models.TextField(primary_key=True)
    gcw_cap_weight = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'global_cweight'
