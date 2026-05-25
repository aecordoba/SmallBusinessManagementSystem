from django.urls import path
from . import views


urlpatterns = [
    path('', views.UsersListView.as_view(), name='users'),
    path('<int:pk>', views.UserDetailView.as_view(), name='user-detail'),
    path('create/', views.user_creation, name='create-user'),
    path('update/<int:pk>', views.user_update, name='update-user'),
    path('delete/<int:pk>', views.UserDelete.as_view(), name='delete-user'),
]
