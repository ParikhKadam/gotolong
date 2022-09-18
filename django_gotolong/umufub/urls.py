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

from .views import UmufubListView, \
    UmufubListView_AMC_Amount, UmufubListView_SubcatAmount, \
    UmufubRefreshView, UmufubListView_StyleBox

urlpatterns = [
    path('list/', UmufubListView.as_view(), name='umufub-list'),
    path('amc/amount/list/', UmufubListView_AMC_Amount.as_view(), name='umufub-list-amc-amount'),
    path('subcat/amount/list/', UmufubListView_SubcatAmount.as_view(), name='umufub-list-subcat-amount'),
    path('stylebox/list/', UmufubListView_StyleBox.as_view(), name='umufub-list-stylebox'),
    path('refresh/', UmufubRefreshView.as_view(), name='umufub-refresh')
]
