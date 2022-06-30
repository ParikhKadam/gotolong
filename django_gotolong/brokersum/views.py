# Create your views here.

from .models import BrokerSum

from django.shortcuts import render, redirect, get_object_or_404

from django.views.generic.list import ListView

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

from django_gotolong.comm import comfun

class BrokerSumListView(ListView):
    model = BrokerSum

    # if pagination is desired
    # paginate_by = 300

    def get_queryset(self):
        return BrokerSum.objects.all().filter(bs_user_id=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


# one parameter named request
def BrokerSumUpload(request):
    # for quick debugging
    #
    # import pdb; pdb.set_trace()
    #
    # breakpoint()

    print('broker is ', request.POST["broker"])

    template = "invalid-get-request.html"
    # change column name of data frame
    columns_list = ['bs_stock_symbol', 'bs_company_name', 'bs_isin_code_id', 'bs_qty', 'bs_acp',
                    'bs_cmp', 'bs_pct_change', 'bs_value_cost', 'bs_value_market',
                    'bs_days_gain', 'bs_days_gain_pct', 'bs_realized_pl', 'bs_unrealized_pl',
                    'bs_unrealized_pl_pct', 'bs_unused1']
    list_url_name = "broker-sum-list"
    data_set = comfun.comm_func_upload(request, template, columns_list, list_url_name)

    # delete existing records
    print('Deleted existing BrokerSum data')
    BrokerSum.objects.all().filter(bs_user_id=request.user.id).delete()

    max_id_instances = BrokerSum.objects.aggregate(max_id=Max('bs_id'))
    max_id = max_id_instances['max_id']
    print('max_id ', max_id)
    if max_id is None:
        max_id = 0
        print('max_id ', max_id)

    # setup a stream which is when we loop through each line we are able to handle a data in a stream

    io_string = io.StringIO(data_set)
    next(io_string)
    unique_id = max_id
    for column in csv.reader(io_string, delimiter=',', quotechar='"'):
        unique_id += 1
        column[0] = column[0].strip()
        column[1] = column[1].strip()

        _, created = BrokerSum.objects.update_or_create(
            bs_id=unique_id,
            bs_user_id=request.user.id,
            bs_broker=request.POST["broker"],
            bs_stock_symbol=column[0],
            bs_company_name=column[1],
            bs_isin_code_id=column[2],
            bs_qty=column[3],
            bs_acp=column[4],
            bs_cmp=column[5],
            bs_pct_change=column[6],
            bs_value_cost=column[7],
            bs_value_market=column[8],
            bs_days_gain=column[9],
            bs_days_gain_pct=column[10],
            bs_realized_pl=column[11],
            bs_unrealized_pl=column[12],
            bs_unrealized_pl_pct=column[13],
            bs_unused1=column[14]
        )

    lastrefd_update("broker-sum")

    print('Completed loading new BrokerSum data')
    return HttpResponseRedirect(reverse(list_url_name))

def BrokerSumReset(request):
    # delete existing records
    print('Cleared existing BrokerSum data')
    BrokerSum.objects.all().filter(bs_user_id=request.user.id).delete()
    return HttpResponseRedirect(reverse("broker-sum-list"))
