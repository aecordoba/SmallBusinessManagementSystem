from django.views import generic
from django.shortcuts import render
from .models import Accounting
from django.contrib.auth.mixins import PermissionRequiredMixin


class AccountingListView(PermissionRequiredMixin, generic.ListView):
    permission_required = 'accounting.view_accounting'
    model = Accounting
    paginate_by = 10

