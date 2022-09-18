# Create your views here.

from .models import Umfcent

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


def Umfcent_url():
    return "unused-umfcent-refresh-url"


class UmfcentListView(ListView):
    model = Umfcent

    # if pagination is desired
    # paginate_by = 300
    # filter_backends = [filters.OrderingFilter,]
    # ordering_fields = ['sno', 'nse_symbol']

    def get_queryset(self):
        queryset = Umfcent.objects.all().filter(umfcent_user_id=self.request.user.id)
        return queryset

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UmfcentListView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        refresh_url = Umfcent_url()
        context["refresh_url"] = refresh_url
        return context


class UmfcentListView_AMC_Amount(ListView):
    model = Umfcent

    def get_queryset(self):
        self.queryset = Umfcent.objects.all().filter(umfcent_user_id=self.request.user.id). \
            values('umfcent_amc').annotate(scheme_sum=Sum('umfcent_value')). \
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
            labels_values_dict[q_row['umfcent_amc']] = q_row['scheme_sum']
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
        app_label = 'umfcent'
        template_name_first = app_label + '/' + 'umfcent_aggregate.html'
        template_names_list = [template_name_first]
        return template_names_list


class UmfcentListView_SubcatAmount(ListView):
    model = Umfcent

    def get_queryset(self):
        self.queryset = Umfcent.objects.all().filter(umfcent_user_id=self.request.user.id). \
            values('umfcent_subcat').annotate(scheme_sum=Sum('umfcent_value')). \
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
            labels_values_dict[q_row['umfcent_subcat']] = q_row['scheme_sum']
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
        app_label = 'umfcent'
        template_name_first = app_label + '/' + 'umfcent_aggregate.html'
        template_names_list = [template_name_first]
        return template_names_list


class UmfcentListView_StyleBox(ListView):
    model = Umfcent

    def get_queryset(self):
        queryset = Umfcent.objects.all().filter(umfcent_user_id=self.request.user.id). \
            order_by('umfcent_amc', 'umfcent_category', 'umfcent_subcat', '-umfcent_value')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        refresh_url = Umfcent_url()
        context["refresh_url"] = refresh_url
        return context

    def get_template_names(self):
        app_label = 'umfcent'
        template_name_first = app_label + '/' + 'umfcent_stylebox_list.html'
        template_names_list = [template_name_first]
        return template_names_list


class UmfcentListView_CapBox(ListView):
    model = Umfcent

    def get_queryset(self):
        self.queryset = Umfcent.objects.all().filter(umfcent_user_id=self.request.user.id). \
            order_by('umfcent_amc', 'umfcent_category', 'umfcent_subcat', '-umfcent_value')
        return self.queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        qs_flexi = Umfcent.objects.all().filter(umfcent_user_id=self.request.user.id). \
            filter(umfcent_subcat='F-500'). \
            order_by('umfcent_amc', 'umfcent_value')

        qs_large = Umfcent.objects.all().filter(umfcent_user_id=self.request.user.id). \
            filter(umfcent_subcat='L-100'). \
            order_by('umfcent_amc', 'umfcent_value')

        qs_mid = Umfcent.objects.all().filter(umfcent_user_id=self.request.user.id). \
            filter(umfcent_subcat='M-150'). \
            order_by('umfcent_amc', 'umfcent_value')

        qs_small = Umfcent.objects.all().filter(umfcent_user_id=self.request.user.id). \
            filter(umfcent_subcat='S-250'). \
            order_by('umfcent_amc', 'umfcent_value')

        flexi_list = []
        large_list = []
        mid_list = []
        small_list = []

        flexi_value = 0
        large_value = 0
        mid_value = 0
        small_value = 0

        for q1 in qs_flexi:
            flexi_value += q1.umfcent_value
            flexi_list.append(q1.umfcent_name + '-' + str(q1.umfcent_value))

        for q1 in qs_large:
            large_value += q1.umfcent_value
            large_list.append(q1.umfcent_name + '-' + str(q1.umfcent_value))

        for q1 in qs_mid:
            mid_value += q1.umfcent_value
            mid_list.append(q1.umfcent_name + '-' + str(q1.umfcent_value))

        for q1 in qs_small:
            small_value += q1.umfcent_value
            small_list.append(q1.umfcent_name + '-' + str(q1.umfcent_value))

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

        refresh_url = Umfcent_url()
        context["refresh_url"] = refresh_url

        return context

    def get_template_names(self):
        app_label = 'umfcent'
        template_name_first = app_label + '/' + 'umfcent_capbox_list.html'
        template_names_list = [template_name_first]
        return template_names_list


