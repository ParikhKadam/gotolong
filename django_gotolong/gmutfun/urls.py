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

from django_gotolong.gmutfun.views import GmutfunListView, \
    Gmutfun_upload, Gmutfun_fetch
from django_gotolong.gmutfun.views import GmutfunIndustryView, \
    GmutfunListView_Type, GmutfunListView_Benchmark, GmutfunListView_Passive_Select, \
    GmutfunListView_AUM, GmutfunListView_NonGold_FOF, GmutfunListView_NonGold_ETF, \
    GmutfunListView_Gold_ETF, GmutfunListView_Gold_FOF, \
    GmutfunListView_Global_ETF, GmutfunListView_Global_FOF, \
    GmutfunListView_Hybrid_ETF, GmutfunListView_Hybrid_FOF, \
    GmutfunListView_Nifty_ETF, GmutfunListView_Nifty_FOF, \
    GmutfunListView_Next_ETF, GmutfunListView_Next_FOF, \
    GmutfunListView_Mid_ETF, GmutfunListView_Mid_FOF

from django_gotolong.gmutfun.views import GmutfunListView_Active_Flexi, \
    GmutfunListView_Active_Large, GmutfunListView_Active_Mid, GmutfunListView_Active_Small, \
    GmutfunListView_Active_Multi, GmutfunListView_Active_LargeMid, \
    GmutfunListView_Active_Value, GmutfunListView_Active_Dividend, \
    GmutfunListView_Active_Select_4321, GmutfunListView_Active_Select_5555

urlpatterns = [
    path('list/', GmutfunListView.as_view(), name='gmutfun-list'),
    path('list/aum/', GmutfunListView_AUM.as_view(), name='gmutfun-list-aum'),
    path('list/type/', GmutfunListView_Type.as_view(), name='gmutfun-list-type'),
    path('list/benchmark/', GmutfunListView_Benchmark.as_view(), name='gmutfun-list-benchmark'),
    path('list/passive-select/', GmutfunListView_Passive_Select.as_view(), name='gmutfun-list-passive-select'),
    path('list/etf/gold/', GmutfunListView_Gold_ETF.as_view(), name='gmutfun-list-etf-gold'),
    path('list/etf/nifty-50/', GmutfunListView_Nifty_ETF.as_view(), name='gmutfun-list-etf-nifty'),
    path('list/etf/next-50/', GmutfunListView_Next_ETF.as_view(), name='gmutfun-list-etf-next'),
    path('list/etf/mid-150/', GmutfunListView_Mid_ETF.as_view(), name='gmutfun-list-etf-mid'),
    path('list/etf/global/', GmutfunListView_Global_ETF.as_view(), name='gmutfun-list-etf-global'),
    path('list/etf/hybrid/', GmutfunListView_Hybrid_ETF.as_view(), name='gmutfun-list-etf-hybrid'),
    path('list/etf/non-gold/', GmutfunListView_NonGold_ETF.as_view(), name='gmutfun-list-etf-non-gold'),
    path('list/fof/gold/', GmutfunListView_Gold_FOF.as_view(), name='gmutfun-list-fof-gold'),
    path('list/fof/nifty-50/', GmutfunListView_Nifty_FOF.as_view(), name='gmutfun-list-fof-nifty'),
    path('list/fof/next-50/', GmutfunListView_Next_FOF.as_view(), name='gmutfun-list-fof-next'),
    path('list/fof/mid-150/', GmutfunListView_Mid_FOF.as_view(), name='gmutfun-list-fof-mid'),
    path('list/fof/global/', GmutfunListView_Global_FOF.as_view(), name='gmutfun-list-fof-global'),
    path('list/fof/hybrid/', GmutfunListView_Hybrid_FOF.as_view(), name='gmutfun-list-fof-hybrid'),
    path('list/fof/non-gold/', GmutfunListView_NonGold_FOF.as_view(), name='gmutfun-list-fof-non-gold'),
    path('list/active/flexi/', GmutfunListView_Active_Flexi.as_view(), name='gmutfun-list-active-flexi'),
    path('list/active/large/', GmutfunListView_Active_Large.as_view(), name='gmutfun-list-active-large'),
    path('list/active/mid/', GmutfunListView_Active_Mid.as_view(), name='gmutfun-list-active-mid'),
    path('list/active/small/', GmutfunListView_Active_Small.as_view(), name='gmutfun-list-active-small'),
    path('list/active/multi/', GmutfunListView_Active_Multi.as_view(), name='gmutfun-list-active-multi'),
    path('list/active/large-mid/', GmutfunListView_Active_LargeMid.as_view(), name='gmutfun-list-active-largemid'),
    path('list/active/value/', GmutfunListView_Active_Value.as_view(), name='gmutfun-list-active-value'),
    path('list/active/dividend/', GmutfunListView_Active_Dividend.as_view(), name='gmutfun-list-active-dividend'),
    path('list/active/select/4321/', GmutfunListView_Active_Select_4321.as_view(),
         name='gmutfun-list-active-select-4321'),
    path('list/active/select/5555/', GmutfunListView_Active_Select_5555.as_view(),
         name='gmutfun-list-active-select-5555'),
    path('industry/', GmutfunIndustryView.as_view(), name='gmutfun-industry-list'),
    path('fetch/', Gmutfun_fetch, name='gmutfun-fetch'),
    path('upload/', Gmutfun_upload, name='gmutfun-upload'),
]
