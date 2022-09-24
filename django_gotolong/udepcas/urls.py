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

from .views import UdepcasListView, \
    UdepcasListView_AMC_Amount, UdepcasListView_SubcatAmount, \
    UdepcasListView_StyleBox, UdepcasListView_CapBox, Udepcas_upload

urlpatterns = [
    path('list/', UdepcasListView.as_view(), name='udepcas-list'),
    path('amc/amount/list/', UdepcasListView_AMC_Amount.as_view(), name='udepcas-list-amc-amount'),
    path('subcat/amount/list/', UdepcasListView_SubcatAmount.as_view(), name='udepcas-list-subcat-amount'),
    path('stylebox/list/', UdepcasListView_StyleBox.as_view(), name='udepcas-list-stylebox'),
    path('capbox/list/', UdepcasListView_CapBox.as_view(), name='udepcas-list-capbox'),
    path('upload/', Udepcas_upload, name='udepcas-upload'),
]
