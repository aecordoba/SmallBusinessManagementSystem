from django.urls import path
from . import views


urlpatterns = [
    path('', views.NewsListView.as_view(), name='news'),
    path('<int:pk>', views.NewsDetailView.as_view(), name='news-detail'),
    path('events/', views.EventsListView.as_view(), name='events'),
    path('event/<int:pk>', views.EventDetailView.as_view(), name='event-detail'),
]
