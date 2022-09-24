# Create your views here.

from django.views.generic.list import ListView

from django_gotolong.amfi.models import Amfi
from django_gotolong.bhav.models import Bhav
from django_gotolong.brokersum.models import BrokerSum
from django_gotolong.brokertxn.models import BrokerTxn
from django_gotolong.brokermf.models import BrokerMf
from django_gotolong.bstmtdiv.models import BstmtDiv
from django_gotolong.corpact.models import Corpact
from django_gotolong.dematsum.models import DematSum
from django_gotolong.demattxn.models import DematTxn
from django_gotolong.dividend.models import Dividend
from django_gotolong.fratio.models import Fratio
from django_gotolong.ftwhl.models import Ftwhl
from django_gotolong.gfundareco.models import Gfundareco
from django_gotolong.gcweight.models import Gcweight
from django_gotolong.gmutfun.models import Gmutfun
from django_gotolong.indices.models import Indices
from django_gotolong.lastrefd.models import Lastrefd
from django_gotolong.othinv.models import Othinv
# from django_gotolong.peqia.models import Peqia
# from django_gotolong.pmfia.models import Pmfia
# from django_gotolong.screener.models import Screener
from django_gotolong.trendlyne.models import Trendlyne
from django_gotolong.udepcas.models import Udepcas
from django_gotolong.uiweight.models import Uiweight
from django_gotolong.umfcent.models import Umfcent
from django_gotolong.umufub.models import Umufub

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class DbstatListView(ListView):
    db_stat = {}
    db_rows = 0

    # model = Peqia
    # if pagination is desired
    # paginate_by = 300
    # filter_backends = [filters.OrderingFilter,]
    # ordering_fields = ['sno', 'nse_symbol']

    def get_queryset(self):
        return Amfi.objects.all()

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(DbstatListView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        self.db_stat['amfi'] = Amfi.objects.count()
        self.db_stat['bmf'] = BrokerMf.objects.count()
        self.db_stat['bsum'] = BrokerSum.objects.count()
        self.db_stat['btxn'] = BrokerTxn.objects.count()
        self.db_stat['bhav'] = Bhav.objects.count()
        self.db_stat['bstmtdiv'] = BstmtDiv.objects.count()
        self.db_stat['corpact'] = Corpact.objects.count()
        self.db_stat['dematsum'] = DematSum.objects.count()
        self.db_stat['demattxn'] = DematTxn.objects.count()
        self.db_stat['dividend'] = Dividend.objects.count()
        self.db_stat['fratio'] = Fratio.objects.count()
        self.db_stat['ftwhl'] = Ftwhl.objects.count()
        self.db_stat['gfundareco'] = Gfundareco.objects.count()
        self.db_stat['gcweight'] = Gcweight.objects.count()
        self.db_stat['gmutfun'] = Gmutfun.objects.count()
        self.db_stat['indices'] = Indices.objects.count()
        self.db_stat['lastrefd'] = Lastrefd.objects.count()
        self.db_stat['othinv'] = Othinv.objects.count()
        # self.db_stat['peqia'] = Peqia.objects.count()
        # self.db_stat['pmfia'] = Pmfia.objects.count()
        self.db_stat['udepcas'] = Udepcas.objects.count()
        self.db_stat['uiweight'] = Uiweight.objects.count()
        self.db_stat['umfcent'] = Umfcent.objects.count()
        self.db_stat['umufub'] = Umufub.objects.count()
        # db_stat['screener'] = Screener.objects.count()
        self.db_stat['trendlyne'] = Trendlyne.objects.count()

        context["db_stat"] = self.db_stat

        for k in self.db_stat.keys():
            v = self.db_stat[k]
            print(k, v)
            self.db_rows += v
        print('total rows', self.db_rows)

        context["db_rows"] = self.db_rows

        return context

    def get_template_names(self):
        app_label = 'dbstat'
        template_name_first = app_label + '/' + 'dbstat_list.html'
        template_names_list = [template_name_first]
        return template_names_list
