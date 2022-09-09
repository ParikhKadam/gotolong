# Create your views here.

from .models import Mfund

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

import pandas as pd
import csv, io
import openpyxl
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect

from django_gotolong.lastrefd.models import Lastrefd, lastrefd_update

from django_gotolong.brokermf.models import BrokerMf


def Mfund_url():
    return "unused-mfund-refresh-url"


class MfundListView(ListView):
    model = Mfund

    # if pagination is desired
    # paginate_by = 300
    # filter_backends = [filters.OrderingFilter,]
    # ordering_fields = ['sno', 'nse_symbol']

    def get_queryset(self):
        queryset = Mfund.objects.all().filter(mf_user_id=self.request.user.id)
        return queryset

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(MfundListView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        refresh_url = Mfund_url()
        context["refresh_url"] = refresh_url
        return context


class MfundListView_AMC_Amount(ListView):
    model = Mfund

    def get_queryset(self):
        self.queryset = Mfund.objects.all().filter(mf_user_id=self.request.user.id). \
            values('mf_amc').annotate(scheme_sum=Sum('mf_nav_value')). \
            exclude(scheme_sum=0.0).order_by('-scheme_sum')
        print('hi ', self.queryset)
        return self.queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        labels = []
        values = []
        labels_values_dict = {}
        sum_total = 0
        for q_row in self.queryset:
            sum_total += q_row['scheme_sum']
            labels_values_dict[q_row['mf_amc']] = q_row['scheme_sum']
        context['sum_total'] = int(sum_total)

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
        app_label = 'mfund'
        template_name_first = app_label + '/' + 'mfund_aggregate.html'
        template_names_list = [template_name_first]
        return template_names_list


class MfundListView_SubcatAmount(ListView):
    model = Mfund

    def get_queryset(self):
        self.queryset = Mfund.objects.all().filter(mf_user_id=self.request.user.id). \
            values('mf_subcat').annotate(scheme_sum=Sum('mf_nav_value')). \
            exclude(scheme_sum=0.0).order_by('-scheme_sum')
        return self.queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        labels = []
        values = []
        labels_values_dict = {}
        sum_total = 0
        for q_row in self.queryset:
            sum_total += q_row['scheme_sum']
            labels_values_dict[q_row['mf_subcat']] = q_row['scheme_sum']
        context['sum_total'] = int(sum_total)

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
        app_label = 'mfund'
        template_name_first = app_label + '/' + 'mfund_aggregate.html'
        template_names_list = [template_name_first]
        return template_names_list


class MfundListView_Rebalance(ListView):
    model = Mfund

    def get_queryset(self):
        queryset = Mfund.objects.all().filter(mf_user_id=self.request.user.id). \
            order_by('mf_amc', 'mf_category', 'mf_subcat', '-mf_nav_value')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        refresh_url = Mfund_url()
        context["refresh_url"] = refresh_url
        return context

    def get_template_names(self):
        app_label = 'mfund'
        template_name_first = app_label + '/' + 'mfund_rebalance_list.html'
        template_names_list = [template_name_first]
        return template_names_list


class MfundRefreshView(View):
    debug_level = 1

    def get(self, request):
        self.mfund_refresh(request)
        return HttpResponseRedirect(reverse("mfund-list"))

    def __init__(self):
        super(MfundRefreshView, self).__init__()

    def mfund_refresh(self, request):
        debug_level = 1
        # declaring template

        # first delete all existing mfund objects
        Mfund.objects.all().filter(mf_user_id=request.user.id).delete()
        max_id_instances = Mfund.objects.aggregate(max_id=Max('mf_id'))
        max_mf_id = max_id_instances['max_id']
        print('DS: found max id ', max_mf_id)
        if max_mf_id is None:
            max_mf_id = 0
            print('max_mf_id ', max_mf_id)

        unique_id = max_mf_id
        for brec in BrokerMf.objects.all().filter(bmf_user_id=request.user.id):
            unique_id += 1
            print(brec.bmf_amc, brec.bmf_name, brec.bmf_category, brec.bmf_subcat)
            print(brec.bmf_rating, brec.bmf_units, brec.bmf_cost_value, brec.bmf_nav_value)
            print(brec.bmf_research_reco)
            # skip 0 units
            if int(float(brec.bmf_units)) != 0:
                _, created = Mfund.objects.update_or_create(
                    mf_id=unique_id,
                    mf_user_id=request.user.id,
                    mf_broker=brec.bmf_broker,
                    mf_amc=brec.bmf_amc,
                    mf_name=brec.bmf_name,
                    mf_category=brec.bmf_category,
                    mf_subcat=brec.bmf_subcat,
                    mf_rating=brec.bmf_rating,
                    mf_cost_value=brec.bmf_cost_value,
                    mf_nav_value=brec.bmf_nav_value,
                    mf_research_reco=brec.bmf_research_reco
                )

        # breakpoint()

        # import pdb
        # pdb.set_trace()

        # Updated Gfundareco objects
        lastrefd_update("mfund")
