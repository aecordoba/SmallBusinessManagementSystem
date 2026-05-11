from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('partners/', views.PartnersListView.as_view(), name='partners'),
    path('partner/<int:pk>', views.PartnerDetailView.as_view(), name='partner-detail'),
    path('person/<int:pk>', views.PersonDetailView.as_view(), name='person-detail'),
    path('partners/create/', views.partner_creation, name='create-partner'),
]
