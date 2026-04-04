from django.views import generic
from django.shortcuts import render
from .models import News


class NewsListView(generic.ListView):
    model = News
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        news_aside = News.objects.all()[:3]
        for news in news_aside:
            news.description = news.description[:60]
        context['news_aside'] = news_aside
        return context


class NewsDetailView(generic.DetailView):
    model = News

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        news_aside = News.objects.all()[:3]
        for news in news_aside:
            news.description = news.description[:60]
        context['news_aside'] = news_aside
        return context

