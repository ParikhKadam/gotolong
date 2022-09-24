# Create your views here.

from django.views.generic.list import ListView

from django_gotolong.amfi.models import Amfi

from django_gotolong.bhav.models import Bhav

from django_gotolong.indices.models import Indices

from django_gotolong.corpact.models import Corpact

from django_gotolong.dematsum.models import DematSum
from django_gotolong.demattxn.models import DematTxn

from django_gotolong.ftwhl.models import Ftwhl

from django_gotolong.gfundareco.models import Gfundareco
from django_gotolong.gcweight.models import Gcweight

from django_gotolong.trendlyne.models import Trendlyne

from django.db.models import (OuterRef, Subquery, ExpressionWrapper)
from django.db.models import (F, IntegerField, Count, Q)
from django.db.models import Case, Value, When, CharField

from django_gotolong.jsched.tasks import jsched_task_bg, jsched_task_daily
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


# from django_gotolong.ftwhl.views import ftwhl_fetch

class AdvisorListView_AllButNone(ListView):
    # crete task
    # jsched_task_bg(schedule=timezone.now())
    # jsched_task_daily()

    # model = Advisor
    # if pagination is desired
    # paginate_by = 300
    # filter_backends = [filters.OrderingFilter,]
    # ordering_fields = ['sno', 'nse_symbol']
    def get_queryset(self):
        indices_qs = Indices.objects.filter(ind_isin=OuterRef("comp_isin"))
        bhav_qs = Bhav.objects.filter(bhav_isin=OuterRef("comp_isin"))
        ca_qs = Corpact.objects.filter(ca_ticker=OuterRef("nse_symbol"))
        ftwhl_qs = Ftwhl.objects.filter(ftwhl_ticker=OuterRef("nse_symbol"))
        gfunda_reco_qs = Gfundareco.objects.filter(funda_reco_isin=OuterRef("comp_isin"))
        tl_qs = Trendlyne.objects.filter(tl_nse=OuterRef("nse_symbol"))
        dematsum_qs = DematSum.objects.filter(ds_user_id=self.request.user.id).filter(ds_isin=OuterRef("comp_isin"))
        demattxn_qs = DematTxn.objects.filter(dt_user_id=self.request.user.id).filter(
            dt_isin=OuterRef("comp_isin")).order_by('-dt_date').values('dt_date')
        gcweight_qs = Gcweight.objects.filter(gcw_cap_type=OuterRef("cap_type"))
        queryset = Amfi.objects.all(). \
            annotate(
            cur_oku=ExpressionWrapper(Subquery(dematsum_qs.values('ds_mktvalue')[:1]) / 1000,
                                      output_field=IntegerField())). \
            annotate(plan_oku=Subquery(gcweight_qs.values('gcw_cap_weight')[:1])). \
            annotate(tbd_oku=ExpressionWrapper(F('plan_oku') - F('cur_oku'), output_field=IntegerField())). \
            annotate(bat=Subquery(tl_qs.values('tl_bat')[:1])). \
            annotate(ca_total=Subquery(ca_qs.values('ca_total')[:1])). \
            annotate(funda_reco_type=Subquery(gfunda_reco_qs.values('funda_reco_type')[:1])). \
            annotate(funda_reco_cause=Subquery(gfunda_reco_qs.values('funda_reco_cause')[:1])). \
            annotate(dt_date=Subquery(demattxn_qs.values('dt_date')[:1])). \
            annotate(bhav_price=Subquery(bhav_qs.values('bhav_price')[:1])). \
            annotate(ftwhl_low=Subquery(ftwhl_qs.values('ftwhl_low')[:1])). \
            annotate(safety_margin=ExpressionWrapper((F('bat') - F('bhav_price')) * 100.0 / F('bhav_price'),
                                                     output_field=IntegerField())). \
            annotate(valuation_reco=Case( \
            When(safety_margin__gt=10, then=Value('Upside')), \
            When(safety_margin__lt=-10, then=Value('Downside')), \
            default=Value('Neutral'), \
            output_field=CharField() \
            )). \
            annotate(low_margin=ExpressionWrapper((F('bhav_price') - F('ftwhl_low')) * 100.0 / F('ftwhl_low'),
                                                  output_field=IntegerField())). \
            annotate(industry=Subquery(indices_qs.values('ind_industry')[:1])). \
            filter(Q(bhav_price__isnull=False)
                   & Q(bat__isnull=False) & Q(ftwhl_low__isnull=False)). \
            values('nse_symbol', 'comp_name', 'bhav_price', 'bat', 'ftwhl_low',
                   'valuation_reco', 'safety_margin', 'low_margin', 'ca_total',
                   'dt_date', 'plan_oku',
                   'cur_oku', 'tbd_oku', 'funda_reco_type', 'funda_reco_cause',
                   'industry', 'cap_type'). \
            order_by('low_margin')
        return queryset

    # @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AdvisorListView_AllButNone, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        funda_reco_list = (
            Gfundareco.objects.all().values('funda_reco_type').annotate(funda_reco_count=Count('funda_reco_type')).
                order_by('funda_reco_count'))

        context["funda_reco_list"] = funda_reco_list

        return context

    def get_template_names(self):
        app_label = 'advisor'
        template_name_first = app_label + '/' + 'advisor_list.html'
        template_names_list = [template_name_first]
        return template_names_list


