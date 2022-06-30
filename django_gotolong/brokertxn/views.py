# Create your views here.

from django_gotolong.brokertxn.models import BrokerTxn

from django.utils import timezone

from django.views.generic.list import ListView
from django.views.generic.dates import YearArchiveView, MonthArchiveView

from django.db.models import IntegerField, F, ExpressionWrapper, fields, Max, Min, Sum, Count
from django.db.models.functions import (ExtractYear, Round, ExtractMonth)
from django.db.models.expressions import RawSQL

import calendar
import pandas as pd
import csv, io
import openpyxl
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect

from django_gotolong.lastrefd.models import Lastrefd, lastrefd_update

from django_gotolong.comm import comfun

class BrokerTxnListView(ListView):
    model = BrokerTxn

    # if pagination is desired
    # paginate_by = 300
    # queryset = BrokerTxn.objects.all()
    # month_list = BrokerTxn.objects.dates('txn_date', 'month')

    def get_queryset(self):
        return BrokerTxn.objects.all().filter(bt_user_id=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


def txn_date_iso(self, txn_date):
    month_name_abbr_to_num_dict = {name: num for num, name in enumerate(calendar.month_abbr) if num}

    try:
        # dd-mmm-yy
        txn_date_arr = txn_date.split('-')
        txn_day = txn_date_arr[0].strip()
        txn_month = txn_date_arr[1].strip()
        txn_year = txn_date_arr[2].strip()
        if txn_month.isdigit():
            # get rid of leading 0 in month number
            txn_month = str(int(txn_month))
        else:
            # month name to number
            txn_month = str(month_name_abbr_to_num_dict[txn_month])
        txn_date_iso = txn_year + "-" + txn_month + "-" + txn_day
        # ignore rest
    except ValueError:
        logging.error('ValueError ', txn_date, row_list)
    except IndexError:
        logging.error('IndexError ', txn_date, row_list)

    return txn_date_iso


# one parameter named request
def BrokerTxnUpload(request):
    # for quick debugging
    #
    # import pdb; pdb.set_trace()
    #
    # breakpoint()

    template = "invalid-get-request.html"
    # change column name of data frame
    columns_list = ['bt_stock_symbol', 'bt_company_name', 'bt_isin_code', 'bt_action', 'bt_quantity',
                    'bt_txn_price', 'bt_brokerage', 'bt_txn_charges', 'bt_stamp_duty',
                    'bt_segment', 'bt_stt', 'bt_remarks', 'bt_txn_date',
                    'bt_exchange', 'bt_unused1']
    list_url_name = "broker-txn-list"
    data_set = comfun.comm_func_upload(request, template, columns_list, list_url_name)

    # delete existing records
    print('Deleted existing BrokerTxn data')
    BrokerTxn.objects.all().filter(bt_user_id=request.user.id).delete()
    max_id_instances = BrokerTxn.objects.aggregate(max_id=Max('bt_id'))
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

        # convert dd-mmm-yy to YYYY-mm-dd
        txn_date = txn_date_iso(request, column[12])

        print(unique_id, column)

        _, created = BrokerTxn.objects.update_or_create(
            bt_id=unique_id,
            bt_user_id=request.user.id,
            bt_broker=request.POST["broker"],
            bt_stock_symbol=column[0],
            bt_company_name=column[1],
            bt_isin_code=column[2],
            bt_action=column[3],
            bt_quantity=column[4],
            bt_txn_price=column[5],
            bt_brokerage=column[6],
            bt_txn_charges=column[7],
            bt_stamp_duty=column[8],
            bt_segment=column[9],
            bt_stt=column[10],
            bt_remarks=column[11],
            bt_txn_date=txn_date,
            bt_exchange=column[13],
            bt_unused1=column[14]
        )

    lastrefd_update("broker-txn")

    print('Completed loading new BrokerTxn data')
    return HttpResponseRedirect(reverse(list_url_name))

def BrokerTxnReset(request):
    # delete existing records
    print('Cleared existing BrokerTxn data')
    BrokerTxn.objects.all().filter(bt_user_id=request.user.id).delete()
    return HttpResponseRedirect(reverse("broker-txn-list"))
