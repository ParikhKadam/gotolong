# Create your views here.

from .models import BrokerMf

from django.views.generic.list import ListView

from django.db.models import IntegerField, F, ExpressionWrapper, fields, Max, Min, Sum, Count

from django.urls import reverse
from django.http import HttpResponseRedirect
import urllib3
import csv
import io

import re

import openpyxl

import pandas as pd

from django_gotolong.lastrefd.models import Lastrefd, lastrefd_update

from django_gotolong.comm import comfun

import plotly.graph_objects as go
from plotly.offline import plot
from plotly.tools import make_subplots


class BrokerMfListView(ListView):
    model = BrokerMf

    def get_queryset(self):
        queryset = BrokerMf.objects.all().filter(bmf_user_id=self.request.user.id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        refresh_url = BrokerMf_url()
        context["refresh_url"] = refresh_url
        return context


def BrokerMf_url():
    url = 'https://archives.nseindia.com/content/BrokerMf/ind_nifty500list.csv'

    return url


# one parameter named request
def BrokerMf_fetch(request):
    # for quick debugging
    #
    # import pdb; pdb.set_trace()
    #
    # breakpoint()
    debug_level = 1
    print('fetch not supported')
    return HttpResponseRedirect(reverse("broker-mf-list"))

# one parameter named request
def BrokerMf_upload(request):
    # for quick debugging
    #
    # import pdb; pdb.set_trace()
    #
    # breakpoint()

    broker_name = request.POST["broker"]
    print('broker is ', broker_name)

    template = "broker-mf/BrokerMf_list.html"

    list_url_name = "broker-mf-list"

    if broker_name == "IcicSec" or broker_name == 'Zerodha':
        # change column name of data frame
        columns_list = ["amc", "name", "category", "subcat", "rating",
                        "units", "acp", "cost_value",
                        "nav_date", "nav", "nav_value",
                        "pnl_realized", "pnl", "pnl_pct",
                        "research_reco"]

    else:
        print('Unsupported broker: ', broker_name)
        return HttpResponseRedirect(reverse(list_url_name))

    # get rid of top 4 lines
    if broker_name == 'HdfcSec':
        ignore_top_lines = 0
    else:
        ignore_top_lines = 0

    data_set = comfun.comm_func_upload(request, template, columns_list, list_url_name, ignore_top_lines)

    # delete existing records
    print('Deleted existing BrokerMf data')
    BrokerMf.objects.all().filter(bmf_broker=broker_name).filter(bmf_user_id=request.user.id).delete()

    # note: what about using existing slots... how do we fill holes
    #
    max_id_instances = BrokerMf.objects.aggregate(max_id=Max('bmf_id'))
    max_id = max_id_instances['max_id']
    print('max_id ', max_id)
    if max_id is None:
        max_id = 0
        print('max_id ', max_id)

    # setup a stream which is when we loop through each line we are able to handle a data in a stream

    io_string = io.StringIO(data_set)
    # skip top 1 row
    next(io_string)

    skip_records = 0
    unique_id = max_id
    for column in csv.reader(io_string, delimiter=',', quotechar='"'):
        unique_id += 1

        bmf_id = unique_id
        bmf_user_id = request.user.id
        bmf_broker = broker_name
        bmf_amc = 'Unknown'
        bmf_name = 'Unknown'
        bmf_category = 'Unknown'
        bmf_subcat = 'Unknown'
        bmf_rating = 'Unknown'
        bmf_units = 0
        bmf_acp = 0
        bmf_cost_value = 0
        bmf_nav_date = ''
        bmf_nav = 0
        bmf_nav_value = 0
        bmf_pnl_realized = 0
        bmf_pnl = 0
        bmf_pnl_pct = 0
        bmf_research_reco = 'Unknown'

        if broker_name == "IcicSec":
            bmf_amc = column[0].strip()
            bmf_name = column[1].strip()
            bmf_category = column[2].strip()
            bmf_subcat = column[3].strip()
            bmf_rating = column[4].strip()
            bmf_units = column[5].strip()
            bmf_acp = column[6].strip()
            bmf_cost_value = column[7].strip()
            bmf_nav_date = column[8].strip()
            bmf_nav = column[9].strip()
            bmf_nav_value = column[10].strip()
            bmf_pnl_realized = column[10].strip()
            bmf_pnl = column[12].strip()
            bmf_pnl_pct = column[13].strip()
            bmf_research_reco = column[14].strip()
        else:
            print('broker not supported: ', broker_name)
        # print('bmf_units ', bmf_units)
        # skip mutual funds with 0 holdings
        # if int(float(bmf_units)) !=  0 :

        _, created = BrokerMf.objects.update_or_create(
            bmf_id=unique_id,
            bmf_user_id=bmf_user_id,
            bmf_broker=bmf_broker,
            bmf_amc=bmf_amc,
            bmf_name=bmf_name,
            bmf_category=bmf_category,
            bmf_subcat=bmf_subcat,
            bmf_rating=bmf_rating,
            bmf_units=bmf_units,
            bmf_acp=bmf_acp,
            bmf_cost_value=bmf_cost_value,
            bmf_nav_date=bmf_nav_date,
            bmf_nav=bmf_nav,
            bmf_nav_value=bmf_nav_value,
            bmf_pnl_realized=bmf_pnl_realized,
            bmf_pnl=bmf_pnl,
            bmf_pnl_pct=bmf_pnl_pct,
            bmf_research_reco=bmf_research_reco
        )

    lastrefd_update("broker-mf")

    print('Skipped records', skip_records)
    print('Completed loading new BrokerMf data')
    return HttpResponseRedirect(reverse(list_url_name))