class AdvisorListView_All(ListView):
    # crete task
    # jsched_task_bg(schedule=timezone.now())
    # jsched_task_daily()

    # model = Advisor
    # if pagination is desired
    # paginate_by = 300
    # filter_backends = [filters.OrderingFilter,]
    # ordering_fields = ['sno', 'nse_symbol']
    def get_queryset(self):
        indices_qs = Indices.objects.filter(ind_isin=OuterRef("comp_isin"))
        bhav_qs = Bhav.objects.filter(bhav_isin=OuterRef("comp_isin"))
        ca_qs = Corpact.objects.filter(ca_ticker=OuterRef("nse_symbol"))
        ftwhl_qs = Ftwhl.objects.filter(ftwhl_ticker=OuterRef("nse_symbol"))
        gfunda_reco_qs = Gfundareco.objects.filter(funda_reco_isin=OuterRef("comp_isin"))
        tl_qs = Trendlyne.objects.filter(tl_nse=OuterRef("nse_symbol"))
        dematsum_qs = DematSum.objects.filter(ds_user_id=self.request.user.id).filter(ds_isin=OuterRef("comp_isin"))
        demattxn_qs = DematTxn.objects.filter(dt_user_id=self.request.user.id).filter(
            dt_isin=OuterRef("comp_isin")).order_by('-dt_date').values('dt_date')
        gcweight_qs = Gcweight.objects.filter(gcw_cap_type=OuterRef("cap_type"))
        queryset = Amfi.objects.all(). \
            annotate(
            cur_oku=ExpressionWrapper(Subquery(dematsum_qs.values('ds_mktvalue')[:1]) / 1000,
                                      output_field=IntegerField())). \
            annotate(plan_oku=Subquery(gcweight_qs.values('gcw_cap_weight')[:1])). \
            annotate(tbd_oku=ExpressionWrapper(F('plan_oku') - F('cur_oku'), output_field=IntegerField())). \
            annotate(bat=Subquery(tl_qs.values('tl_bat')[:1])). \
            annotate(ca_total=Subquery(ca_qs.values('ca_total')[:1])). \
            annotate(funda_reco_type=Subquery(gfunda_reco_qs.values('funda_reco_type')[:1])). \
            annotate(funda_reco_cause=Subquery(gfunda_reco_qs.values('funda_reco_cause')[:1])). \
            annotate(dt_date=Subquery(demattxn_qs.values('dt_date')[:1])). \
            annotate(bhav_price=Subquery(bhav_qs.values('bhav_price')[:1])). \
            annotate(ftwhl_low=Subquery(ftwhl_qs.values('ftwhl_low')[:1])). \
            annotate(safety_margin=ExpressionWrapper((F('bat') - F('bhav_price')) * 100.0 / F('bhav_price'),
                                                     output_field=IntegerField())). \
            annotate(valuation_reco=Case( \
            When(safety_margin__gt=10, then=Value('Upside')), \
            When(safety_margin__lt=-10, then=Value('Downside')), \
            default=Value('Neutral'), \
            output_field=CharField() \
            )). \
            annotate(low_margin=ExpressionWrapper((F('bhav_price') - F('ftwhl_low')) * 100.0 / F('ftwhl_low'),
                                                  output_field=IntegerField())). \
            annotate(industry=Subquery(indices_qs.values('ind_industry')[:1])). \
            values('nse_symbol', 'comp_name', 'bhav_price', 'bat', 'ftwhl_low',
                   'valuation_reco', 'safety_margin', 'low_margin', 'ca_total',
                   'dt_date', 'plan_oku',
                   'cur_oku', 'tbd_oku', 'funda_reco_type', 'funda_reco_cause',
                   'industry', 'cap_type'). \
            order_by('low_margin')
        return queryset

    # @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AdvisorListView_All, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        funda_reco_list = (
            Gfundareco.objects.all().values('funda_reco_type').annotate(funda_reco_count=Count('funda_reco_type')).
                order_by('funda_reco_count'))

        context["funda_reco_list"] = funda_reco_list

        return context

    def get_template_names(self):
        app_label = 'advisor'
        template_name_first = app_label + '/' + 'advisor_list.html'
        template_names_list = [template_name_first]
        return template_names_list


