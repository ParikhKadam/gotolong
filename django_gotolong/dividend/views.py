# Create your views here.

from django.views.generic.list import ListView

from django.http import HttpResponseRedirect
from django.views import View

import pandas as pd
import io
import csv

from django.urls import reverse

from django_gotolong.amfi.models import Amfi
from django_gotolong.bstmtdiv.models import BstmtDiv
from django_gotolong.indices.models import Indices
from django_gotolong.fratio.models import Fratio
from django_gotolong.trendlyne.models import Trendlyne
from django_gotolong.gcweight.models import Gcweight
from django_gotolong.dividend.models import Dividend

from django_gotolong.lastrefd.models import Lastrefd, lastrefd_update

from django.db.models import OuterRef, Subquery, ExpressionWrapper, F, IntegerField, Count
from django.db.models import (Sum, Count)
from django.db.models.functions import (Round)

import fuzzymatcher

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class DividendListView(ListView):
    model = Dividend

    # if pagination is desired
    # paginate_by = 300
    # filter_backends = [filters.OrderingFilter,]
    # ordering_fields = ['sno', 'nse_symbol']

    def get_queryset(self):
        return Dividend.objects.all().filter(divi_user_id=self.request.user.id)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(DividendListView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class DividendTickerListView(ListView):
    model = Dividend

    # if pagination is desired
    # paginate_by = 300
    # filter_backends = [filters.OrderingFilter,]
    # ordering_fields = ['sno', 'nse_symbol']

    def get_queryset(self):
        return Dividend.objects.all().filter(divi_user_id=self.request.user.id). \
            values('divi_ticker').annotate(Total=Round(Sum('divi_amount'))).order_by('-Total')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(DividendTickerListView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class DividendRefreshView(View):
    fr_buy = {}
    fr_hold = {}
    fr_enabled = {}
    isin_industry_dict = {}
    debug_level = 1

    def get(self, request):
        self.dividend_refresh(request)
        return HttpResponseRedirect(reverse("dividend-list"))

    def __init__(self):
        super(DividendRefreshView, self).__init__()

    def dividend_refresh(self, request):
        debug_level = 1
        # declaring template
        template = "dividend/dividend_list.html"

        df_bstmtdiv = pd.DataFrame.from_records(BstmtDiv.objects.all().
                                                filter(bsdiv_user_id=self.request.user.id).values())
        df_amfi = pd.DataFrame.from_records(Amfi.objects.all().values())

        left_on = ["bsdiv_remarks", ]
        right_on = ["comp_name", "nse_symbol"]

        # get the header
        bstmtdiv_top = df_bstmtdiv.head()
        print('df_bstmtdiv: columns')
        print(bstmtdiv_top)

        # Most of these were matching to CANFINHOMES due to FIN in it

        df_bstmtdiv['bsdiv_remarks'].replace(to_replace='FINDIV', value='DIV', inplace=True, regex=True)
        df_bstmtdiv['bsdiv_remarks'].replace(to_replace='FIN DIV', value='DIV', inplace=True, regex=True)
        df_bstmtdiv['bsdiv_remarks'].replace(to_replace='FINALDIV', value='DIV', inplace=True, regex=True)
        df_bstmtdiv['bsdiv_remarks'].replace(to_replace='FINAL DIV', value='DIV', inplace=True, regex=True)

        # most of these were matching with M&M for mahindra and mahindra ltd
        df_bstmtdiv['bsdiv_remarks'].replace(to_replace='LTD', value='', inplace=True, regex=True)
        df_bstmtdiv['bsdiv_remarks'].replace(to_replace='Ltd', value='', inplace=True, regex=True)
        df_bstmtdiv['bsdiv_remarks'].replace(to_replace='LIMITED', value='', inplace=True, regex=True)
        df_bstmtdiv['bsdiv_remarks'].replace(to_replace='Limited', value='', inplace=True, regex=True)

        matched_results = fuzzymatcher.fuzzy_left_join(df_bstmtdiv,
                                                       df_amfi,
                                                       left_on,
                                                       right_on,
                                                       left_id_col='bsdiv_id',
                                                       right_id_col='comp_rank')

        # drop NaN
        matched_results.dropna(inplace=True)
        print("matched_results")
        print(matched_results)

        cols = [
            "bsdiv_id", "bsdiv_user_id", "bsdiv_date", "bsdiv_remarks", "comp_name", "nse_symbol", "bsdiv_amount",
            "best_match_score"
        ]

        df = matched_results[cols].sort_values(by=['best_match_score'], ascending=False)

        # drop NaN entries
        df.dropna(inplace=True)
        print("df")
        print(df)

        # breakpoint()

        # import pdb
        # pdb.set_trace()

        # first delete all existing dividend objects
        Dividend.objects.all().filter(divi_user_id=self.request.user.id).delete()

        data_set = df.to_csv(header=False, index=False)

        io_string = io.StringIO(data_set)
        next(io_string)
        print('first record', io_string)
        skipped_records = 0
        for column in csv.reader(io_string, delimiter=',', quotechar='"'):

            if debug_level > 1:
                print(column)

            divi_id = column[0].strip()
            divi_user_id = column[1].strip()
            divi_date = column[2].strip()
            divi_remarks = column[3].strip()
            divi_company = column[4].strip()
            divi_ticker = column[5].strip()
            divi_amount = column[6].strip()
            divi_score = column[7].strip()

            try:
                _, created = Dividend.objects.update_or_create(
                    divi_id=divi_id,
                    divi_user_id=divi_user_id,
                    divi_date=divi_date,
                    divi_remarks=divi_remarks,
                    divi_company=divi_company,
                    divi_ticker=divi_ticker,
                    divi_amount=divi_amount,
                    divi_score=divi_score,
                )
            except Exception as e:
                print('Exception ')
                print(e)

        # Updated Dividend objects
        lastrefd_update("dividend")
