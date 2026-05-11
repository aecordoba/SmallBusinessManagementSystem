from django.shortcuts import render
from django.views import generic
from .models import User
from django.contrib.auth.mixins import PermissionRequiredMixin


class UsersListView(PermissionRequiredMixin, generic.ListView):
    permission_required = 'users.view_user'
    model = User
    paginate_by = 10

    context_object_name = 'users_no_admin'
    queryset = User.objects.exclude(is_superuser=True)


class UserDetailView(PermissionRequiredMixin, generic.DetailView):
    permission_required = 'users.view_user'
    model = User
