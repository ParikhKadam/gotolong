# Create your views here.

from django.views.generic.list import ListView

from django_gotolong.gmutfun.models import Gmutfun
from django_gotolong.umufu.models import Umufu

from django.db.models import (OuterRef, Subquery, ExpressionWrapper)
from django.db.models import (F, IntegerField, Count, Q)
from django.db.models import Case, Value, When, CharField

from django_gotolong.jsched.tasks import jsched_task_bg, jsched_task_daily
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

import re


class MfiaListView(ListView):

    def get_queryset(self):

        self.queryset = Umufu.objects.all().filter(umf_user_id=self.request.user.id)
        return self.queryset

    # @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(MfiaListView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        min_score_grade = self.kwargs['min_score_grade']

        qs_flexi = Gmutfun.objects.all().filter(Q(gmutfun_type='Active')). \
            filter(Q(gmutfun_scheme__contains='Flexi')). \
            filter(Q(gmutfun_benchmark__contains='500 Total Return Index')). \
            exclude(gmutfun_benchmark__contains=','). \
            filter(gmutfun_aum__gte=1000). \
            filter(gmutfun_score_grade__gte=min_score_grade). \
            order_by('-gmutfun_score_pct', '-gmutfun_aum')

        qs_large = Gmutfun.objects.all().filter(Q(gmutfun_type='Active')). \
            filter(Q(gmutfun_benchmark__contains='100 Total Return Index')). \
            exclude(gmutfun_benchmark__contains=','). \
            filter(gmutfun_aum__gte=1000). \
            filter(gmutfun_score_grade__gte=min_score_grade). \
            order_by('-gmutfun_score_pct', '-gmutfun_aum')

        qs_mid = Gmutfun.objects.all().filter(Q(gmutfun_type='Active')). \
            filter(Q(gmutfun_benchmark__contains='Midcap 150 Total Return Index') |
                   Q(gmutfun_benchmark__contains='150 MidCap Total Return Index')). \
            exclude(gmutfun_benchmark__contains=','). \
            filter(gmutfun_aum__gte=1000). \
            filter(gmutfun_score_grade__gte=min_score_grade). \
            order_by('-gmutfun_score_pct', '-gmutfun_aum')

        qs_small = Gmutfun.objects.all().filter(Q(gmutfun_type='Active')). \
            filter(Q(gmutfun_benchmark__contains='Smallcap 250 Total Return Index') |
                   Q(gmutfun_benchmark__contains='250 SmallCap Total Return Index')). \
            exclude(gmutfun_benchmark__contains=','). \
            filter(gmutfun_aum__gte=1000). \
            filter(gmutfun_score_grade__gte=min_score_grade). \
            order_by('-gmutfun_score_pct', '-gmutfun_aum')

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
                u_name = q2.umf_name.lower()
                u_name = u_name.split("fund")[0]
                # print(g_name, ':', u_name)
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

        context["mfia_flex_list"] = flex_list
        context["mfia_large_list"] = large_list
        context["mfia_mid_list"] = mid_list
        context["mfia_small_list"] = small_list

        return context

    def get_template_names(self):
        app_label = 'mfia'
        template_name_first = app_label + '/' + 'mfia_list.html'
        template_names_list = [template_name_first]
        return template_names_list
