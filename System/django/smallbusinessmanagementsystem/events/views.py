from django.views import generic
from django.shortcuts import render
from .models import News, Event
from django.contrib.auth.mixins import LoginRequiredMixin


class NewsListView(generic.ListView):
    model = News
    paginate_by = 10


class NewsDetailView(generic.DetailView):
    model = News


class EventsListView(generic.ListView):
    model = Event
    paginate_by = 10


class EventDetailView(LoginRequiredMixin, generic.DetailView):
    model = Event