# Insufficient data
class AdvisorListView_Insuf(ListView):
    # crete task
    # jsched_task_bg(schedule=timezone.now())
    # jsched_task_daily()

    # model = Advisor
    # if pagination is desired
    # paginate_by = 300
    # filter_backends = [filters.OrderingFilter,]
    # ordering_fields = ['sno', 'nse_symbol']
    def get_queryset(self):
        indices_qs = Indices.objects.filter(ind_isin=OuterRef("comp_isin"))
        bhav_qs = Bhav.objects.filter(bhav_isin=OuterRef("comp_isin"))
        ca_qs = Corpact.objects.filter(ca_ticker=OuterRef("nse_symbol"))
        ftwhl_qs = Ftwhl.objects.filter(ftwhl_ticker=OuterRef("nse_symbol"))
        gfunda_reco_qs = Gfundareco.objects.filter(funda_reco_isin=OuterRef("comp_isin"))
        tl_qs = Trendlyne.objects.filter(tl_nse=OuterRef("nse_symbol"))
        dematsum_qs = DematSum.objects.filter(ds_user_id=self.request.user.id).filter(ds_isin=OuterRef("comp_isin"))
        demattxn_qs = DematTxn.objects.filter(dt_user_id=self.request.user.id).filter(
            dt_isin=OuterRef("comp_isin")).order_by('-dt_date').values('dt_date')
        gcweight_qs = Gcweight.objects.filter(gcw_cap_type=OuterRef("cap_type"))
        queryset = Amfi.objects.all(). \
            annotate(
            cur_oku=ExpressionWrapper(Subquery(dematsum_qs.values('ds_mktvalue')[:1]) / 1000,
                                      output_field=IntegerField())). \
            annotate(plan_oku=Subquery(gcweight_qs.values('gcw_cap_weight')[:1])). \
            annotate(tbd_oku=ExpressionWrapper(F('plan_oku') - F('cur_oku'), output_field=IntegerField())). \
            annotate(bat=Subquery(tl_qs.values('tl_bat')[:1])). \
            annotate(ca_total=Subquery(ca_qs.values('ca_total')[:1])). \
            annotate(funda_reco_type=Subquery(gfunda_reco_qs.values('funda_reco_type')[:1])). \
            annotate(funda_reco_cause=Subquery(gfunda_reco_qs.values('funda_reco_cause')[:1])). \
            annotate(dt_date=Subquery(demattxn_qs.values('dt_date')[:1])). \
            annotate(bhav_price=Subquery(bhav_qs.values('bhav_price')[:1])). \
            annotate(ftwhl_low=Subquery(ftwhl_qs.values('ftwhl_low')[:1])). \
            annotate(safety_margin=ExpressionWrapper((F('bat') - F('bhav_price')) * 100.0 / F('bhav_price'),
                                                     output_field=IntegerField())). \
            annotate(valuation_reco=Case( \
            When(safety_margin__gt=10, then=Value('Upside')), \
            When(safety_margin__lt=-10, then=Value('Downside')), \
            default=Value('Neutral'), \
            output_field=CharField() \
            )). \
            annotate(low_margin=ExpressionWrapper((F('bhav_price') - F('ftwhl_low')) * 100.0 / F('ftwhl_low'),
                                                  output_field=IntegerField())). \
            annotate(industry=Subquery(indices_qs.values('ind_industry')[:1])). \
            filter(Q(bhav_price__isnull=True) | Q(bat__isnull=True) | Q(ftwhl_low__isnull=True)). \
            values('nse_symbol', 'comp_name', 'bhav_price', 'bat', 'ftwhl_low',
                   'valuation_reco', 'safety_margin', 'low_margin', 'ca_total',
                   'dt_date', 'plan_oku',
                   'cur_oku', 'tbd_oku', 'funda_reco_type', 'funda_reco_cause',
                   'industry', 'cap_type'). \
            order_by('low_margin')
        return queryset

    # @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AdvisorListView_Insuf, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        funda_reco_list = (
            Gfundareco.objects.all().values('funda_reco_type').annotate(funda_reco_count=Count('funda_reco_type')).
                order_by('funda_reco_count'))

        context["funda_reco_list"] = funda_reco_list

        return context

    def get_template_names(self):
        app_label = 'advisor'
        template_name_first = app_label + '/' + 'advisor_list.html'
        template_names_list = [template_name_first]
        return template_names_list


