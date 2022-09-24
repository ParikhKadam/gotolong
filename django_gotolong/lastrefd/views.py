# Create your views here.

# Create your views here.

# Create your views here.

from django.views.generic.list import ListView

from django_gotolong.lastrefd.models import Lastrefd
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class LastrefdListView(ListView):
    model = Lastrefd
    # if pagination is desired
    # paginate_by = 300
    # filter_backends = [filters.OrderingLastrefd,]
    # ordering_fields = ['sno', 'nse_symbol']
    queryset = Lastrefd.objects.all()

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LastrefdListView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

# from django.http import HttpResponse
# def index(request):
#    return HttpResponse("Hello, world. You're at the polls index.")
#
