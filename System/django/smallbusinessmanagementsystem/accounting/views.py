from django.views import generic
from django.shortcuts import render
from .models import Accounting


class AccountingListView(generic.ListView):
    model = Accounting
    paginate_by = 10

