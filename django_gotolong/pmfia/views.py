# Create your views here.

from django.views.generic.list import ListView

from django_gotolong.gmutfun.models import Gmutfun
from django_gotolong.umufub.models import Umufub

from django_gotolong.umfcent.models import Umfcent

from django.db.models import (OuterRef, Subquery, ExpressionWrapper)
from django.db.models import (F, IntegerField, Count, Q)
from django.db.models import Case, Value, When, CharField

from django_gotolong.jsched.tasks import jsched_task_bg, jsched_task_daily
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

import re
from itertools import zip_longest


class PmfiaListView_Lead(ListView):

    def get_queryset(self):

        # self.queryset = Umufub.objects.all().filter(umfb_user_id=self.request.user.id)
        self.queryset = Umfcent.objects.all().filter(umfcent_user_id=self.request.user.id)

        return self.queryset

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PmfiaListView_Lead, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        min_score_grade = self.kwargs['min_score_grade']

        qs_flexi = Gmutfun.objects.all().filter(Q(gmutfun_type='Active')). \
            filter(Q(gmutfun_scheme__contains='Flexi')). \
            filter(Q(gmutfun_benchmark__contains='500 Total Return Index')). \
            exclude(gmutfun_benchmark__contains=','). \
            filter(gmutfun_aum__gte=1000). \
            filter(gmutfun_alpha_grade__gte=min_score_grade). \
            order_by('-gmutfun_alpha_pct', '-gmutfun_aum')

        qs_large = Gmutfun.objects.all().filter(Q(gmutfun_type='Active')). \
            filter(Q(gmutfun_benchmark__contains='100 Total Return Index')). \
            exclude(gmutfun_benchmark__contains=','). \
            filter(gmutfun_aum__gte=1000). \
            filter(gmutfun_alpha_grade__gte=min_score_grade). \
            order_by('-gmutfun_alpha_pct', '-gmutfun_aum')

        qs_mid = Gmutfun.objects.all().filter(Q(gmutfun_type='Active')). \
            filter(Q(gmutfun_benchmark__contains='Midcap 150 Total Return Index') |
                   Q(gmutfun_benchmark__contains='150 MidCap Total Return Index')). \
            exclude(gmutfun_benchmark__contains=','). \
            filter(gmutfun_aum__gte=1000). \
            filter(gmutfun_alpha_grade__gte=min_score_grade). \
            order_by('-gmutfun_alpha_pct', '-gmutfun_aum')

        qs_small = Gmutfun.objects.all().filter(Q(gmutfun_type='Active')). \
            filter(Q(gmutfun_benchmark__contains='Smallcap 250 Total Return Index') |
                   Q(gmutfun_benchmark__contains='250 SmallCap Total Return Index')). \
            exclude(gmutfun_benchmark__contains=','). \
            filter(gmutfun_aum__gte=1000). \
            filter(gmutfun_alpha_grade__gte=min_score_grade). \
            order_by('-gmutfun_alpha_pct', '-gmutfun_aum')

        flex_list = []
        large_list = []
        mid_list = []
        small_list = []

        for q1 in (qs_flexi | qs_large | qs_mid | qs_small):
            g_name = q1.gmutfun_scheme.lower()
            g_name = g_name.split("fund")[0]
            g_benchmark = q1.gmutfun_benchmark
            # print(q1)
            for q2 in self.queryset:
                # print(q2)
                # print(g_name, ':', u_name)
                if False:
                    # umf broker path
                    u_name = q2.umfb_name.lower()

                else:
                    # umf central path
                    u_name = q2.umfcent_name.lower()
                u_name = u_name.split("fund")[0]

                # print(g_name, ':', u_name)

                # remove hyphen from mid-cap
                # how to treat flexicap and flexi cap as same
                # smallcap vs small cap
                # largecap vs large cap
                # midcap vs mid cap
                # bluechip vs blue chip

                g_name = re.sub(r"-", "", g_name)
                g_name = re.sub(r"flexi cap", "flexicap", g_name)
                g_name = re.sub(r"large cap", "largecap", g_name)
                g_name = re.sub(r"mid cap", "midcap", g_name)
                g_name = re.sub(r"small cap", "smallcap", g_name)
                g_name = re.sub(r"blue chip", "bluechip", g_name)

                u_name = re.sub(r"-", "", u_name)
                u_name = re.sub(r"flexi cap", "flexicap", u_name)
                u_name = re.sub(r"large cap", "largecap", u_name)
                u_name = re.sub(r"mid cap", "midcap", u_name)
                u_name = re.sub(r"small cap", "smallcap", u_name)
                u_name = re.sub(r"blue chip", "bluechip", u_name)

                if g_name == u_name:
                    print('match ', g_name, ':', u_name)
                    g_name = g_name + '(*)'
                    break

            max_captype_mf = self.kwargs['max_captype_mf']
            if re.search('500', g_benchmark):
                if len(flex_list) < max_captype_mf:
                    flex_list.append(g_name)
            elif re.search('100', g_benchmark):
                if len(large_list) < max_captype_mf:
                    large_list.append(g_name)
            elif re.search('150', g_benchmark):
                if len(mid_list) < max_captype_mf:
                    mid_list.append(g_name)
            elif re.search('250', g_benchmark):
                if len(small_list) < max_captype_mf:
                    small_list.append(g_name)

        context["pmfia_flex_list"] = flex_list
        context["pmfia_large_list"] = large_list
        context["pmfia_mid_list"] = mid_list
        context["pmfia_small_list"] = small_list

        context["all_list"] = list(zip_longest(flex_list, large_list, mid_list, small_list, fillvalue='-'))

        return context

    def get_template_names(self):
        app_label = 'pmfia'
        template_name_first = app_label + '/' + 'pmfia_list.html'
        template_names_list = [template_name_first]
        return template_names_list


