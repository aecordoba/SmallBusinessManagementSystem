from django.views import generic
from django.shortcuts import render
from .models import News, Event, Share
from partners.models import Partner
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CreateEventForm, CreateNewsForm
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db import transaction
from django.utils import timezone
from django.db.models import Q


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


class NewsListView(generic.ListView):
    model = News
    paginate_by = 5

    def get_queryset(self):
        return News.objects.filter(Q(event=None) | Q(event__date__gt=timezone.now()))


class NewsDetailView(generic.DetailView):
    model = News


class EventsListView(generic.ListView):
    model = Event
    paginate_by = 10

    def get_queryset(self):
        return Event.objects.filter(date__gt=timezone.now())


class EventDetailView(LoginRequiredMixin, generic.DetailView):
    model = Event
