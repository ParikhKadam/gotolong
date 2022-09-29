# Create your views here.

# Create your views here.

from django.views.generic.list import ListView

from django.urls import reverse

from django.http import HttpResponseRedirect
from django.db import transaction

# from django_filters.rest_framework import DjangoFilterBackend, FilterSet, OrderingFilter

import urllib.request
import csv
import io
import requests

from datetime import date, timedelta
import pandas as pd

from django_gotolong.bhav.models import Bhav

from django_gotolong.amfi.models import Amfi, amfi_load_rank
from django_gotolong.dematsum.models import DematSum, dematsum_load_stocks
from django_gotolong.comm import comfun

from django_gotolong.lastrefd.models import Lastrefd, lastrefd_update

from apscheduler.schedulers.background import BackgroundScheduler

from django_gotolong.lastrefd.models import Lastrefd, lastrefd_update, \
    lastrefd_same_day, lastrefd_same_time


def bhav_url():
    # last working day
    # how about 3 based on today's day
    # weekday as a number
    # current_week_day = date.today().strftime('%W')
    current_week_day = date.today().weekday()
    if current_week_day == 6:
        # sunday
        days_diff = 2
    elif current_week_day == 0:
        # monday
        days_diff = 3
    else:
        days_diff = 1
    print('days_diff ', days_diff)
    current_date = date.today() - timedelta(days=days_diff)
    cur_year = current_date.year
    # abbreviation in upper case
    cur_month = current_date.strftime('%b').upper()
    cur_day = current_date.strftime('%d')

    url = 'https://archives.nseindia.com/content/historical/EQUITIES/' + str(cur_year) + '/' + str(cur_month) + '/cm'
    url += str(cur_day) + str(cur_month) + str(cur_year) + 'bhav.csv.zip'

    return url


def cmp_url():
    # https://www.nseindia.com/api/quote-equity?symbol=TCS
    # https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%20500
    url = "https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%20500"
    return url


class BhavListView(ListView):
    model = Bhav
    # if pagination is desired
    # paginate_by = 300
    # filter_backends = [filters.OrderingFilter,]
    # ordering_fields = ['sno', 'nse_symbol']
    queryset = Bhav.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        refresh_url = bhav_url()
        context["refresh_url"] = refresh_url
        refresh_url_2 = cmp_url()
        context["refresh_url_2"] = refresh_url_2
        return context


# one parameter named request
def bhav_fetch_yday(request):
    # for quick debugging
    #
    # import pdb; pdb.set_trace()
    #
    # breakpoint()

    debug_level = 1

    # last refresh date is same
    if lastrefd_same_day("bhav"):
        print('bhav_fetch_yday: skipped as last refresh date is same')
        return HttpResponseRedirect(reverse("bhav-list"))

    amfi_rank_dict = {}
    dematsum_list = []

    print("load amfi")
    # load rank
    amfi_load_rank(amfi_rank_dict)

    print("load dematsum")
    dematsum_load_stocks(dematsum_list)

    # declaring template
    template = "bhav/amfi_list.html"

    url = bhav_url()

    print(url)

    response = urllib.request.urlopen(url)

    status_code = response.getcode()
    # successful
    if status_code == 200:
        print('deleted existing Bhav data')
        # delete existing data
        Bhav.objects.all().delete()

    df = pd.read_csv(io.BytesIO(response.read()), compression='zip', sep=',', header=None)

    data_set = df.to_csv(header=False, index=False)

    io_string = io.StringIO(data_set)
    next(io_string)
    print('first record', io_string)
    skipped_records = 0
    for column in csv.reader(io_string, delimiter=',', quotechar='"'):
        bhav_ticker = column[0].strip()
        bhav_series = column[1].strip()
        bhav_open = column[2].strip()
        bhav_high = column[3].strip()
        bhav_low = column[4].strip()
        bhav_close = column[5].strip()
        bhav_last = column[6].strip()
        bhav_prevclose = column[7].strip()
        bhav_tottrdqty = column[8].strip()
        bhav_tottrdval = column[9].strip()
        bhav_timestamp = column[10].strip()
        bhav_totaltrades = column[11].strip()
        bhav_isin = column[12].strip()

        if bhav_series == 'EQ':
            if comfun.comm_func_ticker_match(bhav_ticker, amfi_rank_dict, dematsum_list):
                _, created = Bhav.objects.update_or_create(
                    bhav_ticker=bhav_ticker,
                    bhav_price=bhav_last,
                    bhav_isin=bhav_isin
                )
        else:
            skipped_records += 1

    lastrefd_update("bhav")

    print('Skipped records ', skipped_records)
    print('Completed updating Bhav data for yday')
    # context = {}
    # render(request, template, context)

    #
    return HttpResponseRedirect(reverse("bhav-list"))


