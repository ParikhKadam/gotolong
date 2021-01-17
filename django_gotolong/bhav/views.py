# Create your views here.

# Create your views here.

from django.views.generic.list import ListView

from django.urls import reverse

from django.http import HttpResponseRedirect

# from django_filters.rest_framework import DjangoFilterBackend, FilterSet, OrderingFilter

import urllib.request
import csv
import io

from datetime import date, timedelta

from django_gotolong.bhav.models import Bhav

import pandas as pd


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
        return context


def bhav_url():
    # last working day
    # how about 3 based on today's day
    current_date = date.today() - timedelta(days=1)
    cur_year = current_date.year
    # abbreviation in upper case
    cur_month = current_date.strftime('%b').upper()
    cur_day = current_date.strftime('%d')

    url = 'https://archives.nseindia.com/content/historical/EQUITIES/' + str(cur_year) + '/' + str(cur_month) + '/cm'
    url += str(cur_day) + str(cur_month) + str(cur_year) + 'bhav.csv.zip'

    return url


# one parameter named request
def bhav_fetch(request):
    # for quick debugging
    #
    # import pdb; pdb.set_trace()
    #
    # breakpoint()

    debug_level = 1
    # declaring template
    template = "bhav/bhav_list.html"

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
    for column in csv.reader(io_string, delimiter=',', quotechar='"'):
        column[0] = column[0].strip()

        _, created = Bhav.objects.update_or_create(
            bhav_ticker=column[0],
            bhav_price=column[6],
            bhav_isin=column[12]
        )
    print('Completed updating Bhav data')
    # context = {}
    # render(request, template, context)
    return HttpResponseRedirect(reverse("bhav-list"))


# from django.http import HttpResponse
# def index(request):
#    return HttpResponse("Hello, world. You're at the polls index.")

# one parameter named request
def bhav_upload(request):
    # for quick debugging
    #
    # import pdb; pdb.set_trace()
    #
    # breakpoint()

    debug_level = 1
    # declaring template
    template = "bhav/bhav_list.html"
    data = Bhav.objects.all()

    # GET request returns the value of the data with the specified key.
    if request.method == "GET":
        return render(request, template)

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
        column[0] = column[0].strip()

        _, created = Bhav.objects.update_or_create(
            bhav_ticker=column[0],
            bhav_price=column[6],
            bhav_isin=column[12]
        )
    # context = {}
    # render(request, template, context)
    print('Completed loading new Bhav data')
    return HttpResponseRedirect(reverse("bhav-list"))

# from django.http import HttpResponse
# def index(request):
#    return HttpResponse("Hello, world. You're at the polls index.")
#
