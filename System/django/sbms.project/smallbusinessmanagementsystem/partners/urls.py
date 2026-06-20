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
    path('', views.index, name='index'),
    path('partners/', views.PartnersListView.as_view(), name='partners'),
    path('partner/<int:pk>', views.PartnerDetailView.as_view(), name='partner-detail'),
    path('person/<int:pk>', views.PersonDetailView.as_view(), name='person-detail'),
    path('partners/create/', views.partner_creation, name='create-partner'),
    path('partners/update/<int:pk>', views.partner_update, name='update-partner'),
]