# one parameter named request
def bhav_fetch_today(request):
    # for quick debugging
    #
    # import pdb; pdb.set_trace()
    #
    # breakpoint()

    debug_level = 1

    # last refresh date is same
    if lastrefd_same_time("bhav"):
        print('bhav_fetch: skipped as last refresh date is same')
        return HttpResponseRedirect(reverse("bhav-list"))

    amfi_rank_dict = {}
    dematsum_list = []

    print("load amfi")
    # load rank
    amfi_load_rank(amfi_rank_dict)

    print("load dematsum")
    dematsum_load_stocks(dematsum_list)

    # declaring template
    template = "bhav/amfi_list.html"

    url = cmp_url()

    print(url)

    # https://fineracy.com/get-live-data-of-national-stock-exchangense-stocks-of-all-symbolsnifty50-using-python/

    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; '
                             'x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'}

    main_url = "https://www.nseindia.com/"
    response = requests.get(main_url, headers=headers)
    print(response.status_code)
    cookies = response.cookies

    nifty500_data = requests.get(url, headers=headers, cookies=cookies)
    print(nifty500_data.status_code)

    if nifty500_data.status_code != 200:
        print('Failed status code ', nifty500_data.status_code)
        return HttpResponseRedirect(reverse("bhav-list"))

    nifty500_data = nifty500_data.json()
    print(nifty500_data)

    with transaction.atomic():
        for stocks in nifty500_data.get("data"):
            bhav_ticker = stocks['symbol']
            bhav_last = stocks['lastPrice']

            if comfun.comm_func_ticker_match(bhav_ticker, amfi_rank_dict, dematsum_list):
                Bhav.objects.filter(bhav_ticker=bhav_ticker).update(bhav_price=bhav_last)

            """
            _, created = Bhav.objects.update_or_create(
                    bhav_ticker=bhav_ticker,
                    bhav_price=bhav_last
            )
            """

            # obj = Bhav.objects.get(bhav_ticker=bhav_ticker)
            # new_values = {'bhav_last', bhav_last}
            # for key, value in new_values.items():
            #    setattr(obj, key, value)
            # obj.save()

    lastrefd_update("bhav")

    print('Completed updating Bhav data for today')
    # context = {}
    # render(request, template, context)

    return HttpResponseRedirect(reverse("bhav-list"))


