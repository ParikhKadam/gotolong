# Create your views here.

from .models import Udepcas

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

from itertools import zip_longest

import re
import pandas as pd
import csv, io
import openpyxl
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect

from django_gotolong.lastrefd.models import Lastrefd, lastrefd_update

from django_gotolong.comm import comfun

import humanize


def Udepcas_url():
    return "unused-udepcas-refresh-url"


class UdepcasListView(ListView):
    model = Udepcas

    # if pagination is desired
    # paginate_by = 300
    # filter_backends = [filters.OrderingFilter,]
    # ordering_fields = ['sno', 'nse_symbol']

    def get_queryset(self):
        queryset = Udepcas.objects.all().filter(udepcas_user_id=self.request.user.id)
        return queryset

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UdepcasListView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        refresh_url = Udepcas_url()
        context["refresh_url"] = refresh_url
        return context


class UdepcasListView_AMC_Amount(ListView):
    model = Udepcas

    def get_queryset(self):
        self.queryset = Udepcas.objects.all().filter(udepcas_user_id=self.request.user.id). \
            values('udepcas_amc').annotate(scheme_sum=Sum('udepcas_value')). \
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
            labels_values_dict[q_row['udepcas_amc']] = q_row['scheme_sum']
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
        app_label = 'udepcas'
        template_name_first = app_label + '/' + 'udepcas_aggregate.html'
        template_names_list = [template_name_first]
        return template_names_list


class UdepcasListView_SubcatAmount(ListView):
    model = Udepcas

    def get_queryset(self):
        self.queryset = Udepcas.objects.all().filter(udepcas_user_id=self.request.user.id). \
            values('udepcas_subcat').annotate(scheme_sum=Sum('udepcas_value')). \
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
            labels_values_dict[q_row['udepcas_subcat']] = q_row['scheme_sum']
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
        app_label = 'udepcas'
        template_name_first = app_label + '/' + 'udepcas_aggregate.html'
        template_names_list = [template_name_first]
        return template_names_list


class UdepcasListView_StyleBox(ListView):
    model = Udepcas

    def get_queryset(self):
        queryset = Udepcas.objects.all().filter(udepcas_user_id=self.request.user.id). \
            order_by('udepcas_amc', 'udepcas_category', 'udepcas_subcat', '-udepcas_value')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        refresh_url = Udepcas_url()
        context["refresh_url"] = refresh_url
        return context

    def get_template_names(self):
        app_label = 'udepcas'
        template_name_first = app_label + '/' + 'udepcas_stylebox_list.html'
        template_names_list = [template_name_first]
        return template_names_list


class UdepcasListView_CapBox(ListView):
    model = Udepcas

    def get_queryset(self):
        self.queryset = Udepcas.objects.all().filter(udepcas_user_id=self.request.user.id). \
            order_by('udepcas_amc', 'udepcas_category', 'udepcas_subcat', '-udepcas_value')
        return self.queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        qs_flexi = Udepcas.objects.all().filter(udepcas_user_id=self.request.user.id). \
            filter(udepcas_subcat='F-500'). \
            order_by('udepcas_amc', 'udepcas_value')

        qs_large = Udepcas.objects.all().filter(udepcas_user_id=self.request.user.id). \
            filter(udepcas_subcat='L-100'). \
            order_by('udepcas_amc', 'udepcas_value')

        qs_mid = Udepcas.objects.all().filter(udepcas_user_id=self.request.user.id). \
            filter(udepcas_subcat='M-150'). \
            order_by('udepcas_amc', 'udepcas_value')

        qs_small = Udepcas.objects.all().filter(udepcas_user_id=self.request.user.id). \
            filter(udepcas_subcat='S-250'). \
            order_by('udepcas_amc', 'udepcas_value')

        flexi_list = []
        large_list = []
        mid_list = []
        small_list = []

        flexi_value = 0
        large_value = 0
        mid_value = 0
        small_value = 0

        for q1 in qs_flexi:
            flexi_value += q1.udepcas_value
            flexi_list.append(q1.udepcas_name + '-' + str(q1.udepcas_value))

        for q1 in qs_large:
            large_value += q1.udepcas_value
            large_list.append(q1.udepcas_name + '-' + str(q1.udepcas_value))

        for q1 in qs_mid:
            mid_value += q1.udepcas_value
            mid_list.append(q1.udepcas_name + '-' + str(q1.udepcas_value))

        for q1 in qs_small:
            small_value += q1.udepcas_value
            small_list.append(q1.udepcas_name + '-' + str(q1.udepcas_value))

        context["flexi_list"] = flexi_list
        context["large_list"] = large_list
        context["mid_list"] = mid_list
        context["small_list"] = small_list

        all_list = list(zip_longest(flexi_list, large_list, mid_list, small_list, fillvalue='-'))

        print(all_list)

        context["all_list"] = all_list

        context["flexi_value"] = humanize.intword(flexi_value)
        context["large_value"] = humanize.intword(large_value)
        context["mid_value"] = humanize.intword(mid_value)
        context["small_value"] = humanize.intword(small_value)

        total_value = flexi_value + large_value + mid_value + small_value
        context["flexi_value_pct"] = int(flexi_value * 100.0 / total_value)
        context["large_value_pct"] = int(large_value * 100.0 / total_value)
        context["mid_value_pct"] = int(mid_value * 100.0 / total_value)
        context["small_value_pct"] = int(small_value * 100.0 / total_value)

        refresh_url = Udepcas_url()
        context["refresh_url"] = refresh_url

        return context

    def get_template_names(self):
        app_label = 'udepcas'
        template_name_first = app_label + '/' + 'udepcas_capbox_list.html'
        template_names_list = [template_name_first]
        return template_names_list


