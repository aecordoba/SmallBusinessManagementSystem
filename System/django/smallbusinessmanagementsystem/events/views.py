from django.views import generic
from django.shortcuts import render
from .models import News, Event


class NewsListView(generic.ListView):
    model = News
    paginate_by = 10


class NewsDetailView(generic.DetailView):
    model = News


class EventsListView(generic.ListView):
    model = Event
    paginate_by = 10


class EventDetailView(generic.DetailView):
    model = Event
