# Create your models here.
from django.db import models
from django.utils.timezone import make_aware
from django.utils import timezone

from time import strftime
from datetime import datetime


# Create your models here.

class Lastrefd(models.Model):
    lastrefd_module = models.TextField(primary_key=True)
    lastrefd_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'both_lastrefd'


def lastrefd_same_time(module_name):
    lastrefd_module = module_name
    try:
        e = Lastrefd.objects.get(lastrefd_module=lastrefd_module)
    except:
        return False
    lastrefd_date = e.lastrefd_date.strftime("%Y-%m-%d %H:%M")
    now = timezone.now()
    today_date = now.strftime("%Y-%m-%d %H:%M")
    print("lastrefd_same_time: ", lastrefd_module, 'last: ', lastrefd_date, 'today: ', today_date)
    if lastrefd_date == today_date:
        return True
    else:
        return False


def lastrefd_same_day(module_name):
    lastrefd_module = module_name
    try:
        e = Lastrefd.objects.get(lastrefd_module=lastrefd_module)
    except:
        return False

    lastrefd_date = e.lastrefd_date.strftime("%Y-%m-%d")
    now = timezone.now()
    today_date = now.strftime("%Y-%m-%d")
    print("lastrefd_same_day: ", lastrefd_module, 'last: ', lastrefd_date, 'today: ', today_date)
    if lastrefd_date == today_date:
        return True
    else:
        return False

def lastrefd_update(module_name):
    now = timezone.now()
    lastrefd_module = module_name
    # fixed timezone issue
    lastrefd_date = now.strftime("%Y-%m-%d %H:%M:%S.%f%z")

    print(lastrefd_module, lastrefd_date)

    # delete existing record
    Lastrefd.objects.filter(lastrefd_module=lastrefd_module).delete()

    # update
    _, created = Lastrefd.objects.update_or_create(
        lastrefd_module=lastrefd_module,
        lastrefd_date=lastrefd_date
    )