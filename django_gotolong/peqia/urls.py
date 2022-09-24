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

from django_gotolong.peqia.views import PeqiaListView_AllButNone, PeqiaListView_All, PeqiaListView_Buy
from django_gotolong.peqia.views import PeqiaListView_Sell, PeqiaListView_Hold, PeqiaListView_Insuf
from django_gotolong.peqia.views import PeqiaListView_Mixed

urlpatterns = [
    path('list/all-none/', PeqiaListView_AllButNone.as_view(), name='peqia-list-all-but-none'),
    path('list/all/', PeqiaListView_All.as_view(), name='peqia-list-all'),
    path('list/buy/', PeqiaListView_Buy.as_view(), name='peqia-list-buy'),
    path('list/hold/', PeqiaListView_Hold.as_view(), name='peqia-list-hold'),
    path('list/sell/', PeqiaListView_Sell.as_view(), name='peqia-list-sell'),
    path('list/mixed/', PeqiaListView_Mixed.as_view(), name='peqia-list-mixed'),
    path('list/insuf/', PeqiaListView_Insuf.as_view(), name='peqia-list-insuf'),

]