class AdvisorListView_Strong(ListView):
    # model = Advisor
    # if pagination is desired
    # paginate_by = 300
    # filter_backends = [filters.OrderingFilter,]
    # ordering_fields = ['sno', 'nse_symbol']
    indices_qs = Indices.objects.filter(ind_isin=OuterRef("comp_isin"))
    bhav_qs = Bhav.objects.filter(bhav_isin=OuterRef("comp_isin"))
    ca_qs = Corpact.objects.filter(ca_ticker=OuterRef("nse_symbol"))
    ftwhl_qs = Ftwhl.objects.filter(ftwhl_ticker=OuterRef("nse_symbol"))
    gfunda_reco_qs = Gfundareco.objects.filter(funda_reco_isin=OuterRef("comp_isin"))
    tl_qs = Trendlyne.objects.filter(tl_nse=OuterRef("nse_symbol"))
    dematsum_qs = DematSum.objects.filter(ds_isin=OuterRef("comp_isin"))
    demattxn_qs = DematTxn.objects.filter(dt_isin=OuterRef("comp_isin")).order_by('-dt_date').values('dt_date')
    gcweight_qs = Gcweight.objects.filter(gcw_cap_type=OuterRef("cap_type"))
    queryset = Amfi.objects.all(). \
        annotate(
        cur_oku=ExpressionWrapper(Subquery(dematsum_qs.values('ds_mktvalue')[:1]) / 1000,
                                  output_field=IntegerField())). \
        annotate(plan_oku=Subquery(gcweight_qs.values('gcw_cap_weight')[:1])). \
        annotate(tbd_oku=ExpressionWrapper(F('plan_oku') - F('cur_oku'), output_field=IntegerField())). \
        annotate(bat=Subquery(tl_qs.values('tl_bat')[:1])). \
        annotate(ca_total=Subquery(ca_qs.values('ca_total')[:1])). \
        annotate(funda_reco_type=Subquery(gfunda_reco_qs.values('funda_reco_type')[:1])). \
        annotate(funda_reco_cause=Subquery(gfunda_reco_qs.values('funda_reco_cause')[:1])). \
        annotate(dt_date=Subquery(demattxn_qs.values('dt_date')[:1])). \
        annotate(bhav_price=Subquery(bhav_qs.values('bhav_price')[:1])). \
        annotate(ftwhl_low=Subquery(ftwhl_qs.values('ftwhl_low')[:1])). \
        annotate(safety_margin=ExpressionWrapper((F('bat') - F('bhav_price')) * 100.0 / F('bhav_price'),
                                                 output_field=IntegerField())). \
        annotate(valuation_reco=Case( \
        When(safety_margin__gt=10, then=Value('Upside')), \
        When(safety_margin__lt=-10, then=Value('Downside')), \
        default=Value('Neutral'), \
        output_field=CharField() \
        )). \
        annotate(low_margin=ExpressionWrapper((F('bhav_price') - F('ftwhl_low')) * 100.0 / F('ftwhl_low'),
                                              output_field=IntegerField())). \
        annotate(industry=Subquery(indices_qs.values('ind_industry')[:1])). \
        filter(Q(bhav_price__isnull=False) & Q(bat__isnull=False)). \
        filter(funda_reco_type='Strong'). \
        values('nse_symbol', 'comp_name', 'bhav_price', 'bat', 'ftwhl_low',
               'valuation_reco', 'safety_margin', 'low_margin', 'ca_total',
               'dt_date', 'plan_oku',
               'cur_oku', 'tbd_oku', 'funda_reco_type', 'funda_reco_cause',
               'industry', 'cap_type'). \
        order_by('low_margin')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        funda_reco_list = (
            Gfundareco.objects.all().values('funda_reco_type').annotate(funda_reco_count=Count('funda_reco_type')).
                order_by('funda_reco_count'))

        context["funda_reco_list"] = funda_reco_list

        return context

    def get_template_names(self):
        app_label = 'advisor'
        template_name_first = app_label + '/' + 'advisor_list.html'
        template_names_list = [template_name_first]
        return template_names_list


