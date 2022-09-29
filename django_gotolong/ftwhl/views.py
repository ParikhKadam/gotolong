# Create your views here.

# Create your views here.

from django.views.generic.list import ListView

# from django_filters.rest_framework import DjangoFilterBackend, FilterSet, OrderingFilter

from django.urls import reverse

from django.http import HttpResponseRedirect

from datetime import date, timedelta

import urllib3
import csv
import io

from django_gotolong.ftwhl.models import Ftwhl

from django_gotolong.amfi.models import Amfi, amfi_load_rank
from django_gotolong.dematsum.models import DematSum, dematsum_load_stocks
from django_gotolong.comm import comfun
from django_gotolong.lastrefd.models import Lastrefd, lastrefd_update, lastrefd_same_day

class FtwhlListView(ListView):
    model = Ftwhl
    # if pagination is desired
    # paginate_by = 300
    # filter_backends = [filters.OrderingFilter,]
    # ordering_fields = ['sno', 'nse_symbol']
    queryset = Ftwhl.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        refresh_url = ftwhl_url()
        context["refresh_url"] = refresh_url
        return context


def ftwhl_url():
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
    current_date = date.today() - timedelta(days=days_diff)

    cur_year = current_date.year
    # month name
    cur_month = current_date.strftime('%m')
    cur_day = current_date.strftime('%d')

    url = 'https://archives.nseindia.com/content/CM_52_wk_High_low_'
    url += str(cur_day) + str(cur_month) + str(cur_year) + '.csv'

    return url


# one parameter named request
def ftwhl_fetch(request):
    # for quick debugging
    #
    # import pdb; pdb.set_trace()
    #
    # breakpoint()

    debug_level = 1

    # last refresh date is same
    if lastrefd_same_day("ftwhl"):
        print('ftwhl_fetch: skipped as last refresh date is same')
        return HttpResponseRedirect(reverse("ftwhl-list"))

    amfi_rank_dict = {}
    dematsum_list = []

    print("load amfi")
    # load rank
    amfi_load_rank(amfi_rank_dict)

    print("load dematsum")
    dematsum_load_stocks(dematsum_list)

    # declaring template
    template = "ftwhl/ftwhl_list.html"
    data = Ftwhl.objects.all()

    url = ftwhl_url()

    print(url)

    http = urllib3.PoolManager()

    response = http.request('GET', url)

    print(response.status)

    if response.status == 200:
        print('delete existing ftwhl data')
        Ftwhl.objects.all().delete()

    resp_data = response.data

    # response data
    io_string = io.StringIO(resp_data.decode('utf-8'))
    # skip first three rows
    next(io_string)
    next(io_string)
    next(io_string)

    for column in csv.reader(io_string, delimiter=',', quotechar='"'):
        if debug_level > 1:
            print(column)

        ftwhl_ticker = column[0].strip()
        # ignore column[1] Series : EQ
        column[2] = column[2].strip()
        column[3] = column[3].strip()
        column[4] = column[4].strip()
        column[5] = column[5].strip()

        if comfun.comm_func_ticker_match(ftwhl_ticker, amfi_rank_dict, dematsum_list):
            _, created = Ftwhl.objects.update_or_create(
                ftwhl_ticker=ftwhl_ticker,
                ftwhl_high=column[2],
                ftwhl_high_dt=column[3],
                ftwhl_low=column[4],
                ftwhl_low_dt=column[5]
            )

    #
    lastrefd_update("ftwhl")
    return HttpResponseRedirect(reverse("ftwhl-list"))


# from django.http import HttpResponse
# def index(request):
#    return HttpResponse("Hello, world. You're at the polls index.")
#

# one parameter named request
def ftwhl_upload(request):
    # for quick debugging
    #
    # import pdb; pdb.set_trace()
    #
    # breakpoint()

    debug_level = 1
    # declaring template
    template = "ftwhl/ftwhl_list.html"
    data = Ftwhl.objects.all()

    # GET request returns the value of the data with the specified key.
    if request.method == "GET":
        return render(request, template)

    amfi_rank_dict = {}
    dematsum_list = []

    print("load amfi")
    # load rank
    amfi_load_rank(amfi_rank_dict)

    print("load dematsum")
    dematsum_load_stocks(dematsum_list)

    req_file = request.FILES['file']

    # let's check if it is a csv file

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
        columns_list = ["SYMBOL", "SERIES", "Adjusted 52_Week_High", "52_Week_High_Date", "Adjusted 52_Week_Low",
                        "52_Week_Low_DT"]
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
        return HttpResponseRedirect(reverse("ftwhl-list"))

    # delete existing records
    print('Deleted existing Ftwhl data')
    Ftwhl.objects.all().delete()

    # setup a stream which is when we loop through each line we are able to handle a data in a stream

    io_string = io.StringIO(data_set)
    # skip top three rows
    next(io_string)
    next(io_string)
    next(io_string)

    skip_records = 0
    for column in csv.reader(io_string, delimiter=',', quotechar='"'):
        ftwhl_ticker = column[0].strip()
        ftwhl_series = column[1].strip()
        ftwhl_high = column[2].strip()
        ftwhl_high_dt = column[3].strip()
        ftwhl_low = column[4].strip()
        ftwhl_low_dt = column[5].strip()

        # skip some rows
        # retail investors series : EQ and BE
        # EQ - intra day trade allowed (normal trading)
        # BE - trade to trade/T-segment : (no intra day squaring allowed : (accept/give delivery)
        if ftwhl_series == 'EQ':
            if comfun.comm_func_ticker_match(ftwhl_ticker, amfi_rank_dict, dematsum_list):
                _, created = Ftwhl.objects.update_or_create(
                    ftwhl_ticker=ftwhl_ticker,
                    ftwhl_high=ftwhl_high,
                    ftwhl_high_dt=ftwhl_high_dt,
                    ftwhl_low=ftwhl_low,
                    ftwhl_low_dt=ftwhl_low_dt
                )
        else:
            skip_records += 1
    # context = {}
    # render(request, template, context)
    lastrefd_update("ftwhl")
    #
    print('Skipped records', skip_records)
    print('Completed loading new Ftwhl data')
    return HttpResponseRedirect(reverse("ftwhl-list"))

# from django.http import HttpResponse
# def index(request):
#    return HttpResponse("Hello, world. You're at the polls index.")
#
