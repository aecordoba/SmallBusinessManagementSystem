#  		urls.py			Jun 19, 2026
#  				Adrián E. Córdoba [software.dynamicmcs@gmail.com]
#
#  Copyright (C) 2026
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

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