class AdvisorListView_Weak(ListView):
    # model = Advisor
    # if pagination is desired
    # paginate_by = 300
    # filter_backends = [filters.OrderingFilter,]
    # ordering_fields = ['sno', 'nse_symbol']
    indices_qs = Indices.objects.filter(ind_isin=OuterRef("comp_isin"))
    bhav_qs = Bhav.objects.filter(bhav_isin=OuterRef("comp_isin"))
    ca_qs = Corpact.objects.filter(ca_ticker=OuterRef("nse_symbol"))
    ftwhl_qs = Ftwhl.objects.filter(ftwhl_ticker=OuterRef("nse_symbol"))
    gfunda_reco_qs = Gfundareco.objects.filter(funda_reco_isin=OuterRef("comp_isin"))
    tl_qs = Trendlyne.objects.filter(tl_nse=OuterRef("nse_symbol"))
    dematsum_qs = DematSum.objects.filter(ds_isin=OuterRef("comp_isin"))
    demattxn_qs = DematTxn.objects.filter(dt_isin=OuterRef("comp_isin")).order_by('-dt_date').values('dt_date')
    gcweight_qs = Gcweight.objects.filter(gcw_cap_type=OuterRef("cap_type"))
    queryset = Amfi.objects.all(). \
        annotate(
        cur_oku=ExpressionWrapper(Subquery(dematsum_qs.values('ds_mktvalue')[:1]) / 1000,
                                  output_field=IntegerField())). \
        annotate(plan_oku=Subquery(gcweight_qs.values('gcw_cap_weight')[:1])). \
        annotate(tbd_oku=ExpressionWrapper(F('plan_oku') - F('cur_oku'), output_field=IntegerField())). \
        annotate(bat=Subquery(tl_qs.values('tl_bat')[:1])). \
        annotate(ca_total=Subquery(ca_qs.values('ca_total')[:1])). \
        annotate(funda_reco_type=Subquery(gfunda_reco_qs.values('funda_reco_type')[:1])). \
        annotate(funda_reco_cause=Subquery(gfunda_reco_qs.values('funda_reco_cause')[:1])). \
        annotate(dt_date=Subquery(demattxn_qs.values('dt_date')[:1])). \
        annotate(bhav_price=Subquery(bhav_qs.values('bhav_price')[:1])). \
        annotate(ftwhl_low=Subquery(ftwhl_qs.values('ftwhl_low')[:1])). \
        annotate(safety_margin=ExpressionWrapper((F('bat') - F('bhav_price')) * 100.0 / F('bhav_price'),
                                                 output_field=IntegerField())). \
        annotate(valuation_reco=Case( \
        When(safety_margin__gt=10, then=Value('Upside')), \
        When(safety_margin__lt=-10, then=Value('Downside')), \
        default=Value('Neutral'), \
        output_field=CharField() \
        )). \
        annotate(low_margin=ExpressionWrapper((F('bhav_price') - F('ftwhl_low')) * 100.0 / F('ftwhl_low'),
                                              output_field=IntegerField())). \
        annotate(industry=Subquery(indices_qs.values('ind_industry')[:1])). \
        filter(Q(bhav_price__isnull=False) & Q(bat__isnull=False)). \
        filter(funda_reco_type='Weak'). \
        values('nse_symbol', 'comp_name', 'bhav_price', 'bat', 'ftwhl_low',
               'valuation_reco', 'safety_margin',
               'low_margin', 'ca_total', 'dt_date', 'plan_oku', 'cur_oku',
               'tbd_oku', 'funda_reco_type', 'funda_reco_cause',
               'industry', 'cap_type'). \
        order_by('safety_margin')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        funda_reco_list = (
            Gfundareco.objects.all().values('funda_reco_type').annotate(funda_reco_count=Count('funda_reco_type')).
                order_by('funda_reco_count'))

        context["funda_reco_list"] = funda_reco_list

        return context

    def get_template_names(self):
        app_label = 'advisor'
        template_name_first = app_label + '/' + 'advisor_list.html'
        template_names_list = [template_name_first]
        return template_names_list


