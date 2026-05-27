from django.urls import path
from . import views


urlpatterns = [
    path('', views.AccountingListView.as_view(), name='accounting'),
    path('add/', views.accounting_addition, name='add-accounting'),
]
