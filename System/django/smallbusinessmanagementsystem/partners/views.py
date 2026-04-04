from django.views import generic
from django.shortcuts import render
from .models import Partner
from news.models import News


def index(request):
    partners_quantity = Partner.objects.count()
    news_aside = News.objects.all()[:3]

    for news in news_aside:
        news.description = news.description[:60]

    context = {
        'partners_quantity': partners_quantity,
        'news_aside': news_aside
        }

    return render(request, 'index.html', context=context)


class PartnersListView(generic.ListView):
    model = Partner


class PartnerDetailView(generic.DetailView):
    model = Partner