# one parameter named request
def Udepcas_upload(request):
    # for quick debugging
    #
    # import pdb; pdb.set_trace()
    #
    # breakpoint()

    debug_level = 1

    template = "udepcas/udepcas_list.html"

    list_url_name = "udepcas-list"

    # change column name of data frame
    columns_list = []

    # get rid of top 0 lines
    ignore_top_lines = 0

    data_set = comfun.comm_func_upload(request, template, columns_list, list_url_name, ignore_top_lines)

    # delete existing records
    print('Deleted existing Udepcas data')
    Udepcas.objects.all().filter(udepcas_user_id=request.user.id).delete()

    # note: what about using existing slots... how do we fill holes
    #

    # setup a stream which is when we loop through each line we are able to handle a data in a stream

    check_txn = False
    fund_txn_cnt = 0
    unit_closing = 0
    nav_date = ''
    nav_value = 0
    valuation_date = ''
    fund_value = 0
    last_txn_date = ''
    fund_type = ''
    unique_id = 0

    skip_records = 0

    if debug_level > 1:
        print('SURI - begin')
        print(data_set)
        print('SURI - end')

    parse_begin = False
    line_type = ''

    text_list = data_set
    line_idx = 0

    print('num_lines', len(text_list))
    while line_idx < len(text_list):
        line = text_list[line_idx]

        if debug_level > 2:
            print(' new line ---- ', line)

        if re.search(r'ISIN ISIN ', line, re.IGNORECASE):
            print('--ETF--')
            line_type = 'ETF'
            line_idx += 3
            # ISIN ISIN Description No. of
            # UnitsNAV
            # in `Value
            # in `
        elif re.fullmatch('ISIN', line, re.IGNORECASE):
            if re.search(r'UCCISIN', text_list[line_idx + 1], re.IGNORECASE):
                print('--MF--')
                line_type = 'MF'
                line_idx += 11
                # ISIN
                # UCCISIN Description Folio No. No. of
                # UnitsAverage
                # Cost Per Units
                # `Total Cost
                # `Current NAV
                # per unit
                # in `Current Value
                # in `Unrealised
                # Profit/(Loss)
                # `Annualised
                # Return(%)
            else:
                print('--STOCK--')
                line_type = 'STOCK'
                line_idx += 4
                # ISIN
                # Stock SymbolCompany Name Face Value
                # in `No. of
                # SharesMarket
                # Price in `Value in `
            parse_begin = True
        elif re.search(r'Consolidated Account Statement', line, re.IGNORECASE) or \
                re.search(r'Summary Holdings Transactions Your Account About NSDL', line, re.IGNORECASE):
            line_idx += 1
            continue
        elif re.search(r'Corporate Bonds', line, re.IGNORECASE):
            line_type = ''
        elif re.search(r'Government Securities', line, re.IGNORECASE):
            line_type = ''
        elif re.search(r'Notes:', line, re.IGNORECASE):
            line_type = ''
            parse_begin = False
        elif re.search(r'Transactions for the period from', line, re.IGNORECASE):
            line_type = ''
            parse_begin = False
        elif re.search(r'End of Statement', line, re.IGNORECASE):
            line_type = ''
            parse_begin = False
        else:
            if parse_begin and line_type != '':
                if debug_level > 1:
                    print(line_type, line)
                if line_type == 'STOCK':
                    if debug_level > 1:
                        print('hi')
                    if re.match(r'INE', line):
                        if debug_level > 1:
                            print('hi2')
                        stock_line = ''

                        if re.search(r'(.+)Page (\d)*', text_list[line_idx + 1]):
                            match = re.search(r'(.+)Page (\d)*', text_list[line_idx + 1])
                            stock_line = line + ' ' + match.group(1)
                        elif re.search(r'(.+)Page (\d)*', text_list[line_idx + 2]):
                            match = re.search(r'(.+)Page (\d)*', text_list[line_idx + 2])
                            stock_line = line + ' ' + text_list[line_idx + 1] + ' ' + match.group(1)
                        elif re.match(r'Sub Total', text_list[line_idx + 2]):
                            stock_line = line + ' ' + text_list[line_idx + 1]
                            line_idx += 1
                        elif re.match(r'INE', text_list[line_idx + 2]):
                            stock_line = line + ' ' + text_list[line_idx + 1]
                            line_idx += 1
                        elif re.match(r'INE', text_list[line_idx + 3]):
                            stock_line = line + ' ' + text_list[line_idx + 1] + ' ' + text_list[line_idx + 2]
                            line_idx += 2
                        else:
                            print('-BAD-')

                        if debug_level > 1:
                            print(stock_line)

                        # replace .NSE with with space
                        stock_line = stock_line.replace('.NSE', ' ')
                        stock_line_list = stock_line.split()

                        stock_isin = stock_line_list[0]
                        stock_ticker = stock_line_list[1]
                        stock_qty = stock_line_list[-3]
                        stock_value = stock_line_list[-1]

                        stock_qty = stock_qty.replace(",", "")
                        stock_qty = int(float(stock_qty))
                        stock_value = stock_value.replace(",", "")

                        print(stock_isin, stock_ticker, stock_qty, stock_value)

                        asset_class = "stock"
                        if int(float(stock_value)) != 0:
                            _, created = Udepcas.objects.update_or_create(
                                udepcas_id=unique_id,
                                udepcas_user_id=request.user.id,
                                udepcas_asset_class=asset_class,
                                udepcas_isin=stock_isin,
                                udepcas_symbol=stock_ticker,
                                udepcas_name='-UNK-',
                                udepcas_qty=stock_qty,
                                udepcas_cost=0,
                                udepcas_value=stock_value,
                                udepcas_txn_date=''
                            )
                            unique_id += 1

                elif line_type == 'ETF':
                    if re.search(r"\.\d+$", line):
                        stock_line = line
                    else:
                        stock_line = line + ', ' + text_list[line_idx + 1]
                        line_idx += 1

                    stock_line = stock_line.replace("--", " ")

                    match = re.search(r"(\w+) ([\w\s,\d-]+) ([\d,\.]+) ([\d,\.]+) ([\d,\.]+)$", stock_line)

                    if match:
                        stock_isin = match.group(1)
                        stock_name = match.group(2)
                        stock_qty = match.group(3)
                        stock_value = match.group(5)

                        stock_qty = stock_qty.replace(",", "")
                        stock_value = stock_value.replace(",", "")

                        stock_qty = int(float(stock_qty))

                    if debug_level > 1:
                        print(stock_line)

                    real_stock_line = stock_isin + ', ' + stock_name + ', ' + str(stock_qty) + ', ' + stock_value

                    print(real_stock_line)

                    asset_class = "ETF"
                    if int(float(stock_value)) != 0:
                        _, created = Udepcas.objects.update_or_create(
                            udepcas_id=unique_id,
                            udepcas_user_id=request.user.id,
                            udepcas_asset_class=asset_class,
                            udepcas_isin=stock_isin,
                            udepcas_symbol='-UNK-',
                            udepcas_name=stock_name,
                            udepcas_qty=stock_qty,
                            udepcas_cost=0,
                            udepcas_value=stock_value,
                            udepcas_txn_date=''
                        )
                        unique_id += 1

                elif line_type == 'MF':
                    # MF
                    # combine

                    skip_mf = True

                    if skip_mf:
                        print('skipped MF')
                        break

                    stock_line = line
                    while line_idx < len(text_list):
                        next_line = text_list[line_idx + 1]
                        if re.search(r"Total ", next_line) or re.search(r"Notes:", next_line):
                            print('Exiting from the loop', line_idx)
                            line_type = ''
                            parse_begin = False
                            break
                        elif re.search(r'Consolidated Account Statement', next_line, re.IGNORECASE) or \
                                re.search(r'Summary Holdings Transactions Your Account About NSDL', next_line,
                                          re.IGNORECASE):
                            line_type = ''
                            parse_begin = False
                            break
                        else:
                            stock_line += next_line

                        print(line_idx, next_line)
                        line_idx += 1

                    print('fully parsed..')
                    if debug_level > 1:
                        print(stock_line)

                    print('fully splitted..')
                    stock_line_list = stock_line.split('INF')
                    print(stock_line_list)

                    for rev_line in stock_line_list:
                        rev_list = rev_line.split()
                        if len(rev_list) < 5:
                            continue

                        rev_name = ''
                        for name in rev_list:
                            if re.search(r",", name):
                                break
                            if re.search(r"\.", name):
                                break
                            rev_name += ' ' + name

                        if debug_level > 1:
                            print(rev_list)

                        print(rev_name, rev_list[-5], rev_list[-3])

        if debug_level > 1:
            print(line)

        line_idx += 1

    # end of for

    lastrefd_update("user-udepcas")

    print('Skipped records', skip_records)
    print('Completed loading new User MFCent data')
    return HttpResponseRedirect(reverse(list_url_name))
