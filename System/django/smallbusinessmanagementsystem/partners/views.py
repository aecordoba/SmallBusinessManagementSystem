from django.views import generic
from django.shortcuts import render
from .models import Partner, Person, Address
from events.models import News, Event, Share
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from .forms import CreatePartnerForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db import transaction
from datetime import timedelta
from django.db.models import Q, F
from dateutil.relativedelta import relativedelta
from django.db.models import Max


def index(request):
    partners_quantity = Partner.objects.count()
    aside_list = News.objects.all()[:3]

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
        form = CreatePartnerForm(request.POST)
        if form.is_valid():
            save_partner(form)
            return HttpResponseRedirect(reverse('index'))
    else:
        data = {'partner_number': Partner.objects.aggregate(Max('partner_number'))['partner_number__max']+1}
        form = CreatePartnerForm(initial=data)
    context = {'form': form,}
    return render(request, 'partners/create_partner.html', context)

@transaction.atomic
def save_partner(form):
    """ Save a complete Partner data."""
    # Save address.
    address = Address()
    address.address = form.cleaned_data['address']
    address.zip_code = form.cleaned_data['zip_code']
    address.city = form.cleaned_data['city']
    address.phone = form.cleaned_data['phone']
    address.save()
    # Save person.
    person = Person()
    person.first_name = form.cleaned_data['first_name']
    person.last_name = form.cleaned_data['last_name']
    person.doc_type = form.cleaned_data['doc_type']
    person.doc_number = form.cleaned_data['doc_number']
    person.social_security = form.cleaned_data['social_security']
    person.email = form.cleaned_data['email']
    person.birthdate = form.cleaned_data['birthdate']
    person.gender = form.cleaned_data['gender']
    person.cellphone = form.cleaned_data['cellphone']
    person.address = address
    person.save()
    # Save partner.
    partner = Partner()
    partner.partner_number = form.cleaned_data['partner_number']
    partner.incorporation = form.cleaned_data['incorporation']
    partner.position = form.cleaned_data['position']
    partner.status = form.cleaned_data['status']
    partner.person = person
    partner.save()
    # Save the appropiate shares.
    if partner.status == 'status_1':
        incorporation = partner.incorporation
        auto_events = Event.objects.filter(automatic=True).filter((Q(validity='weekly') & Q(date__gt=incorporation - timedelta(weeks=1))) | (Q(validity='monthly') & Q(date__gt=incorporation - relativedelta(months=1))) | (Q(validity='yearly') & Q(date__gt=incorporation - relativedelta(years=1))))
        for event in auto_events:
            share = Share()
            share.event = event
            share.partner = partner
            share.save()


class PartnersListView(LoginRequiredMixin, generic.ListView):
    model = Partner
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q')
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
