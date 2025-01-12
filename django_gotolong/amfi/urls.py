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

from django_gotolong.amfi.views import AmfiListView, AmfiAmountAllView, AmfiAmountPositiveView, \
    AmfiDeficitWeightView, AmfiDeficit25kView, AmfiDeficit50kView, AmfiDeficit100kView, \
    AmfiNotableInclusionView, AmfiNotableExclusionView, amfi_upload, \
    AmfiPortfWeightView, AmfiPortfWeightIndustryView

urlpatterns = [
    path('list/', AmfiListView.as_view(), name='amfi-list'),
    path('upload/', amfi_upload, name='amfi-upload'),
    path('amount-all/', AmfiAmountAllView.as_view(), name='amfi-amount-all-list'),
    path('amount-positive/', AmfiAmountPositiveView.as_view(), name='amfi-amount-positive-list'),
    path('deficit/weight/', AmfiDeficitWeightView.as_view(), name='amfi-deficit-weight-list'),
    path('deficit/25k/', AmfiDeficit25kView.as_view(), name='amfi-deficit-25k-list'),
    path('deficit/50k/', AmfiDeficit50kView.as_view(), name='amfi-deficit-50k-list'),
    path('deficit/100k/', AmfiDeficit100kView.as_view(), name='amfi-deficit-100k-list'),
    path('portf-weight/', AmfiPortfWeightView.as_view(), name='amfi-portf-weight-list'),
    path('portf-weight/industry/', AmfiPortfWeightIndustryView.as_view(), name='amfi-portf-weight-industry-list'),
    path('notable-exclusion/', AmfiNotableExclusionView.as_view(),
         name='amfi-notable-exclusion-list'),
    path('notable-inclusion/', AmfiNotableInclusionView.as_view(),
         name='amfi-notable-inclusion-list'),
]
