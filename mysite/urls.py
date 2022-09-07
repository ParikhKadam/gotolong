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

from django.views.generic import TemplateView, RedirectView

from django_gotolong.bhav.views import BhavListView, bhav_fetch, bhav_upload

#from django_gotolong.broker.icidir.isum.views import BrokerIcidirSumListView, BrokerIcidirSumUpload
#from django_gotolong.broker.icidir.itxn.views import BrokerIcidirTxnListView, BrokerIcidirTxnUpload

from django_gotolong.bstmtdiv.views import BstmtDivListView, bstmtdiv_upload
from django_gotolong.bstmtdiv.views import BstmtDivYearArchiveView, BstmtDivMonthArchiveView, BstmtDivAmountView, \
    BstmtDivFrequencyView

from django_gotolong.corpact.views import CorpactListView, corpact_upload

from django_gotolong.dbstat.views import DbstatListView

from django_gotolong.dematsum.views import DematSumListView, DematSumRankView, DematSumTickerView, DematSumAmountView, \
    DematSumCapTypeView, DematSumRecoView

from django_gotolong.dividend.views import DividendListView, DividendRefreshView, DividendTickerListView

from django_gotolong.ftwhl.views import FtwhlListView, ftwhl_fetch, ftwhl_upload
from django_gotolong.fratio.views import FratioListView
from django_gotolong.gfundareco.views import GfundarecoListView, GfundarecoRefreshView
from django_gotolong.gcweight.views import GcweightListView

from django_gotolong.indices.views import IndicesListView, IndicesIndustryView
from django_gotolong.indices.views import Indices_fetch, Indices_upload

from django_gotolong.lastrefd.views import LastrefdListView

from django_gotolong.nach.views import NachListView
from django_gotolong.othinv.views import OthinvListView

from django_gotolong.trendlyne.views import TrendlyneListView, TrendlyneRecoView, trendlyne_upload

from django_gotolong.uploaddoc import views

from django_gotolong.jsched.tasks import jsched_task_startup
from django.contrib.staticfiles.storage import staticfiles_storage

