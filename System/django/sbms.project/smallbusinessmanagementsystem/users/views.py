#  		views.py			Jun 20, 2026
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

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.views.generic.edit import DeleteView
from .models import User
from django.contrib.auth.models import Group
from .forms import UserForm
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse_lazy
from django.db import transaction


@login_required
@permission_required('users.add_user', raise_exception=True)
def user_creation(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            save_user(form, User())
            return HttpResponseRedirect(reverse('users'))
    else:
        form = UserForm()
        context = {'form': form, 'create': True}
        return render(request, 'users/user_form.html', context)


@login_required
@permission_required('users.change_user', raise_exception=True)
def user_update(request, pk):
    user = User.objects.get(pk=pk)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            save_user(form, user)
            return HttpResponseRedirect(reverse('users'))
    else:
        form = UserForm(instance=user)
        context = {'form': form, 'create': False}
        return render(request, 'users/user_form.html', context)


@transaction.atomic
def save_user(form, user):
    name = form.cleaned_data['name']
    user.name = name
    user.partner = form.cleaned_data['partner']
    user.is_active = form.cleaned_data['is_active']
    user.is_staff = form.cleaned_data['is_staff']
    user.save()
    # Add or remove Management group.
    user = User.objects.get(name=name)
    group = Group.objects.get(name='Management')
    if user.is_staff:
        user.groups.add(group)
    else:
        user.groups.remove(group)


class UsersListView(PermissionRequiredMixin, generic.ListView):
    permission_required = 'users.view_user'
    model = User
    paginate_by = 10

    context_object_name = 'users_no_admin'
    queryset = User.objects.exclude(is_superuser=True)


class UserDetailView(PermissionRequiredMixin, generic.DetailView):
    permission_required = 'users.view_user'
    model = User
    context_object_name = 'user_to_show'


class UserDelete(PermissionRequiredMixin, DeleteView):
    model = User
    permission_required = 'users.delete_user'
    success_url = reverse_lazy('users')

    def form_valid(self, form):
        try:
            self.object.delete()
            return HttpResponseRedirect(self.success_url)
        except Exception as e:
            return HttpResponseRedirect(reverse("user-delete", kwargs={"pk": self.object.pk}))