class AdvisorListView_Moderate(ListView):
    # model = Advisor
    # if pagination is desired
    # paginate_by = 300
    # filter_backends = [filters.OrderingFilter,]
    # ordering_fields = ['sno', 'nse_symbol']
    indices_qs = Indices.objects.filter(ind_isin=OuterRef("comp_isin"))
    bhav_qs = Bhav.objects.filter(bhav_isin=OuterRef("comp_isin"))
    ca_qs = Corpact.objects.filter(ca_ticker=OuterRef("nse_symbol"))
    ftwhl_qs = Ftwhl.objects.filter(ftwhl_ticker=OuterRef("nse_symbol"))
    gfunda_reco_qs = Gfundareco.objects.filter(funda_reco_isin=OuterRef("comp_isin"))
    tl_qs = Trendlyne.objects.filter(tl_nse=OuterRef("nse_symbol"))
    dematsum_qs = DematSum.objects.filter(ds_isin=OuterRef("comp_isin"))
    demattxn_qs = DematTxn.objects.filter(dt_isin=OuterRef("comp_isin")).order_by('-dt_date').values('dt_date')
    gcweight_qs = Gcweight.objects.filter(gcw_cap_type=OuterRef("cap_type"))
    queryset = Amfi.objects.all(). \
        annotate(
        cur_oku=ExpressionWrapper(Subquery(dematsum_qs.values('ds_mktvalue')[:1]) / 1000,
                                  output_field=IntegerField())). \
        annotate(plan_oku=Subquery(gcweight_qs.values('gcw_cap_weight')[:1])). \
        annotate(tbd_oku=ExpressionWrapper(F('plan_oku') - F('cur_oku'), output_field=IntegerField())). \
        annotate(bat=Subquery(tl_qs.values('tl_bat')[:1])). \
        annotate(ca_total=Subquery(ca_qs.values('ca_total')[:1])). \
        annotate(funda_reco_type=Subquery(gfunda_reco_qs.values('funda_reco_type')[:1])). \
        annotate(funda_reco_cause=Subquery(gfunda_reco_qs.values('funda_reco_cause')[:1])). \
        annotate(dt_date=Subquery(demattxn_qs.values('dt_date')[:1])). \
        annotate(bhav_price=Subquery(bhav_qs.values('bhav_price')[:1])). \
        annotate(ftwhl_low=Subquery(ftwhl_qs.values('ftwhl_low')[:1])). \
        annotate(safety_margin=ExpressionWrapper((F('bat') - F('bhav_price')) * 100.0 / F('bhav_price'),
                                                 output_field=IntegerField())). \
        annotate(valuation_reco=Case( \
        When(safety_margin__gt=10, then=Value('Upside')), \
        When(safety_margin__lt=-10, then=Value('Downside')), \
        default=Value('Neutral'), \
        output_field=CharField() \
        )). \
        annotate(low_margin=ExpressionWrapper((F('bhav_price') - F('ftwhl_low')) * 100.0 / F('ftwhl_low'),
                                              output_field=IntegerField())). \
        annotate(industry=Subquery(indices_qs.values('ind_industry')[:1])). \
        filter(Q(bhav_price__isnull=False) & Q(bat__isnull=False)). \
        filter(funda_reco_type='Moderate'). \
        values('nse_symbol', 'comp_name', 'bhav_price', 'bat', 'ftwhl_low',
               'valuation_reco', 'safety_margin',
               'low_margin', 'ca_total', 'dt_date', 'plan_oku', 'cur_oku',
               'tbd_oku',
               'funda_reco_type', 'funda_reco_cause', 'industry', 'cap_type'). \
        order_by('-safety_margin')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        funda_reco_list = (
            Gfundareco.objects.all().values('funda_reco_type').annotate(funda_reco_count=Count('funda_reco_type')).
                order_by('funda_reco_count'))

        context["funda_reco_list"] = funda_reco_list

        return context

    def get_template_names(self):
        app_label = 'advisor'
        template_name_first = app_label + '/' + 'advisor_list.html'
        template_names_list = [template_name_first]
        return template_names_list
