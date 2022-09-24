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

from django_gotolong.amfi.models import Amfi

from django_gotolong.lastrefd.models import Lastrefd, lastrefd_update

from django_gotolong.comm import comfun

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class BrokerTxnListView(ListView):
    model = BrokerTxn

    # if pagination is desired
    # paginate_by = 300
    # queryset = BrokerTxn.objects.all()
    # month_list = BrokerTxn.objects.dates('txn_date', 'month')

    def get_queryset(self):
        return BrokerTxn.objects.all().filter(bt_user_id=self.request.user.id)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(BrokerTxnListView, self).dispatch(*args, **kwargs)

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

    broker_name = request.POST["broker"]
    print('broker is ', broker_name)

    list_url_name = "broker-txn-list"
    template = "invalid-get-request.html"

    if broker_name == "IcicSec" or broker_name == 'Zerodha' or broker_name == 'HdfcSec':
        # unused - right now
        # change column name of data frame
        columns_list = ['bt_stock_symbol', 'bt_company_name', 'bt_isin_code', 'bt_action', 'bt_quantity',
                        'bt_txn_price', 'bt_brokerage', 'bt_txn_charges', 'bt_stamp_duty',
                        'bt_segment', 'bt_stt', 'bt_remarks', 'bt_txn_date',
                        'bt_exchange', 'bt_unused1']
    else:
        print('Unsupported broker: ', broker_name)
        return HttpResponseRedirect(reverse(list_url_name))

    # get rid of top 7 lines
    if broker_name == 'HdfcSec':
        ignore_top_lines = 7
    else:
        ignore_top_lines = 0
    data_set = comfun.comm_func_upload(request, template, columns_list, list_url_name, ignore_top_lines)

    # delete existing records
    print('Deleted existing BrokerTxn data')
    BrokerTxn.objects.all().filter(bt_broker=broker_name).filter(bt_user_id=request.user.id).delete()
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

        print(unique_id, column)

        bt_stock_symbol = 'UNmapped'
        bt_company_name = 'Unmapped'
        bt_isin_code = 'Unmapped'
        bt_action = 'Unknown'
        bt_quantity = 0
        bt_txn_price = 0
        bt_brokerage = 0
        bt_txn_charges = 0
        bt_stamp_duty = 0
        bt_segment = 'Unknown'
        bt_stt = 0
        bt_remarks = 'Unknown'
        bt_txn_date = ''
        bt_exchange = 'Unknown'
        bt_unused1 = ''

        if broker_name == "IcicSec":
            # ICICI Direct
            # 0-4 Stock Symbol,	Company Name,	ISIN Code,	Action,	Quantity
            # 5-9 Transaction Price,	Brokerage,	Transaction Charges,	StampDuty,	Segment
            # 10-13 STT Paid/Not Paid,	Remarks,	Transaction Date,	Exchange
            column[0] = column[0].strip()
            column[1] = column[1].strip()

            bt_stock_symbol = column[0]
            bt_company_name = column[1]
            bt_isin_code = column[2]
            bt_action = column[3]
            bt_quantity = column[4]
            bt_txn_price = column[5]
            bt_brokerage = column[6]
            bt_txn_charges = column[7]
            bt_stamp_duty = column[8]
            bt_segment = column[9]
            bt_stt = column[10]
            bt_remarks = column[11]
            # convert dd-mmm-yy to YYYY-mm-dd
            bt_txn_date = txn_date_iso(request, column[12])
            bt_exchange = column[13]
            bt_unused1 = column[14]
        elif broker_name == 'Zerodha':
            # Zerodha
            # 0-4  trade_date, tradingsymbol, exchange,	segment, trade_type
            # 5-9 quantity,	price,	order_id,	trade_id, order_execution_time
            bt_stock_symbol = column[1]
            # bt_company_name =
            # bt_isin_code =
            bt_action = column[4]
            bt_quantity = int(float(column[5]))
            bt_txn_price = column[6]
            # bt_brokerage = column[6]
            # bt_txn_charges = column[7]
            # bt_stamp_duty = column[8]
            bt_segment = column[3]
            # bt_stt = column[10]
            # bt_remarks = column[11]
            # convert dd-mmm-yy to YYYY-mm-dd
            bt_txn_date = column[0]
            bt_exchange = column[2]
            # bt_unused1 =
        elif broker_name == 'HdfcSec':
            # HDFC Securities
            # 0-6 Trd Dt,	Trd No.,	Order No.,	Exch (NSE),	Sett No,  Sett Type, Trade Time,
            # 7-12 Order Time, 	Scrip Name, Buy/Sell (B|S), 	Qty, 	Mkt	Price, Mkt Value,
            # 13-17 Squp/Del,	Brok Amount,	Service Tax, 	Stamp Duty, Transn Charge,
            # 18-22 Serv Tax on Txn Charge, STT,	Sebi Turnover Tax, 	Edu	Cess, High Edu Cess,
            # 23-27 Other	charges, Net Amount, Product (Cash) , SIP Flag, 	SIP Ref No

            scrip_name = column[8]
            # get the first name from scrip name like 'CAMPUS ACTIVEWEAR LIMITED'
            first_name = scrip_name.split(' ', 1)[0]
            # use upper case
            first_name = first_name.upper()
            # no longer using isin to name lookup

            scrip_ticker = scrip_name
            amfi_obj = Amfi.objects.filter(comp_name__contains=first_name).first()
            if amfi_obj:
                scrip_ticker = amfi_obj.nse_symbol
            else:
                print('amfi obj failed for scrip name', scrip_name, 'first name', first_name)

            bt_stock_symbol = scrip_ticker
            # get rid of 00:00:00 from date
            bt_txn_date = column[0].split(' ', 1)[0]
            print('txn date', bt_txn_date)

            bt_exchange = column[3]
            bt_action = column[9]

            if bt_action == 'B' or bt_action == 'S':
                if bt_action == 'B':
                    bt_action = 'Buy'
                if bt_action == 'S':
                    bt_action = 'Sell'

            bt_quantity = int(float(column[10]))
            bt_txn_price = column[11]
            bt_segment = column[25]

        else:
            print('Unknown broker:', broker_name)

        _, created = BrokerTxn.objects.update_or_create(
            bt_id=unique_id,
            bt_user_id=request.user.id,
            bt_broker=broker_name,
            bt_stock_symbol=bt_stock_symbol,
            bt_company_name=bt_company_name,
            bt_isin_code=bt_isin_code,
            bt_action=bt_action,
            bt_quantity=bt_quantity,
            bt_txn_price=bt_txn_price,
            bt_brokerage=bt_brokerage,
            bt_txn_charges=bt_txn_charges,
            bt_stamp_duty=bt_stamp_duty,
            bt_segment=bt_segment,
            bt_stt=bt_stt,
            bt_remarks=bt_remarks,
            bt_txn_date=bt_txn_date,
            bt_exchange=bt_exchange,
            bt_unused1=bt_unused1
        )

    lastrefd_update("broker-txn")

    print('Completed loading new BrokerTxn data')
    return HttpResponseRedirect(reverse(list_url_name))

def BrokerTxnReset(request):
    # delete existing records
    print('Cleared existing BrokerTxn data')
    BrokerTxn.objects.all().filter(bt_user_id=request.user.id).delete()
    return HttpResponseRedirect(reverse("broker-txn-list"))
