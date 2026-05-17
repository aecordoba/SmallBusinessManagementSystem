from django.urls import path
from . import views


urlpatterns = [
    path('news/', views.NewsListView.as_view(), name='news'),
    path('news/<int:pk>', views.NewsDetailView.as_view(), name='news-detail'),
    path('', views.EventsListView.as_view(), name='events'),
    path('<int:pk>', views.EventDetailView.as_view(), name='event-detail'),
    path('create/', views.event_creation, name='create-event'),
    path('news/create/', views.news_creation, name='create-news'),
]
