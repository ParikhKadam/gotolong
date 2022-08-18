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

from django_gotolong.fofeti.views import FofetiListView, \
    Fofeti_upload, Fofeti_fetch
from django_gotolong.fofeti.views import FofetiIndustryView, \
    FofetiListView_Type, FofetiListView_Benchmark, FofetiListView_Benchmark_Select, \
    FofetiListView_AUM, FofetiListView_NonGold_FOF, FofetiListView_NonGold_ETF, \
    FofetiListView_Gold_ETF, FofetiListView_Gold_FOF, \
    FofetiListView_Global_ETF, FofetiListView_Global_FOF, \
    FofetiListView_Nifty_ETF, FofetiListView_Nifty_FOF, \
    FofetiListView_Next_ETF, FofetiListView_Next_FOF, \
    FofetiListView_Mid_ETF, FofetiListView_Mid_FOF

urlpatterns = [
    path('list/', FofetiListView.as_view(), name='fofeti-list'),
    path('list/aum/', FofetiListView_AUM.as_view(), name='fofeti-list-aum'),
    path('list/type/', FofetiListView_Type.as_view(), name='fofeti-list-type'),
    path('list/benchmark/', FofetiListView_Benchmark.as_view(), name='fofeti-list-benchmark'),
    path('list/benchmark-select/', FofetiListView_Benchmark_Select.as_view(), name='fofeti-list-benchmark-select'),
    path('list/etf/non-gold/', FofetiListView_NonGold_ETF.as_view(), name='fofeti-list-etf-non-gold'),
    path('list/etf/gold/', FofetiListView_Gold_ETF.as_view(), name='fofeti-list-etf-gold'),
    path('list/etf/nifty-50/', FofetiListView_Nifty_ETF.as_view(), name='fofeti-list-etf-nifty'),
    path('list/etf/next-50/', FofetiListView_Next_ETF.as_view(), name='fofeti-list-etf-next'),
    path('list/etf/mid-150/', FofetiListView_Mid_ETF.as_view(), name='fofeti-list-etf-mid'),
    path('list/etf/global/', FofetiListView_Global_ETF.as_view(), name='fofeti-list-etf-global'),
    path('list/fof/gold/', FofetiListView_Gold_FOF.as_view(), name='fofeti-list-fof-gold'),
    path('list/fof/non-gold/', FofetiListView_NonGold_FOF.as_view(), name='fofeti-list-fof-non-gold'),
    path('list/fof/nifty-50/', FofetiListView_Nifty_FOF.as_view(), name='fofeti-list-fof-nifty'),
    path('list/fof/next-50/', FofetiListView_Next_FOF.as_view(), name='fofeti-list-fof-next'),
    path('list/fof/mid-150/', FofetiListView_Mid_FOF.as_view(), name='fofeti-list-fof-mid'),
    path('list/fof/global/', FofetiListView_Global_FOF.as_view(), name='fofeti-list-fof-global'),
    path('industry/', FofetiIndustryView.as_view(), name='fofeti-industry-list'),
    path('fetch/', Fofeti_fetch, name='fofeti-fetch'),
    path('upload/', Fofeti_upload, name='fofeti-upload'),
]
