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

from django_gotolong.goetf.views import GoetfListView, \
    Goetf_upload, Goetf_fetch
from django_gotolong.goetf.views import GoetfIndustryView, \
    GoetfListView_Type, GoetfListView_Benchmark, GoetfListView_Benchmark_Select, \
    GoetfListView_AUM, GoetfListView_IMF, GoetfListView_NonGold_ETF, \
    GoetfListView_Gold_ETF, GoetfListView_Gold_MF

urlpatterns = [
    path('list/', GoetfListView.as_view(), name='goetf-list'),
    path('list/aum/', GoetfListView_AUM.as_view(), name='goetf-list-aum'),
    path('list/type/', GoetfListView_Type.as_view(), name='goetf-list-type'),
    path('list/benchmark/', GoetfListView_Benchmark.as_view(), name='goetf-list-benchmark'),
    path('list/benchmark-select/', GoetfListView_Benchmark_Select.as_view(), name='goetf-list-benchmark-select'),
    path('list/index-mf/', GoetfListView_IMF.as_view(), name='goetf-list-imf'),
    path('list/gold-etf/', GoetfListView_Gold_ETF.as_view(), name='goetf-list-gold-etf'),
    path('list/gold-mf/', GoetfListView_Gold_MF.as_view(), name='goetf-list-gold-mf'),
    path('list/non-gold-etf/', GoetfListView_NonGold_ETF.as_view(), name='goetf-list-non-gold-etf'),
    path('industry/', GoetfIndustryView.as_view(), name='goetf-industry-list'),
    path('fetch/', Goetf_fetch, name='goetf-fetch'),
    path('upload/', Goetf_upload, name='goetf-upload'),
]
