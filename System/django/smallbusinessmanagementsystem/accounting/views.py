from django.views import generic
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Accounting
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.db import transaction
from .forms import AddAccountingForm
from django.urls import reverse


@login_required
@permission_required('accounting.add_accounting', raise_exception=True)
def accounting_addition(request):
    if request.method == 'POST':
        form = AddAccountingForm(request.POST)
        if form.is_valid():
            save_accounting(form)
            return HttpResponseRedirect(reverse('accounting'))
    else:
        form = AddAccountingForm()
        context = {'form': form,}
        return render(request, 'accounting/add_accounting.html', context)

@transaction.atomic
def save_accounting(form):
    accounting = Accounting()
    accounting.date = form.cleaned_data['date']
    accounting.concept = form.cleaned_data['concept']
    accounting.description = form.cleaned_data['description']
    accounting.debit = form.cleaned_data['debit']
    accounting.credit = form.cleaned_data['credit']
    accounting.save()


class AccountingListView(PermissionRequiredMixin, generic.ListView):
    permission_required = 'accounting.view_accounting'
    model = Accounting
    paginate_by = 10

