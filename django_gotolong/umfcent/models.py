# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

from django.contrib.auth.models import User


class Umfcent(models.Model):
    umfcent_id = models.IntegerField(blank=True, null=True)
    umfcent_user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    umfcent_amc = models.TextField(blank=True, null=True)
    umfcent_category = models.TextField(blank=True, null=True)
    umfcent_subcat = models.TextField(blank=True, null=True)
    umfcent_name = models.TextField(primary_key=True)
    umfcent_txn_date = models.TextField(blank=True, null=True)
    umfcent_value = models.FloatField(blank=True, null=True)

    class Meta:
        db_table = 'user_mfcent'
