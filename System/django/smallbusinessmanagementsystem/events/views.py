from django.views import generic
from django.shortcuts import render, redirect
from .models import News, Event, Share
from partners.models import Partner
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .forms import CreateEventForm, CreateNewsForm
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db import transaction
from django.utils import timezone
from django.db.models import Q, F, Sum


@login_required
@permission_required('events.add_event', raise_exception=True)
def event_creation(request):
    if request.method == 'POST':
        form = CreateEventForm(request.POST)
        if form.is_valid():
            save_event(form)
            return HttpResponseRedirect(reverse('events'))
    else:
        form = CreateEventForm()
    context = {'form': form,}
    return render(request, 'events/create_event.html', context)

@transaction.atomic
def save_event(form):
    """ Save the event. """
    event = Event()
    event.name = form.cleaned_data['name']
    event.date = form.cleaned_data['date']
    event.description = form.cleaned_data['description']
    event.charge = form.cleaned_data['charge']
    event.automatic = form.cleaned_data['automatic']
    if event.automatic:
        event.validity = form.cleaned_data['validity']
    else:
        event.time = form.cleaned_data['time']
        event.attendants = form.cleaned_data['attendants']
    event.save()
    # Save share.
    if event.automatic:
        for partner in Partner.objects.filter(status__exact='status_1'):
            share = Share()
            share.event = event
            share.partner = partner
            share.save()

@login_required
@permission_required('events.add_news', raise_exception=True)
def news_creation(request):
    if request.method == 'POST':
        form = CreateNewsForm(request.POST)
        if form.is_valid():
            save_news(form)
            return HttpResponseRedirect(reverse('news'))
    else:
        form = CreateNewsForm()
    context = {'form': form,}
    return render(request, 'events/create_news.html', context)

@transaction.atomic
def save_news(form):
    news = News()
    if form.cleaned_data['event']:
        news.event = form.cleaned_data['event']
    news.brief = form.cleaned_data['brief']
    if form.cleaned_data['description']:
        news.description = form.cleaned_data['description']
    news.save()

@login_required
def event_attend(request):
    if request.method == 'POST':
        event_pk = request.POST.get('event_pk')
        share = Share()
        share.event = Event.objects.get(pk=event_pk)
        share.partner = request.user.partner
        share.attendees = request.POST.get('attendees')
        share.save()
        return HttpResponseRedirect(reverse('events_attend_list'))

@login_required
@permission_required('events.change_share', raise_exception=True)
def allocate_payment(request):
    if request.method == 'POST':
        partner_pk = request.POST.get('partner_pk')
        partner = Partner.objects.get(pk=partner_pk)
        event = Event.objects.get(pk=request.POST.get('event_pk'))
        Share.objects.filter(partner=partner).filter(event=event).update(payment=F('payment')+request.POST.get('pay'))
        return redirect(reverse('partner_attendance_list', kwargs={'pk': partner_pk}))

class NewsListView(generic.ListView):
    model = News
    paginate_by = 5

    def get_queryset(self):
        return News.objects.filter(Q(event=None) | Q(event__date__gte=timezone.now()))


class NewsDetailView(generic.DetailView):
    model = News


class EventsListView(generic.ListView):
    model = Event
    paginate_by = 10

    def get_queryset(self):
        return Event.objects.filter(date__gte=timezone.now())


class EventsAttendListView(LoginRequiredMixin,generic.ListView):
    paginate_by = 10
    context_object_name = 'share_list'
    template_name = 'events/share_list.html'

    def get_queryset(self):
        return Share.objects.select_related('event').filter(event__automatic=False, event__date__gte=timezone.now(), partner=self.request.user.partner).annotate(debt=F('attendees')*F('event__charge')-F('payment')).order_by('event__date').order_by('event__time')


class EventDetailView(LoginRequiredMixin, generic.DetailView):
    model = Event

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object.automatic:
            context['automatic'] = True
        else:
            partner = self.request.user.partner
            registered = Share.objects.filter(event=self.object, partner=partner).exists()
            attendees = Share.objects.filter(event=self.object).aggregate(Sum('attendees'))['attendees__sum']
            attendees = 0 if attendees is None else attendees
            vacancies = self.object.attendants - attendees
            context['vacancies'] = vacancies
            context['registered'] = registered
        return context

class PartnerAttendanceListView(PermissionRequiredMixin, generic.ListView):
    permission_required = ('events.add_share', 'events.change_share', 'events.delete_share')
    paginate_by = 10
    context_object_name = 'share_list'
    template_name = 'events/partner_attendance_list.html'

    def get_queryset(self, **kwargs):
        partner_pk = self.kwargs.get('pk')
        return Share.objects.select_related('event').filter(partner=Partner.objects.get(pk=partner_pk)).filter(payment__lt=F('attendees')*F('event__charge')).annotate(debt=F('attendees')*F('event__charge')-F('payment')).order_by('event__date').order_by('event__time')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['partner'] = Partner.objects.get(pk=self.kwargs.get('pk'))
        return context
