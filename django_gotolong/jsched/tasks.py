# Create your views here.

# Create your views here.

from django.shortcuts import redirect
from django.http import HttpResponseRedirect

from datetime import date, timedelta
from apscheduler.schedulers.background import BackgroundScheduler

from django_gotolong.bhav.views import bhav_fetch_yday
from django_gotolong.ftwhl.views import ftwhl_fetch

from django.utils import timezone

# from background_task import background

import requests
import sys


# notify_user(user.id, schedule=90) # 90 seconds from now
# notify_user(user.id, schedule=timedelta(minutes=20)) # 20 minutes from now
# notify_user(user.id, schedule=timezone.now()) # at a specific time

# @background(schedule=15)
def jsched_task_bg():
    print('tasks.py : notify_nse')

    # redirect('bhav-fetch')
    # redirect('ftwhl-fetch')


def jsched_task_daily():
    print('tasks.py : jsched_task_daily: to be fixed later')
    return

    if True:
        tmodules = ['bhav', 'ftwhl']
        for tmod in tmodules:
            try:
                url = 'http://127.0.0.1:8000/' + tmod + '/fetch/'
                # connect timeout - 5 sec
                # read timeout - 14 sec
                response = requests.get(url, allow_redirects=False, timeout=(15, 60))
                print(url, response.url, response.status_code)
            except:
                print("Unexpected error:", url, sys.exc_info())


def jsched_task_common():
    print('tasks.py : common tasks')
    # HttpResponseRedirect(reverse('bhav-fetch'))
    # HttpResponseRedirect(reverse('ftwhl-fetch'))
    # redirect('bhav-fetch')
    # redirect('ftwhl-fetch')


def jsched_task_startup():
    print('tasks.py : start')
    # notify_nse(repeat=Task.DAILY, repeat_until=None)
    # scheduler = BackgroundScheduler()
    # scheduler.add_job(jsched_task_common, 'interval', days=1)
    # scheduler.start()
