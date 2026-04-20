from django.urls import path
from . import views


urlpatterns = [
    path('', views.UsersListView.as_view(), name='users'),
    path('<int:pk>', views.UserDetailView.as_view(), name='user-detail'),
]
