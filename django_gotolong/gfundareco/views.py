# Create your views here.

from django.views.generic.list import ListView

from django.http import HttpResponseRedirect
from django.views import View

from django.urls import reverse

from django_gotolong.amfi.models import Amfi
from django_gotolong.indices.models import Indices
from django_gotolong.fratio.models import Fratio
from django_gotolong.trendlyne.models import Trendlyne
from django_gotolong.gcweight.models import Gcweight
from django_gotolong.gfundareco.models import Gfundareco

from django_gotolong.lastrefd.models import Lastrefd, lastrefd_update

from django.db.models import OuterRef, Subquery, ExpressionWrapper, F, IntegerField, Count


class GfundarecoListView(ListView):
    model = Gfundareco
    # if pagination is desired
    # paginate_by = 300
    # filter_backends = [filters.OrderingFilter,]
    # ordering_fields = ['sno', 'nse_symbol']
    queryset = Gfundareco.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        funda_reco_list = (
            Gfundareco.objects.all().values('funda_reco_type').annotate(funda_reco_count=Count('funda_reco_type')).
            order_by('funda_reco_count'))

        context["funda_reco_list"] = funda_reco_list
        return context


class GfundarecoListView2(ListView):
    # model = Gfundareco
    # if pagination is desired
    # paginate_by = 300
    # filter_backends = [filters.OrderingFilter,]
    # ordering_fields = ['sno', 'nse_symbol']
    tl_qs = Trendlyne.objects.filter(tl_nse=OuterRef("nse_symbol"))
    gcweight_qs = Gcweight.objects.filter(gcw_cap_type=OuterRef("cap_type"))
    gfunda_reco_qs = Gfundareco.objects.filter(funda_reco_isin=OuterRef("comp_isin"))
    queryset = Amfi.objects.all(). \
        annotate(bat=Subquery(tl_qs.values('tl_bat')[:1])). \
        annotate(funda_reco_type=Subquery(gfunda_reco_qs.values('funda_reco_type')[:1])). \
        annotate(funda_reco_cause=Subquery(gfunda_reco_qs.values('funda_reco_cause')[:1])). \
        filter(bat__isnull=False). \
        values('nse_symbol', 'comp_name', 'bat', 'funda_reco_type', 'funda_reco_cause')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_template_names(self):
        app_label = 'gfundareco'
        template_name_first = app_label + '/' + 'gfunda_reco_list.html'
        template_names_list = [template_name_first]
        return template_names_list