# one parameter named request
def Umfcent_upload(request):
    # for quick debugging
    #
    # import pdb; pdb.set_trace()
    #
    # breakpoint()

    debug_level = 1

    template = "umfcent/umfcent_list.html"

    list_url_name = "umfcent-list"

    # change column name of data frame
    columns_list = []

    # get rid of top 0 lines
    ignore_top_lines = 0

    data_set = comfun.comm_func_upload(request, template, columns_list, list_url_name, ignore_top_lines)

    # delete existing records
    print('Deleted existing Umfcent data')
    Umfcent.objects.all().filter(umfcent_user_id=request.user.id).delete()

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

    if debug_level:
        print('SURI - begin')
        print(data_set)
        print('SURI - end')

    # list of lines ...
    for line in data_set:

        if debug_level > 2:
            print(' new line ---- ', line)

        if re.search(r'FOLIO NO:', line, re.IGNORECASE):
            match = re.search('FOLIO NO:(.*)', line)
            if match:
                folio_num = match.group(1)
                if debug_level > 1:
                    print('---- folio', folio_num)
        elif re.search(r'Opening Unit Balance:', line, re.IGNORECASE):
            match = re.search(r'Opening Unit Balance:(.*)', line)
            if match:
                unit_opening = match.group(1)
                if debug_level > 1:
                    print('---- unit_opening', unit_opening)
            check_txn = True
            fund_txn_cnt = 0
            last_txn_date = ''
        elif re.search(r'Closing Unit Balance:', line, re.IGNORECASE):
            if debug_level > 1:
                print('--- closing_unit')

            # Closing Unit Balance: 4,581.523 Nav as on 15-SEP-2022: INR 57.3673 Valuation on 16-Sep-2022 : INR 2,62,829.60
            match = re.search(r'Closing Unit Balance:(.*) Nav as on (.*): INR (.*) Valuation on (.*): INR (.*)',
                              line)
            if match:
                unit_closing = match.group(1)
                nav_date = match.group(2)
                nav_value = match.group(3)
                valuation_date = match.group(4)
                fund_value = match.group(5)

                # replace , with nothing
                fund_value = fund_value.replace(',', '')

                if check_txn:
                    check_txn = False
                    print(amc_name, ',', fund_name, ',', fund_value, ',', fund_type, ',', last_txn_date)
                    unique_id += 1

                # strip hyphen to remove content after erestwhile and formerly etc
                # ICICI Prudential Bluechip Fund - Growth (formerly ICICI Prudential Focused Bluechip Equity Fund)
                # Kotak Small Cap Fund - Direct Plan - Growth (Erstwhile Kotak Mid-Cap)
                # Kotak Flexicap Fund - Growth (Regular Plan) (Erstwhile Kotak Standard Multicap Fund - Gr)

                real_fund_name = fund_name.split('-')[0]
                if re.search(r'Flexi', real_fund_name, re.IGNORECASE):
                    fund_subcat = 'F-500'
                elif re.search(r'Large', real_fund_name, re.IGNORECASE) \
                        or re.search(r'Blue.*chip', fund_name, re.IGNORECASE) \
                        or re.search(r'Frontline', fund_name, re.IGNORECASE):
                    if re.search(r'Mid', real_fund_name, re.IGNORECASE):
                        fund_subcat = 'LM-250'
                    else:
                        fund_subcat = 'L-100'
                elif re.search(r'Mid', real_fund_name, re.IGNORECASE):
                    fund_subcat = 'M-150'
                elif re.search(r'Small', real_fund_name, re.IGNORECASE):
                    fund_subcat = 'S-250'
                elif re.search(r'Multi', real_fund_name, re.IGNORECASE):
                    fund_subcat = 'U-Multi'
                elif re.search(r'Value', real_fund_name, re.IGNORECASE):
                    fund_subcat = 'U-Value'
                elif re.search(r'Dividend', real_fund_name, re.IGNORECASE):
                    fund_subcat = 'U-Diviend'
                elif re.search(r'Index', real_fund_name, re.IGNORECASE):
                    fund_subcat = 'U-Index'
                else:
                    fund_subcat = 'U-Unknown'

                _, created = Umfcent.objects.update_or_create(
                    umfcent_id=unique_id,
                    umfcent_user_id=request.user.id,
                    umfcent_amc=amc_name,
                    umfcent_name=fund_name,
                    umfcent_category=fund_type,
                    umfcent_subcat=fund_subcat,
                    umfcent_value=fund_value,
                    umfcent_txn_date=last_txn_date
                )

            # clear fund type
            fund_type = ''
        elif re.search(r'Advisor:', line, re.IGNORECASE):
            if debug_level > 1:
                print(line)

            match = re.search('(.*)\(Advisor:(.*)', line)
            if match:
                fund_name = match.group(1)
                if debug_level > 1:
                    print('--- fund_name ', fund_name)
                if re.search(r'Direct', fund_name, re.IGNORECASE):
                    fund_type = 'Direct-MF'
                else:
                    fund_type = 'Regular-MF'

        elif re.search(r'fund', line, re.IGNORECASE):
            amc_name = line

            if debug_level > 1:
                print('--- amc_name ', amc_name)
        elif check_txn:

            if re.search(r'No Transaction during this statement period', line, re.IGNORECASE):
                pass
            elif re.search(r'Address', line, re.IGNORECASE):
                # Address Updated from KRA Data
                pass
            elif re.search(r'Nominee', line, re.IGNORECASE):
                # Registration of Nominee
                pass
            elif re.search(r'Purchase', line, re.IGNORECASE):
                # 13-DEC-2021 Purchase-BSE - Physical - ARN-0845 24,998.75 125.768 198.77 938.555
                # Purchase Systematic-BSE
                # Purchase-BSE
                fund_txn_cnt += 1
                # get the date
                last_txn_date = line.split()[0]
            else:
                if debug_level > 1:
                    print(line)

        if debug_level > 1:
            print(line)

    # end of for

    lastrefd_update("user-mfcent")

    print('Skipped records', skip_records)
    print('Completed loading new User MFCent data')
    return HttpResponseRedirect(reverse(list_url_name))
