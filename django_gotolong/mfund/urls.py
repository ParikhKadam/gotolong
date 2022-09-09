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

from .views import MfundListView, \
    MfundListView_AMC_Amount, MfundListView_SubcatAmount, \
    MfundRefreshView, MfundListView_Rebalance

urlpatterns = [
    path('list/', MfundListView.as_view(), name='mfund-list'),
    path('amc/amount/list/', MfundListView_AMC_Amount.as_view(), name='mfund-list-amc-amount'),
    path('subcat/amount/list/', MfundListView_SubcatAmount.as_view(), name='mfund-list-subcat-amount'),
    path('rebalance/list/', MfundListView_Rebalance.as_view(), name='mfund-list-rebalance'),
    path('refresh/', MfundRefreshView.as_view(), name='mfund-refresh')
]
