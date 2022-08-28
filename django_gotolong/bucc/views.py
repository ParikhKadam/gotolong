# Create your views here.

from .models import Bucc

from django.shortcuts import render, redirect, get_object_or_404

from django.views.generic.list import ListView

from django.db.models import OuterRef, Subquery, Count, Sum, Max, Min
from django.db.models.functions import Trim, Lower, Round

from django_gotolong.amfi.models import Amfi, amfi_load_isin2ticker
from django_gotolong.gfundareco.models import Gfundareco

import pandas as pd
import csv, io
import openpyxl
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect

from django_gotolong.lastrefd.models import Lastrefd, lastrefd_update

from django_gotolong.comm import comfun


class BuccListView(ListView):
    model = Bucc

    # if pagination is desired
    # paginate_by = 300

    def get_queryset(self):
        return Bucc.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


# one parameter named request
def BuccUpload(request):
    # for quick debugging
    #
    # import pdb; pdb.set_trace()
    #
    # breakpoint()

    template = "invalid-get-request.html"

    list_url_name = "bucc-list"
    columns_list = ['UNUSED']

    # get rid of top 8 lines
    ignore_top_lines = 9
    data_set = comfun.comm_func_upload(request, template, columns_list, list_url_name, ignore_top_lines)

    # delete existing records
    print('Deleted existing Bucc data')
    Bucc.objects.all().delete()

    # setup a stream which is when we loop through each line we are able to handle a data in a stream

    io_string = io.StringIO(data_set)
    next(io_string)
    unique_id = 0
    for column in csv.reader(io_string, delimiter=',', quotechar='"'):
        unique_id += 1

        # sn - serial number
        bucc_id = column[0]
        # name of the tm
        bucc_name = column[1]
        # UCC OF ACTIVE CLIENTS
        bucc_value = column[3]

        if bucc_value == '-':
            bucc_value = 0

        if bucc_id != '':
            _, created = Bucc.objects.update_or_create(
                bucc_id=bucc_id,
                bucc_name=bucc_name,
                bucc_value=bucc_value
            )

    lastrefd_update("bucc")

    print('Completed loading new Bucc data')
    return HttpResponseRedirect(reverse(list_url_name))


def BuccReset(request):
    # delete existing records
    print('Cleared existing Bucc data')
    Bucc.objects.all().delete()
    return HttpResponseRedirect(reverse("bucc-list"))