class PmfiaListView_AUM(ListView):

    def get_queryset(self):

        # self.queryset = Umufub.objects.all().filter(umfb_user_id=self.request.user.id)
        self.queryset = Umfcent.objects.all().filter(umfcent_user_id=self.request.user.id)
        return self.queryset

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PmfiaListView_AUM, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # select all of them
        min_score_grade = 0

        qs_flexi = Gmutfun.objects.all().filter(Q(gmutfun_type='Active')). \
            filter(Q(gmutfun_scheme__contains='Flexi')). \
            filter(Q(gmutfun_benchmark__contains='500 Total Return Index')). \
            exclude(gmutfun_benchmark__contains=','). \
            filter(gmutfun_aum__gte=1000). \
            filter(gmutfun_alpha_grade__gte=min_score_grade). \
            order_by('-gmutfun_aum', '-gmutfun_alpha_pct')

        qs_large = Gmutfun.objects.all().filter(Q(gmutfun_type='Active')). \
            filter(Q(gmutfun_benchmark__contains='100 Total Return Index')). \
            exclude(gmutfun_benchmark__contains=','). \
            filter(gmutfun_aum__gte=1000). \
            filter(gmutfun_alpha_grade__gte=min_score_grade). \
            order_by('-gmutfun_aum', '-gmutfun_alpha_pct')

        qs_mid = Gmutfun.objects.all().filter(Q(gmutfun_type='Active')). \
            filter(Q(gmutfun_benchmark__contains='Midcap 150 Total Return Index') |
                   Q(gmutfun_benchmark__contains='150 MidCap Total Return Index')). \
            exclude(gmutfun_benchmark__contains=','). \
            filter(gmutfun_aum__gte=1000). \
            filter(gmutfun_alpha_grade__gte=min_score_grade). \
            order_by('-gmutfun_aum', '-gmutfun_alpha_pct')

        qs_small = Gmutfun.objects.all().filter(Q(gmutfun_type='Active')). \
            filter(Q(gmutfun_benchmark__contains='Smallcap 250 Total Return Index') |
                   Q(gmutfun_benchmark__contains='250 SmallCap Total Return Index')). \
            exclude(gmutfun_benchmark__contains=','). \
            filter(gmutfun_aum__gte=1000). \
            filter(gmutfun_alpha_grade__gte=min_score_grade). \
            order_by('-gmutfun_aum', '-gmutfun_alpha_pct')

        flex_list = []
        large_list = []
        mid_list = []
        small_list = []

        for q1 in (qs_flexi | qs_large | qs_mid | qs_small):
            g_name = q1.gmutfun_scheme.lower()
            g_name = g_name.split("fund")[0]
            g_benchmark = q1.gmutfun_benchmark
            # print(q1)
            for q2 in self.queryset:
                # print(q2)
                # print(g_name, ':', u_name)
                if False:
                    # umf broker path
                    u_name = q2.umfb_name.lower()

                else:
                    # umf central path
                    u_name = q2.umfcent_name.lower()
                u_name = u_name.split("fund")[0]
                # print(g_name, ':', u_name)

                # remove hyphen from mid-cap
                # how to treat flexicap and flexi cap as same
                # smallcap vs small cap
                # largecap vs large cap
                # midcap vs mid cap
                # bluechip vs blue chip

                g_name = re.sub(r"-", "", g_name)
                g_name = re.sub(r"flexi cap", "flexicap", g_name)
                g_name = re.sub(r"large cap", "largecap", g_name)
                g_name = re.sub(r"mid cap", "midcap", g_name)
                g_name = re.sub(r"small cap", "smallcap", g_name)
                g_name = re.sub(r"blue chip", "bluechip", g_name)

                u_name = re.sub(r"-", "", u_name)
                u_name = re.sub(r"flexi cap", "flexicap", u_name)
                u_name = re.sub(r"large cap", "largecap", u_name)
                u_name = re.sub(r"mid cap", "midcap", u_name)
                u_name = re.sub(r"small cap", "smallcap", u_name)
                u_name = re.sub(r"blue chip", "bluechip", u_name)

                if g_name == u_name:
                    print('match ', g_name, ':', u_name)
                    g_name = g_name + '(*)'
                    break

            max_captype_mf = self.kwargs['max_captype_mf']
            if re.search('500', g_benchmark):
                if len(flex_list) < max_captype_mf:
                    flex_list.append(g_name)
            elif re.search('100', g_benchmark):
                if len(large_list) < max_captype_mf:
                    large_list.append(g_name)
            elif re.search('150', g_benchmark):
                if len(mid_list) < max_captype_mf:
                    mid_list.append(g_name)
            elif re.search('250', g_benchmark):
                if len(small_list) < max_captype_mf:
                    small_list.append(g_name)

        context["pmfia_flex_list"] = flex_list
        context["pmfia_large_list"] = large_list
        context["pmfia_mid_list"] = mid_list
        context["pmfia_small_list"] = small_list

        context["all_list"] = list(zip_longest(flex_list, large_list, mid_list, small_list, fillvalue='-'))

        return context

    def get_template_names(self):
        app_label = 'pmfia'
        template_name_first = app_label + '/' + 'pmfia_list.html'
        template_names_list = [template_name_first]
        return template_names_list
