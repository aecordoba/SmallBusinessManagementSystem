from django.shortcuts import render
from django.views import generic
from .models import User
from django.contrib.auth.mixins import LoginRequiredMixin


class UsersListView(LoginRequiredMixin, generic.ListView):
    model = User
    paginate_by = 10

    context_object_name = 'users_no_admin'
    queryset = User.objects.exclude(is_superuser=True)


class UserDetailView(LoginRequiredMixin, generic.DetailView):
    model = User
