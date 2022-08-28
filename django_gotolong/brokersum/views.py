# Create your views here.

from .models import BrokerSum

from django.shortcuts import render, redirect, get_object_or_404

from django.views.generic.list import ListView

from django.db.models import OuterRef, Subquery, Count, Sum, Max, Min
from django.db.models.functions import Trim, Lower, Round

from django_gotolong.amfi.models import Amfi, amfi_load_isin2ticker
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

    broker_name = request.POST["broker"]
    print('broker is ', broker_name)

    amfi_isin2ticker_dict = {}
    amfi_load_isin2ticker(amfi_isin2ticker_dict)

    template = "invalid-get-request.html"

    list_url_name = "broker-sum-list"

    if broker_name == "IcicSec" or broker_name == 'Zerodha' or broker_name == 'HdfcSec':
        # change column name of data frame
        '''
        columns_list = ['bs_stock_symbol', 'bs_company_name', 'bs_isin_code_id',
                        'bs_qty', 'bs_acp', 'bs_cmp', 'bs_pct_change', 'bs_value_cost',
                        'bs_value_market', 'bs_days_gain', 'bs_days_gain_pct',
                        'bs_realized_pl', 'bs_unrealized_pl', 'bs_unrealized_pl_pct',
                        'bs_unused1']
        '''
    else:
        print('Unsupported broker: ', broker_name)
        return HttpResponseRedirect(reverse(list_url_name))

    # get rid of top 4 lines
    if broker_name == 'HdfcSec':
        ignore_top_lines = 5
    else:
        ignore_top_lines = 0
    data_set = comfun.comm_func_upload(request, template, columns_list, list_url_name, ignore_top_lines)

    # delete existing records
    print('Deleted existing BrokerSum data')
    BrokerSum.objects.all().filter(bs_broker=broker_name).filter(bs_user_id=request.user.id).delete()

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

        bs_stock_symbol = 'UNKNOWN'
        bs_company_name = 'Unmapped'
        bs_isin_code_id = 'Unmapped'
        bs_qty = 0
        bs_acp = 0
        bs_cmp = 0
        bs_pct_change = 0
        bs_value_cost = 0
        bs_value_market = 0
        bs_days_gain = 0
        bs_days_gain_pct = 0
        bs_realized_pl = 0
        bs_unrealized_pl = 0
        bs_unrealized_pl_pct = 0
        bs_unused1 = 'unused'

        if broker_name == "IcicSec":
            # Icidirect Summary
            # Stock Symbol	Company Name	ISIN Code	Qty	Average Cost Price
            # Current Market Price	% Change over prev close	Value At Cost
            # Value At Market Price	Days Gain	Days Gain %	Realized Profit / Loss
            # Unrealized Profit/Loss	Unrealized Profit/Loss %
            column[0] = column[0].strip()
            column[1] = column[1].strip()
            bs_stock_symbol = column[0]
            bs_company_name = column[1]
            bs_isin_code_id = column[2]

            # icici direct using its own symbol instead of NIFTY tickers
            if bs_isin_code_id in amfi_isin2ticker_dict:
                old_bs_stock_symbol = bs_stock_symbol
                bs_stock_symbol = amfi_isin2ticker_dict[bs_isin_code_id]
                print('old symbol: ', old_bs_stock_symbol, 'new ticker: ', bs_stock_symbol)
            else:
                print('using existing symbol as ticker')
            bs_qty = column[3]
            bs_acp = column[4]
            bs_cmp = column[5]
            bs_pct_change = column[6]
            bs_value_cost = column[7]
            bs_value_market = column[8]
            bs_days_gain = column[9]
            bs_days_gain_pct = column[10]
            bs_realized_pl = column[11]
            bs_unrealized_pl = column[12]
            bs_unrealized_pl_pct = column[13]
            bs_unused1 = column[14]
        elif broker_name == "Zerodha":
            # Zerodha Demat Data - excel sheet - first line
            # Instrument, Qty., Avg. cost, LTP, Cur. val, P&L, Net chg., Day chg.
            bs_stock_symbol = column[0]
            bs_qty = column[1]
            bs_acp = column[2]
            bs_cmp = column[3]
            bs_value_market = column[4]
            bs_unrealized_pl = column[5]
            # net change = column[6]
            bs_days_gain = column[7]
        elif broker_name == "HdfcSec":
            # Stock Name	ISIN	Sector Name	 Quantity	Average Cost Price	Value At Cost
            # Current Market Price
            # Current Market Price % Change,	Valuation at Current Market Price,	Unrealized Profit/Loss,
            # Unrealized Profit/Loss % Change,	Realized Profit/Loss,	Nearing Long term Quantity (within 30 days)
            #
            # name not ticker
            bs_stock_name = column[0]
            bs_isin_code_id = column[1]

            if bs_isin_code_id in amfi_isin2ticker_dict:
                bs_stock_symbol = amfi_isin2ticker_dict[bs_isin_code_id]
                print('hdfcsec - isin 2 ticker: ', bs_isin_code_id, bs_stock_symbol)

            # bs_sector = column[2]
            bs_qty = column[3]
            bs_acp = column[4]
            # value at cost
            bs_value_cost = column[5]
            bs_cmp = column[6]
            # cmp % change
            bs_value_market = column[8]
            bs_unrealized_pl = column[9]
            bs_unrealized_pl_pct = column[10]
            bs_realized_pl = column[11]
            # net change = column[6]
            # bs_days_gain = column[7]

        _, created = BrokerSum.objects.update_or_create(
            bs_id=unique_id,
            bs_user_id=request.user.id,
            bs_broker=broker_name,
            bs_stock_symbol=bs_stock_symbol,
            bs_company_name=bs_company_name,
            bs_isin_code_id=bs_isin_code_id,
            bs_qty=bs_qty,
            bs_acp=bs_acp,
            bs_cmp=bs_cmp,
            bs_pct_change=bs_pct_change,
            bs_value_cost=bs_value_cost,
            bs_value_market=bs_value_market,
            bs_days_gain=bs_days_gain,
            bs_days_gain_pct=bs_days_gain_pct,
            bs_realized_pl=bs_realized_pl,
            bs_unrealized_pl=bs_unrealized_pl,
            bs_unrealized_pl_pct=bs_unrealized_pl_pct,
            bs_unused1=bs_unused1
        )

    lastrefd_update("broker-sum")

    print('Completed loading new BrokerSum data')
    return HttpResponseRedirect(reverse(list_url_name))

def BrokerSumReset(request):
    # delete existing records
    print('Cleared existing BrokerSum data')
    BrokerSum.objects.all().filter(bs_user_id=request.user.id).delete()
    return HttpResponseRedirect(reverse("broker-sum-list"))
