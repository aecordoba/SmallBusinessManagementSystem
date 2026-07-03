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
from .models import Partner, Person, Address
from events.models import News, Event, Share
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from .forms import PartnerForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db import transaction
from datetime import timedelta
from django.db.models import Q
from dateutil.relativedelta import relativedelta
from django.db.models import Max
from django.utils import timezone


def index(request):
    partners_quantity = Partner.objects.count()
    aside_list = News.objects.filter(Q(event=None) | Q(event__date__gte=timezone.now()))[:3]
    for news in aside_list:
        news.description = news.description[:60]
    context = {
        'partners_quantity': partners_quantity,
        'aside_list': aside_list
    }
    return render(request, 'index.html', context=context)


@login_required
@permission_required('partners.add_partner', raise_exception=True)
def partner_creation(request):
    if request.method == 'POST':
        form = PartnerForm(request.POST)
        if form.is_valid():
            save_partner(form, Partner(), Person(), Address())
            return HttpResponseRedirect(reverse('partners'))
    else:
        max_partner_number = Partner.objects.aggregate(Max('partner_number'))['partner_number__max']
        if max_partner_number:
            data = {'partner_number': max_partner_number + 1}
        else:
            data = {'partner_number': 1}
        form = PartnerForm(initial=data)
    context = {'form': form, 'create': True}
    return render(request, 'partners/partner_form.html', context)


@login_required
@permission_required('partners.change_partner', raise_exception=True)
def partner_update(request, pk):
    partner = Partner.objects.get(pk=pk)
    if request.method == 'POST':
        form = PartnerForm(request.POST, instance=partner)
        if form.is_valid():
            save_partner(form, partner, partner.person, partner.person.address)
            return HttpResponseRedirect(reverse('partners'))
    else:
        form = PartnerForm(instance=partner)
    context = {'form': form, 'create': False}
    return render(request, 'partners/partner_form.html', context)


@transaction.atomic
def save_partner(form, partner, person, address):
    """ Save a complete Partner data."""
    # Save address.
    address.address = form.cleaned_data['address']
    address.zip_code = form.cleaned_data['zip_code']
    address.city = form.cleaned_data['city']
    address.phone = form.cleaned_data['phone']
    address.save()
    # Save person.
    person.first_name = form.cleaned_data['first_name']
    person.last_name = form.cleaned_data['last_name']
    person.identification = form.cleaned_data['identification']
    person.id_number = form.cleaned_data['id_number']
    person.social_security = form.cleaned_data['social_security']
    person.email = form.cleaned_data['email']
    person.birthdate = form.cleaned_data['birthdate']
    person.gender = form.cleaned_data['gender']
    person.cellphone = form.cleaned_data['cellphone']
    person.address = address
    person.save()
    # Save partner.
    partner.partner_number = form.cleaned_data['partner_number']
    partner.incorporation = form.cleaned_data['incorporation']
    partner.position = form.cleaned_data['position']
    partner.status = form.cleaned_data['status']
    partner.person = person
    partner.save()
    # Save the appropiate shares.
    if partner.status == 'status_1':
        incorporation = partner.incorporation
        auto_events = (Event.objects.filter(automatic=True).
                       filter((Q(validity='weekly') & Q(date__gt=incorporation - timedelta(weeks=1))) |
                              (Q(validity='monthly') & Q(date__gt=incorporation - relativedelta(months=1))) |
                              (Q(validity='yearly') & Q(date__gt=incorporation - relativedelta(years=1)))))
        # If partner has paid events, exclude them from automatic events.
        if Share.objects.filter(partner=partner, payment__gt=0).exists():
            paid_events = Share.objects.filter(partner=partner, payment__gt=0).values('event')
            auto_events = auto_events.exclude(id__in=paid_events)
        # Delete partner share he didn't pay.
        Share.objects.filter(partner=partner, payment=0).delete()
        # Save share to automatic events.
        for event in auto_events:
            share = Share()
            share.event = event
            share.partner = partner
            share.save()


class PartnersListView(LoginRequiredMixin, generic.ListView):
    model = Partner
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('search_data')
        if query:
            if query.isdigit():
                return Partner.objects.filter(partner_number__exact=query)
            else:
                return Partner.objects.filter(person__last_name__icontains=query)
        else:
            return Partner.objects.all()


class PartnerDetailView(PermissionRequiredMixin, generic.DetailView):
    permission_required = 'partners.view_partner'
    model = Partner


class PersonDetailView(PermissionRequiredMixin, generic.DetailView):
    permission_required = 'partners.view_person'
    model = Person
