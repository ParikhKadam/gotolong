"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

from django_gotolong.phealth.views import PhealthListView_AllButNone, PhealthListView_All, PhealthListView_Buy
from django_gotolong.phealth.views import PhealthListView_Sell, PhealthListView_Hold, PhealthListView_Insuf
from django_gotolong.phealth.views import PhealthListView_Mixed

urlpatterns = [
    path('list/all-none/', PhealthListView_AllButNone.as_view(), name='phealth-list-all-but-none'),
    path('list/all/', PhealthListView_All.as_view(), name='phealth-list-all'),
    path('list/buy/', PhealthListView_Buy.as_view(), name='phealth-list-buy'),
    path('list/hold/', PhealthListView_Hold.as_view(), name='phealth-list-hold'),
    path('list/sell/', PhealthListView_Sell.as_view(), name='phealth-list-sell'),
    path('list/mixed/', PhealthListView_Mixed.as_view(), name='phealth-list-mixed'),
    path('list/insuf/', PhealthListView_Insuf.as_view(), name='phealth-list-insuf'),

]
