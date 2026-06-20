#  		views.py			Jun 20, 2026
#  				Adrián E. Córdoba [software.dynamicmcs@gmail.com]
#
#  Copyright (C) 2026
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

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
        return None
    else:
        form = AddAccountingForm()
        context = {'form': form, }
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