urlpatterns = [
                  path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('favicon_io/favicon.ico'))),
                  path('home/', TemplateView.as_view(template_name="home.html"), name='home'),
                  path('', TemplateView.as_view(template_name="home.html"), name='index'),
                  path('accounts/', include('django.contrib.auth.urls')),
                  path('admin/', admin.site.urls),
                  path('advisor/', include('django_gotolong.advisor.urls')),
                  path('amfi/', include('django_gotolong.amfi.urls')),
                  path('bhav/list/', BhavListView.as_view(), name='bhav-list'),
                  path('bhav/fetch/', bhav_fetch, name='bhav-fetch'),
                  path('bhav/upload/', bhav_upload, name='bhav-upload'),
                  path('bstmtdiv/list/', BstmtDivListView.as_view(), name='bstmtdiv-list'),
                  path('bstmtdiv/list/<str:year>/', BstmtDivYearArchiveView.as_view(),
                       name='bstmtdiv_archive_year'),
                path('bstmtdiv/list/<int:year>/<int:month>/',
                     BstmtDivMonthArchiveView.as_view(month_format='%m'),
                     name='bstmtdiv_archive_month_numeric'),
                path('bstmtdiv/list/<int:year>/<str:month>/', BstmtDivMonthArchiveView.as_view(),
                     name='bstmtdiv_archive_month'),
                  path('bstmtdiv/amount/', BstmtDivAmountView.as_view(),
                       name='bstmtdiv-amount-list'),
                  path('bstmtdiv/frequency/', BstmtDivFrequencyView.as_view(),
                       name='bstmtdiv-frequency-list'),
                  path('bstmtdiv/upload/', bstmtdiv_upload, name='bstmt-upload'),
                  path('bhav/fetch/', bhav_fetch, name='bhav-fetch'),
                  #                  path('broker/', include('django_gotolong.broker.urls')),
                  path('brokersum/', include('django_gotolong.brokersum.urls')),
                  path('brokertxn/', include('django_gotolong.brokertxn.urls')),
                  path('brokermf/', include('django_gotolong.brokermf.urls')),
                  path('bucc/', include('django_gotolong.bucc.urls')),
                  path('corpact/list/', CorpactListView.as_view(), name='corpact-list'),
                  path('corpact/upload/', corpact_upload, name='corpact-upload'),
                  path('dbstat/list/', DbstatListView.as_view(), name='dbstat-list'),
                  path('demat/sum/', include('django_gotolong.dematsum.urls')),
                  path('demat/txn/', include('django_gotolong.demattxn.urls')),
                  path('dividend/list/', DividendListView.as_view(), name='dividend-list'),
                  path('dividend/refresh/', DividendRefreshView.as_view(), name='dividend-refresh'),
                  path('dividend/ticker/', DividendTickerListView.as_view(),
                       name='dividend-ticker-list'),
                  #                  path('fof/', include('django_gotolong.fof.urls')),
                  path('fofeti/', include('django_gotolong.fofeti.urls')),
                  path('fratio/', include('django_gotolong.fratio.urls')),
                  path('ftwhl/list/', FtwhlListView.as_view(), name='ftwhl-list'),
                  path('ftwhl/fetch/', ftwhl_fetch, name='ftwhl-fetch'),
                  path('ftwhl/upload/', ftwhl_upload, name='ftwhl-upload'),
                  path('gfundareco/list/', GfundarecoListView.as_view(), name='gfundareco-list'),
                  path('gfundareco/refresh/', GfundarecoRefreshView.as_view(), name='gfundareco-refresh'),
                  path('gcweight/list/', GcweightListView.as_view(), name='gcweight-list'),
                  path('indices/list/', IndicesListView.as_view(), name='indices-list'),
                  path('indices/industry/', IndicesIndustryView.as_view(), name='indices-industry-list'),
                  path('indices/fetch/', Indices_fetch, name='indices-fetch'),
                  path('indices/upload/', Indices_upload, name='indices-upload'),
                  path('lastrefd/list/', LastrefdListView.as_view(), name='lastrefd-list'),
                  path('mfund/', include('django_gotolong.mfund.urls')),
                  path('nach/list/', NachListView.as_view(), name='nach-list'),
                  path('othinv/', include('django_gotolong.othinv.urls')),
                  path('page/about/', TemplateView.as_view(template_name="about.html")),
                  path('page/annual-report-self/', TemplateView.as_view(template_name="annual_report_self.html")),
                  path('page/contact/', TemplateView.as_view(template_name="contact.html")),
                  path('page/global-data/', TemplateView.as_view(template_name="global_data.html")),
                  path('page/home/', TemplateView.as_view(template_name="home.html")),
                  path('page/quick-links/', TemplateView.as_view(template_name="quick_links.html")),
                  path('page/sitemap/', TemplateView.as_view(template_name="sitemap.html")),
                  path('page/user-data/', TemplateView.as_view(template_name="user_data.html")),
                  path('paytxn/', include('django_gotolong.paytxn.urls')),
                  path('phealth/', include('django_gotolong.phealth.urls')),
                  path('trendlyne/list/', TrendlyneListView.as_view(), name='trendlyne-list'),
                  path('trendlyne/reco/', TrendlyneRecoView.as_view(), name='trendlyne-reco-list'),
                  path('trendlyne/upload/', trendlyne_upload, name='trendlyne-upload'),
                  path('uploaddoc/simple/', views.simple_upload, name='uploaddoc-simple'),
                  path('uploaddoc/model-form/', views.model_form_upload, name='uploaddoc-model-form'),
                  path('uploaddoc/list/', views.list, name='uploaddoc-list'),
                  path('uploaddoc/delete/<int:id>/', views.delete_view, name='uploaddoc-delete'),
                  path('users/', include('django_gotolong.users.urls')),
                  path('uiweight/', include('django_gotolong.uiweight.urls')),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

jsched_task_startup()
