from django.views import generic
from django.shortcuts import render
from .models import Partner, Person
from events.models import News


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


class PartnersListView(generic.ListView):
    model = Partner
    paginate_by = 10


class PartnerDetailView(generic.DetailView):
    model = Partner

class PersonDetailView(generic.DetailView):
    model = Person