class GfundarecoRefreshView(View):
    fr_buy = {}
    fr_hold = {}
    fr_enabled = {}
    ticker_industry_dict = {}
    debug_level = 1

    def get(self, request):
        self.gfunda_reco_refresh(request)
        return HttpResponseRedirect(reverse("gfundareco-list"))

    def __init__(self):
        super(GfundarecoRefreshView, self).__init__()

    def gfunda_reco_get_reco(self, stock_name, ticker, isin, bat, der, roce3,
                             roe3, dpr2, sales2, profit5, icr,
                             pledge, low_3y, low_5y, notes):

        bat = round(bat, 2)
        der = round(der, 2)
        roce3 = round(roce3, 2)
        roe3 = round(roe3, 2)

        dpr2 = round(dpr2, 2)
        sales2 = round(sales2, 2)
        profit5 = round(profit5, 2)
        pledge = round(pledge, 2)

        ignore_der = False
        # skip debt for Financial Services like Bank/NBFC.
        if ticker in self.ticker_industry_dict:
            if self.debug_level > 1:
                print('tl', 'isin', ticker, 'industry', self.ticker_industry_dict[ticker])
            if self.ticker_industry_dict[ticker] == 'FINANCIAL SERVICES':
                ignore_der = True
        else:
            print(ticker, isin, 'not found in ticker industry db')

        funda_reco_type = 'NONE'
        funda_reco_cause = ''

        if ignore_der:
            s_c1 = True
        else:
            s_c1 = der <= self.fr_buy['der']

        s_c2 = roce3 >= self.fr_buy['roce3']
        s_c3 = dpr2 >= self.fr_buy['dpr2']
        s_c4 = sales2 >= self.fr_buy['sales2']
        s_c5 = profit5 >= self.fr_buy['profit5']
        s_c6 = pledge <= self.fr_buy['pledge']

        # if isin == 'INE079A01024':
        #    breakpoint()

        if not s_c1:
            funda_reco_cause += " "
            funda_reco_cause = "-S(der)"
        if not s_c2:
            funda_reco_cause += " "
            funda_reco_cause = "-S(roce3)"
        if not s_c3:
            funda_reco_cause += " "
            funda_reco_cause = "-S(dpr2)"
        if not s_c4:
            funda_reco_cause += " "
            funda_reco_cause = "-S(sales)"
        if not s_c5:
            funda_reco_cause += " "
            funda_reco_cause = "-S(profit5)"
        if not s_c6:
            funda_reco_cause += " "
            funda_reco_cause = "-S(pledge)"

        if (s_c1 and s_c2 and s_c3 and s_c4 and s_c5 and s_c6):
            funda_reco_type = "Strong"
            funda_reco_cause = "ALL"
            return (funda_reco_type, funda_reco_cause)
        else:
            w_c1 = der > self.fr_hold['der']
            w_c2 = roce3 < self.fr_hold['roce3']
            w_c3 = dpr2 < self.fr_hold['dpr2']
            w_c4 = sales2 < self.fr_hold['sales2']
            w_c5 = profit5 < self.fr_hold['profit5']
            w_c6 = pledge > self.fr_hold['pledge']
            # avoid NONE
            funda_reco_cause_buy = funda_reco_cause
            funda_reco_cause = ''

            if w_c1:
                if not ignore_der:
                    funda_reco_cause += " "
                    funda_reco_cause += "W(der/" + str(der) + ")"
            if w_c2:
                funda_reco_cause += " "
                funda_reco_cause += "W(roce3/" + str(roce3) + ")"
            if w_c3:
                funda_reco_cause += " "
                funda_reco_cause += "W(dpr2/" + str(dpr2) + ")"
            if w_c4:
                funda_reco_cause += " "
                funda_reco_cause += "W(sales2/" + str(sales2) + ")"
            if w_c5:
                funda_reco_cause += " "
                funda_reco_cause += "W(profit5/" + str(profit5) + ")"
            if w_c6:
                funda_reco_cause += " "
                funda_reco_cause += "W(pledge/" + str(pledge) + ")"

            if funda_reco_cause == '':
                funda_reco_type = "Moderate"
            else:
                funda_reco_type = "Weak"

        if funda_reco_type == 'Moderate':
            m_c1 = (der > self.fr_buy['der'] and der <= self.fr_hold['der'])
            # fixed the bug here to get the cause for HOLD
            m_c2 = (roce3 < self.fr_buy['roce3'] and roce3 >= self.fr_hold['roce3'])
            m_c3 = (dpr2 < self.fr_buy['dpr2'] and dpr2 >= self.fr_hold['dpr2'])
            m_c4 = (sales2 < self.fr_buy['sales2'] and sales2 >= self.fr_hold['sales2'])
            m_c5 = (profit5 < self.fr_buy['profit5'] and profit5 >= self.fr_hold['profit5'])
            m_c6 = (pledge > self.fr_buy['pledge'] and pledge <= self.fr_hold['pledge'])

            if m_c1:
                if not ignore_der:
                    funda_reco_cause += " "
                    funda_reco_cause += "M(der/" + str(der) + ")"
            if m_c2:
                funda_reco_cause += " "
                funda_reco_cause += "M(roce3/" + str(roce3) + ")"
            if m_c3:
                funda_reco_cause += " "
                funda_reco_cause += "M(dpr2/" + str(dpr2) + ")"
            if m_c4:
                funda_reco_cause += " "
                funda_reco_cause += "M(sales2/" + str(sales2) + ")"
            if m_c5:
                funda_reco_cause += " "
                funda_reco_cause += "M(profit5/" + str(profit5) + ")"
            if m_c6:
                funda_reco_cause += " "
                funda_reco_cause += "M(pledge/" + str(pledge) + ")"

            # for debugging
            if funda_reco_cause == '':
                funda_reco_cause = funda_reco_cause_buy

        return (funda_reco_type, funda_reco_cause)

    def gfunda_reco_refresh(self, request):
        debug_level = 1
        # declaring template
        template = "gfundareco/gfunda_reco_list.html"

        for fr in Fratio.objects.all():
            print(fr.fratio_name, fr.fratio_buy, fr.fratio_hold, fr.fratio_enabled)
            self.fr_buy[fr.fratio_name] = fr.fratio_buy
            self.fr_hold[fr.fratio_name] = fr.fratio_hold
            self.fr_enabled[fr.fratio_name] = fr.fratio_enabled

        for ind in Indices.objects.all():
            # strip unwanted new line
            ind.ind_ticker = ind.ind_ticker.rstrip()
            if debug_level > 1:
                print(ind.ind_ticker, ind.ind_industry)
            self.ticker_industry_dict[ind.ind_ticker] = ind.ind_industry

        # breakpoint()

        # import pdb
        # pdb.set_trace()

        # first delete all existing gfundareco objects
        Gfundareco.objects.all().delete()

        for tl in Trendlyne.objects.all():

            # print(tl.stock_name, tl.isin)

            # using 0 for roe3
            # using notes itself as notes
            (funda_reco_type, funda_reco_cause) = \
                self.gfunda_reco_get_reco(tl.tl_stock_name, tl.tl_nse, tl.tl_isin, tl.tl_bat, tl.tl_der, tl.tl_roce3,
                                          tl.tl_roe3, tl.tl_dpr2, tl.tl_sales2, tl.tl_profit5, tl.tl_icr,
                                          tl.tl_pledge, tl.tl_low_3y, tl.tl_low_5y, "notes")

            if debug_level > 1:
                print(tl.tl_stock_name, tl.tl_nse, tl.tl_isin, funda_reco_type, funda_reco_cause)

            # isin_obj = Indices.objects.get(comp_isin=tl.isin)
            # print(isin_obj.comp_ticker)

            # to avoid DoesNotExist exception
            first_name = tl.tl_stock_name.split(' ', 1)[0]
            # use upper case
            first_name = first_name.upper()
            # no longer using isin to name lookup

            '''
            # amfi_obj = Amfi.objects.filter(comp_isin=tl.tl_isin).first()
            # amfi_obj = Amfi.objects.filter(nse_symbol=tl.tl_nse).first()

            # try lookup using name if isin has changed
            # if not amfi_obj:
                # print('amfi obj failed for isin', tl.tl_isin, 'stock_name', tl.tl_stock_name)
                print('amfi obj failed for nse ticker', tl.tl_nse, 'stock_name', tl.tl_stock_name)
                amfi_obj = Amfi.objects.filter(comp_name__contains=first_name).first()

            if amfi_obj:
                if debug_level > 1:
                    print(amfi_obj.nse_symbol)
                if tl.tl_isin == 'INE745G01035':
                    print('nse symbol', amfi_obj.nse_symbol)
                if amfi_obj.nse_symbol != '':
                    # earlier code ....
            else:
                print('amfi obj failed for stock_name', tl.tl_stock_name, 'first name', first_name)
            '''

            if tl.tl_nse != '':
                _, created = Gfundareco.objects.update_or_create(
                    funda_reco_ticker=tl.tl_nse,
                    funda_reco_isin=tl.tl_isin,
                    funda_reco_type=funda_reco_type,
                    funda_reco_cause=funda_reco_cause
                )
            else:
                print('nse failed for stock_name', tl.tl_stock_name, 'first name', first_name)

        # Updated Gfundareco objects
        lastrefd_update("gfundareco")
