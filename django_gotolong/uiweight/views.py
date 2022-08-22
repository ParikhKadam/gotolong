# Create your views here.

from django.views.generic.list import ListView

from django.http import HttpResponseRedirect
from django.views import View

from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django_gotolong.amfi.models import Amfi
from django_gotolong.dematsum.models import DematSum
from django_gotolong.fratio.models import Fratio
from django_gotolong.indices.models import Indices
from django_gotolong.lastrefd.models import Lastrefd, lastrefd_update
from django_gotolong.uiweight.models import Uiweight

from django.db.models import OuterRef, Subquery, ExpressionWrapper, F, IntegerField, Count

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

import plotly.graph_objects as go
from plotly.offline import plot


class UiweightListView(ListView):
    model = Uiweight

    def get_queryset(self):
        # NOTE - added dummy values() to fix subscriptable error in get_context_data ...
        # otherwise we cannot access data using column name in get_context_data...
        self.queryset = Uiweight.objects.all().filter(uiw_user_id=self.request.user.id). \
            values().order_by('uiw_name')
        return self.queryset

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UiweightListView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        labels = []
        values = []
        labels_values_dict = {}
        sum_total = 0
        for q_row in self.queryset:
            # sum_total += q_row['scheme_sum']
            labels_values_dict[q_row['uiw_name']] = q_row['uiw_value']
        # context['sum_total'] = int(sum_total)

        print('labels values dict', labels_values_dict)

        for k, v in sorted(labels_values_dict.items(), key=lambda item: item[1]):
            labels.append(k)
            values.append(v)

        print('labels ', labels)
        print('values ', values)

        fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
        fig.update_traces(textposition='inside', textinfo='percent+label')
        # fig.show()

        plot_div_1 = plot(fig, output_type='div', include_plotlyjs=False)
        context['plot_div_1'] = plot_div_1

        return context


class UiweightRebalanceView(ListView):

    def get_queryset(self):
        self.queryset = Uiweight.objects.all().filter(uiw_user_id=self.request.user.id). \
            values('uiw_name', 'uiw_value', 'uiw_value_pct').order_by('uiw_name')
        return self.queryset

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UiweightRebalanceView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        labels = []
        values = []
        labels_values_dict = {}
        sum_total = 0
        for q_row in self.queryset:
            # sum_total += q_row['scheme_sum']
            labels_values_dict[q_row['uiw_name']] = q_row['uiw_value']
        # context['sum_total'] = int(sum_total)

        print('labels values dict', labels_values_dict)

        for k, v in sorted(labels_values_dict.items(), key=lambda item: item[1]):
            labels.append(k)
            values.append(v)

        print('labels ', labels)
        print('values ', values)

        fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
        fig.update_traces(textposition='inside', textinfo='percent+label')
        # fig.show()

        plot_div_1 = plot(fig, output_type='div', include_plotlyjs=False)
        context['plot_div_1'] = plot_div_1

        return context

    def get_template_names(self):
        app_label = 'uiweight'
        template_name_first = app_label + '/' + 'uiweight_rebalance.html'
        template_names_list = [template_name_first]
        return template_names_list


class UiweightRefreshView(View):
    ticker_industry_dict = {}
    isin_industry_dict = {}

    ind_weight_dict = {}
    ind_ticker_dict = {}
    ind_ticker_weight_dict = {}

    debug_level = 1

    def get(self, request):
        self.uiweight_refresh(request)
        return HttpResponseRedirect(reverse("uiweight-list"))

    def __init__(self):
        super(UiweightRefreshView, self).__init__()

    def uiweight_refresh(self, request):
        debug_level = 1
        # declaring template
        template = "uiweight/uiweight_list.html"

        # ticker to industry mapping
        for ind in Indices.objects.all():
            # strip unwanted new line
            ind.ind_ticker = ind.ind_ticker.rstrip()
            ind.ind_isin = ind.ind_isin.rstrip()
            if debug_level > 1:
                print(ind.ind_ticker, ind.ind_isin, ind.ind_industry)
            self.ticker_industry_dict[ind.ind_ticker] = ind.ind_industry
            self.isin_industry_dict[ind.ind_isin] = ind.ind_industry

        portfolio_size = 0
        # ticker to industry name and industry weight
        for ds in DematSum.objects.all().filter(ds_user_id=request.user.id):
            print(ds.ds_id, ds.ds_user_id, ds.ds_broker, ds.ds_isin, ds.ds_mktvalue)

            if ds.ds_isin in self.isin_industry_dict:
                ind_name = self.isin_industry_dict[ds.ds_isin]
            else:
                ind_name = 'Unknown'

            if ind_name in self.ind_weight_dict:
                self.ind_weight_dict[ind_name] += ds.ds_mktvalue
            else:
                self.ind_weight_dict[ind_name] = ds.ds_mktvalue

            portfolio_size += ds.ds_mktvalue

            if ind_name in self.ind_ticker_dict:
                self.ind_ticker_dict[ind_name] += ', ' + ds.ds_ticker
            else:
                self.ind_ticker_dict[ind_name] = ds.ds_ticker

        # fill ticker with portfolio % - pick bigger asset first
        for ds in DematSum.objects.all().filter(ds_user_id=request.user.id).order_by('-ds_mktvalue'):
            print(ds.ds_id, ds.ds_user_id, ds.ds_broker, ds.ds_isin, ds.ds_mktvalue)

            if ds.ds_isin in self.isin_industry_dict:
                ind_name = self.isin_industry_dict[ds.ds_isin]
            else:
                ind_name = 'Unknown'

            if ind_name in self.ind_ticker_weight_dict:
                self.ind_ticker_weight_dict[ind_name] += ', ' + ds.ds_ticker + '(' + str(
                    round(ds.ds_mktvalue * 100.0 / portfolio_size, 2)) + ')'
            else:
                self.ind_ticker_weight_dict[ind_name] = ds.ds_ticker + '(' + str(
                    round(ds.ds_mktvalue * 100.0 / portfolio_size, 2)) + ')'

        # breakpoint()

        # import pdb
        # pdb.set_trace()

        # first delete all existing uiweight objects
        Uiweight.objects.all().filter(uiw_user_id=request.user.id).delete()

        for ind_name in sorted(self.ind_weight_dict):

            # print(tl.stock_name, tl.isin)

            # using 0 for roe3
            # using notes itself as notes
            uiw_name = ind_name
            uiw_value = round(self.ind_weight_dict[ind_name], 2)
            # uiw_tickers = self.ind_ticker_dict[ind_name]
            uiw_tickers = self.ind_ticker_weight_dict[ind_name]
            uiw_companies = 'tbd'
            if ',' in uiw_tickers or uiw_tickers != '':
                uiw_constituents = uiw_tickers.count(",") + 1
            else:
                uiw_constituents = 0

            if debug_level > 1:
                print(uiw_name, uiw_value, uiw_tickers, uiw_companies)

            uiw_value_pct = round(uiw_value * 100.0 / portfolio_size, 2)
            _, created = Uiweight.objects.update_or_create(
                uiw_user_id=request.user.id,
                uiw_name=uiw_name,
                uiw_value=uiw_value,
                uiw_value_pct=uiw_value_pct,
                uiw_constituents=uiw_constituents,
                uiw_tickers=uiw_tickers,
                uiw_companies=uiw_companies
            )

        # Updated Uiweight objects
        lastrefd_update("uiweight")
