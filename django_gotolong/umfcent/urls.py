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

from .views import UmfcentListView, \
    UmfcentListView_AMC_Amount, UmfcentListView_SubcatAmount, \
    UmfcentListView_StyleBox, UmfcentListView_CapBox, Umfcent_upload

urlpatterns = [
    path('list/', UmfcentListView.as_view(), name='umfcent-list'),
    path('amc/amount/list/', UmfcentListView_AMC_Amount.as_view(), name='umfcent-list-amc-amount'),
    path('subcat/amount/list/', UmfcentListView_SubcatAmount.as_view(), name='umfcent-list-subcat-amount'),
    path('stylebox/list/', UmfcentListView_StyleBox.as_view(), name='umfcent-list-stylebox'),
    path('capbox/list/', UmfcentListView_CapBox.as_view(), name='umfcent-list-capbox'),
    path('upload/', Umfcent_upload, name='umfcent-upload'),
]
