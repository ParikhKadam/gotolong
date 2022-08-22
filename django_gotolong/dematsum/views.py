# Create your views here.

from .models import DematSum

import plotly.graph_objects as go
from plotly.offline import plot
from plotly.tools import make_subplots

from django.db.models import Q

from django.conf import settings
from django.shortcuts import redirect

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.views.generic.list import ListView
from django.views import View

from django.db.models import OuterRef, Subquery, Count, Sum, Max, Min
from django.db.models.functions import Trim, Lower, Round

from django_gotolong.amfi.models import Amfi
from django_gotolong.gfundareco.models import Gfundareco

import pandas as pd
import csv, io
import openpyxl
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect

from django_gotolong.lastrefd.models import Lastrefd, lastrefd_update

from django_gotolong.brokersum.models import BrokerSum




class DematSumListView(ListView):
    model = DematSum

    # if pagination is desired
    # paginate_by = 300

    # queryset = DematSum.objects.all()

    def get_queryset(self):
        return DematSum.objects.all().filter(ds_user_id=self.request.user.id)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(DematSumListView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_amount = (DematSum.objects.all().filter(ds_user_id=self.request.user.id).
                        aggregate(mktvalue=Sum('ds_mktvalue')))['mktvalue']
        if total_amount:
            total_amount = round(total_amount)
        else:
            # NoneType
            # handle case where data has not been loaded yet
            return

        # reit list
        filter_list = ['EMBOFF', 'MINBUS', 'BROIND']
        query = Q()
        for fltr in filter_list:
            query = query | Q(ds_ticker=fltr)

        reit_amount = (DematSum.objects.all().filter(ds_user_id=self.request.user.id).
                       filter(query).aggregate(mktvalue=Sum('ds_mktvalue')))['mktvalue']

        if reit_amount:
            reit_amount = round(int(float(reit_amount)))

        # domestic etf list
        filter_list = ['HDFRGE', 'ICINEX', 'ICINIF', 'KOTNIF', 'NIFBEE',
                       'REL150', 'SBIN50', 'SBINIF', 'UTINIF']
        query = Q()
        for fltr in filter_list:
            query = query | Q(ds_ticker=fltr)

        d_etf_amount = (DematSum.objects.all().filter(ds_user_id=self.request.user.id).
                        filter(query).aggregate(mktvalue=Sum('ds_mktvalue')))['mktvalue']
        if d_etf_amount:
            d_etf_amount = round(d_etf_amount)

        # international etf list
        filter_list = ['MOTNAS']
        query = Q()
        for fltr in filter_list:
            query = query | Q(ds_ticker=fltr)

        i_etf_amount = (DematSum.objects.all().filter(ds_user_id=self.request.user.id).
                        filter(query).aggregate(mktvalue=Sum('ds_mktvalue')))['mktvalue']
        if i_etf_amount:
            i_etf_amount = round(i_etf_amount)

        gold_amount = (DematSum.objects.all().filter(ds_user_id=self.request.user.id). \
                       filter(ds_ticker__icontains='GOL').aggregate(mktvalue=Sum('ds_mktvalue')))['mktvalue']
        if gold_amount:
            gold_amount = round(gold_amount)

        direct_equity_amount = total_amount - reit_amount - \
                               d_etf_amount - i_etf_amount - gold_amount

        context["total_amount"] = total_amount
        context["reit_amount"] = reit_amount
        context["d_etf_amount"] = d_etf_amount
        context["i_etf_amount"] = i_etf_amount
        context["gold_amount"] = gold_amount
        context["direct_equity_amount"] = direct_equity_amount

        labels = ['REIT', 'domestic ETF', 'international ETF', 'gold ETF',
                  'direct equity']
        values = [reit_amount, d_etf_amount, i_etf_amount, gold_amount,
                  direct_equity_amount]

        fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
        fig.update_traces(textposition='inside', textinfo='percent+label')
        # fig.show()

        plot_div_1 = plot(fig, output_type='div', include_plotlyjs=False)
        context['plot_div_1'] = plot_div_1

        return context

class DematSumTickerView(ListView):
    model = DematSum

    # if pagination is desired
    # paginate_by = 300

    # select required columns instead of all columns
    queryset = DematSum.objects.values('ds_ticker')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class DematSumRankView(ListView):
    # model = DematSum

    # if pagination is desired
    # paginate_by = 300

    # amfi_qset = Amfi.objects.filter(comp_isin=OuterRef('pk'))
    # queryset = DematSum.objects.annotate(comp_rank=Subquery(amfi_qset.values('comp_rank'))).order_by('comp_rank')
    # queryset = DematSum.objects.annotate(comp_rank=Subquery(amfi_qset.values('comp_rank')))
    amfi_qs = Amfi.objects.filter(comp_isin=OuterRef("ds_isin"))
    queryset = DematSum.objects.all(). \
        annotate(comp_rank=Subquery(amfi_qs.values('comp_rank')[:1])). \
        annotate(cap_type=Lower(Trim(Subquery(amfi_qs.values('cap_type')[:1])))). \
        values('ds_ticker', 'ds_costvalue', 'comp_rank', 'cap_type'). \
        order_by('comp_rank')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class DematSumRecoView(ListView):
    # model = DematSum

    # if pagination is desired
    # paginate_by = 300

    # amfi_qset = Amfi.objects.filter(comp_isin=OuterRef('pk'))
    # queryset = DematSum.objects.annotate(comp_rank=Subquery(amfi_qset.values('comp_rank'))).order_by('comp_rank')
    # queryset = DematSum.objects.annotate(comp_rank=Subquery(amfi_qset.values('comp_rank')))
    amfi_qs = Amfi.objects.filter(comp_isin=OuterRef("ds_isin"))
    gfunda_reco_qs = Gfundareco.objects.filter(funda_reco_isin=OuterRef("ds_isin"))
    queryset = DematSum.objects.all(). \
        annotate(comp_rank=Subquery(amfi_qs.values('comp_rank')[:1])). \
        annotate(cap_type=Lower(Trim(Subquery(amfi_qs.values('cap_type')[:1])))). \
        annotate(funda_reco_type=Subquery(gfunda_reco_qs.values('funda_reco_type')[:1])). \
        annotate(funda_reco_cause=Subquery(gfunda_reco_qs.values('funda_reco_cause')[:1])). \
        values('ds_ticker', 'ds_costvalue', 'comp_rank', 'cap_type', 'funda_reco_type',
               'funda_reco_cause'). \
        order_by('comp_rank')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class DematSumAmountView(ListView):
    # model = DematSum

    # if pagination is desired
    # paginate_by = 300

    # amfi_qset = Amfi.objects.filter(comp_isin=OuterRef('pk'))
    # queryset = DematSum.objects.annotate(comp_rank=Subquery(amfi_qset.values('comp_rank'))).order_by('comp_rank')
    # queryset = DematSum.objects.annotate(comp_rank=Subquery(amfi_qset.values('comp_rank')))
    queryset = DematSum.objects.all(). \
        values('ds_ticker', 'ds_costvalue'). \
        order_by('-ds_costvalue')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class DematSumCapTypeView(ListView):
    # model = DematSum

    # if pagination is desired
    # paginate_by = 300

    # amfi_qset = Amfi.objects.filter(comp_isin=OuterRef('pk'))
    # queryset = DematSum.objects.annotate(comp_rank=Subquery(amfi_qset.values('comp_rank'))).order_by('comp_rank')
    # queryset = DematSum.objects.annotate(comp_rank=Subquery(amfi_qset.values('comp_rank')))

    def get_queryset(self):
        self.amfi_qs = Amfi.objects.filter(comp_isin=OuterRef("ds_isin"))
        self.queryset = DematSum.objects.all().filter(ds_user_id=self.request.user.id). \
            annotate(comp_rank=Subquery(self.amfi_qs.values('comp_rank')[:1])). \
            annotate(cap_type=Lower(Trim(Subquery(self.amfi_qs.values('cap_type')[:1])))). \
            values('cap_type'). \
            annotate(cap_count=Count('cap_type')). \
            annotate(cap_cost=Round(Sum('ds_costvalue'))). \
            order_by('cap_type')

        return self.queryset

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(DematSumCapTypeView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        amfi_qs = Amfi.objects.filter(comp_isin=OuterRef("ds_isin"))
        self.queryset = DematSum.objects.all().filter(ds_user_id=self.request.user.id). \
            annotate(comp_rank=Subquery(self.amfi_qs.values('comp_rank')[:1])). \
            annotate(cap_type=Lower(Trim(Subquery(amfi_qs.values('cap_type')[:1])))). \
            values('cap_type'). \
            annotate(cap_count=Count('cap_type')). \
            annotate(cap_cost=Round(Sum('ds_costvalue'))). \
            order_by('cap_type')

        direct_equity_amount = 0
        cap_type_list = []
        cap_amount_dict = {}
        cap_pct_dict = {}
        cap_count_dict = {}
        for q in self.queryset:
            print('q ', q)
            # exclude non cap_type - like gold, etf etc
            cap_type = q['cap_type']
            if cap_type:
                if cap_type not in cap_type_list:
                    cap_type_list.append(cap_type)
                if cap_type in cap_amount_dict:
                    cap_amount_dict[cap_type] += q['cap_cost']
                else:
                    cap_amount_dict[cap_type] = q['cap_cost']
                if cap_type in cap_count_dict:
                    cap_count_dict[cap_type] += q['cap_count']
                else:
                    cap_count_dict[cap_type] = q['cap_count']
                direct_equity_amount += q['cap_cost']
        context['direct_equity_amount'] = int(direct_equity_amount)

        cap_type_list.sort()
        print('cap_type_list ', cap_type_list)

        for cap_type in cap_amount_dict:
            cap_pct_dict[cap_type] = int(cap_amount_dict[cap_type] * 100.0 / int(direct_equity_amount))

        # fig = make_subplots(rows=2, cols=1)

        # expected distribution - 14%, 28%, 58%
        expected_pct_list = [58, 28, 14]
        actual_pct_list = [cap_pct_dict['large cap'], cap_pct_dict['mid cap'], cap_pct_dict['small cap']]

        print(cap_pct_dict);

        fig_1 = go.Figure(data=[
            go.Bar(name='Expected %', x=cap_type_list, y=expected_pct_list, text=expected_pct_list,
                   textposition='auto', ),
            go.Bar(name='Actual %', x=cap_type_list, y=actual_pct_list, text=actual_pct_list,
                   textposition='auto', )
        ])
        # Change the bar mode
        fig_1.update_layout(barmode='group')
        # fig.update_layout(yaxis_tickformat='%')
        # fig.update_traces(textposition='inside', textinfo='percent')
        # fig.show()

        # plot_div = plot(fig, output_type='div', include_plotlyjs=False)
        # context['plot_div'] = plot_div

        plot_div_1 = plot(fig_1, output_type='div', include_plotlyjs=False)
        context['plot_div_1'] = plot_div_1

        # expected companies distribution - 50 L - portfolio - 28, 28, 29
        # expected companies distribution - 1 Cr - portfolio - 58, 56, 56
        expected_count_list = [58, 56, 56]
        actual_count_list = [cap_count_dict['large cap'], cap_count_dict['mid cap'], cap_count_dict['small cap']]
        fig_2 = go.Figure(data=[
            go.Bar(name='Expected Count', x=cap_type_list, y=expected_count_list, text=expected_count_list,
                   textposition='auto', ),
            go.Bar(name='Actual Count', x=cap_type_list, y=actual_count_list, text=actual_count_list,
                   textposition='auto', )
        ])
        # Change the bar mode
        fig_2.update_layout(barmode='group')

        plot_div_2 = plot(fig_2, output_type='div', include_plotlyjs=False)
        context['plot_div_2'] = plot_div_2

        return context

class DematSumRefreshView(View):
    fr_buy = {}
    fr_hold = {}
    fr_enabled = {}
    isin_industry_dict = {}
    debug_level = 1

    def get(self, request):
        self.dematsum_refresh(request)
        return HttpResponseRedirect(reverse("dematsum-list"))

    def __init__(self):
        super(DematSumRefreshView, self).__init__()

    def dematsum_refresh(self, request):
        debug_level = 1
        # declaring template
        template = "gfundareco/gfunda_reco_list.html"

        # first delete all existing dematsum objects
        DematSum.objects.all().filter(ds_user_id=request.user.id).delete()
        max_id_instances = DematSum.objects.aggregate(max_id=Max('ds_id'))
        max_ds_id = max_id_instances['max_id']
        print('DS: found max id ', max_ds_id)
        if max_ds_id is None:
            max_ds_id = 0
            print('max_ds_id ', max_ds_id)

        unique_id = max_ds_id
        for brec in BrokerSum.objects.all().filter(bs_user_id=request.user.id):
            unique_id += 1
            print(brec.bs_stock_symbol, brec.bs_isin_code_id, brec.bs_qty)
            print(brec.bs_acp, brec.bs_value_cost, brec.bs_value_market)
            _, created = DematSum.objects.update_or_create(
                ds_id=unique_id,
                ds_user_id=request.user.id,
                ds_broker=brec.bs_broker,
                ds_ticker=brec.bs_stock_symbol,
                ds_isin=brec.bs_isin_code_id,
                ds_qty=brec.bs_qty,
                ds_acp=brec.bs_acp,
                ds_costvalue=brec.bs_value_cost,
                ds_mktvalue=brec.bs_value_market
            )

        # breakpoint()

        # import pdb
        # pdb.set_trace()

        # Updated Gfundareco objects
        lastrefd_update("dematsum")