# one parameter named request
def bhav_upload(request):
    # for quick debugging
    #
    # import pdb; pdb.set_trace()
    #
    # breakpoint()

    amfi_rank_dict = {}
    dematsum_list = []
    debug_level = 1
    # declaring template
    template = "bhav/amfi_list.html"
    data = Bhav.objects.all()

    # GET request returns the value of the data with the specified key.
    if request.method == "GET":
        return render(request, template)

    print("load amfi")
    # load rank
    amfi_load_rank(amfi_rank_dict)

    print("load dematsum")
    dematsum_load_stocks(dematsum_list)

    req_file = request.FILES['file']

    # let's check if it is a csv file
    skipped_records = 0
    if req_file.name.endswith('.xls') or req_file.name.endswith('.xlsx'):
        # get worksheet name
        # print('temporary file path:', req_file.temporary_file_path)
        print(req_file)

        if True:
            wb = openpyxl.load_workbook(req_file)
            print(wb.sheetnames)
            sheet_name = wb.sheetnames[0]
            print(sheet_name)
            ws = wb[sheet_name]
            df = pd.DataFrame(ws.values)
        else:
            xl = pd.ExcelFile(req_file)
            if debug_level > 0:
                print(xl.sheet_names)
            # single worksheet - Data
            sheet_name = xl.sheet_names[0]
            df = xl.parse(sheet_name)

        # can be 'Data'
        # can be 'Average MCap Jan Jun 2020'
        if sheet_name != 'Data':
            print("sheet name changed to", sheet_name)

        # ignore top two line : Average Market Capitalization of listed companies during the six months ended
        # remove top two line from dataframe
        df = df.iloc[2:]

        if debug_level > 0:
            print("old columns : ")
            print(df.columns)

        # change column name of data frame
        columns_list = ['SYMBOL', 'SERIES', 'OPEN',
                        'HIGH', 'LOW', 'CLOSE', 'LAST',
                        'PREVCLOSE', 'TOTTRDQTY', 'TOTTRDVAL', 'TIMESTAMP',
                        'TOTALTRADES', 'ISIN']
        df.columns = columns_list

        if debug_level > 0:
            print("new columns : ")
            print(df.columns)

        # Keep only top 1000 entries
        df = df.iloc[:1000]

        # round avg_mcap
        # df = df.round({'avg_mcap' : 1})
        # covert to numeric
        # df[["avg_mcap"]] = df[["avg_mcap"]].apply(pd.to_numeric)
        df[["avg_mcap"]] = df[["avg_mcap"]].astype(int)

        # drop columns that are not required
        # skip_columns_list = ['bse_mcap', 'nse_mcap', 'mse_symbol', 'mse_mcap']
        # df.drop(skip_columns_list, axis=1, inplace=True)

        data_set = df.to_csv(header=True, index=False)

    if req_file.name.endswith('.csv'):
        data_set = req_file.read().decode('UTF-8')

    if not (req_file.name.endswith('.csv') or req_file.name.endswith('.xls') or req_file.name.endswith('.xlsx')):
        messages.error(request, req_file.name + ' : THIS IS NOT A XLS/XLSX/CSV FILE.')
        return HttpResponseRedirect(reverse("bhav-list"))

    # delete existing records
    print('Deleted existing Bhav data')
    Bhav.objects.all().delete()

    # setup a stream which is when we loop through each line we are able to handle a data in a stream

    io_string = io.StringIO(data_set)
    next(io_string)

    for column in csv.reader(io_string, delimiter=',', quotechar='"'):
        bhav_ticker = column[0].strip()
        bhav_series = column[1].strip()
        bhav_open = column[2].strip()
        bhav_high = column[3].strip()
        bhav_low = column[4].strip()
        bhav_close = column[5].strip()
        bhav_last = column[6].strip()
        bhav_prevclose = column[7].strip()
        bhav_tottrdqty = column[8].strip()
        bhav_tottrdval = column[9].strip()
        bhav_timestamp = column[10].strip()
        bhav_totaltrades = column[11].strip()
        bhav_isin = column[12].strip()

        # skip some rows
        # retail investors series : EQ and BE
        # EQ - intra day trade allowed (normal trading)
        # BE - trade to trade/T-segment : (no intra day squaring allowed : (accept/give delivery)
        if bhav_series == 'EQ':
            if comfun.comm_func_ticker_match(bhav_ticker, amfi_rank_dict, dematsum_list):
                _, created = Bhav.objects.update_or_create(
                    bhav_ticker=bhav_ticker,
                    bhav_price=bhav_last,
                    bhav_isin=bhav_isin
                )
        else:
            skipped_records += 1

    # context = {}
    # render(request, template, context)
    lastrefd_update("bhav")
    #

    print('skipped records: ', skipped_records)
    print('Completed loading new Bhav data')
    return HttpResponseRedirect(reverse("bhav-list"))

# from django.http import HttpResponse
# def index(request):
#    return HttpResponse("Hello, world. You're at the polls index.")
#

