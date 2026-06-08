from django.urls import path
from . import views


urlpatterns = [
    path('news/', views.NewsListView.as_view(), name='news'),
    path('news/<int:pk>', views.NewsDetailView.as_view(), name='news-detail'),
    path('', views.EventsListView.as_view(), name='events'),
    path('<int:pk>', views.EventDetailView.as_view(), name='event-detail'),
    path('create/', views.event_creation, name='create-event'),
    path('news/create/', views.news_creation, name='create-news'),
    path('attend/', views.event_attend, name='event-attend'),
    path('share/', views.EventsAttendanceListView.as_view(), name='events-attendance-list'),
    path('share/<int:pk>', views.PartnerAttendanceListView.as_view(), name='partner-attendance-list'),
    path('payment/', views.allocate_payment, name='allocate-payment'),
    path('remove_attendance/', views.remove_attendance, name='remove-attendance'),
    path('attendees/<int:event>', views.AttendeesListView.as_view(), name='list-attendees'),
    path('share/partner/<int:pk>', views.PartnerSharingListView.as_view(), name='partner-sharing'),
    path('sharing/', views.add_sharing, name='add-sharing'),
]
