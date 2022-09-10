# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

from django.contrib.auth.models import User


class Umufu(models.Model):
    umf_id = models.IntegerField(blank=True, null=True)
    umf_user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    umf_broker = models.TextField(blank=True, null=True)
    umf_amc = models.TextField(blank=True, null=True)
    umf_name = models.TextField(primary_key=True)
    umf_category = models.TextField(blank=True, null=True)
    umf_subcat = models.TextField(blank=True, null=True)
    umf_rating = models.TextField(blank=True, null=True)
    umf_cost_value = models.FloatField(blank=True, null=True)
    umf_nav_value = models.FloatField(blank=True, null=True)
    umf_research_reco = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'user_mufu'
