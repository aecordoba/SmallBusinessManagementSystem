#  		admin.py			Jun 20, 2026
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

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    # Specify fields to display in the list view
    list_display = ('name', 'partner', 'is_superuser', 'is_staff', 'is_active')
    # Fields to show when editing an existing user
    fieldsets = (
        (None, {'fields': ('name', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
    )
    # Fields to show when creating a new user
    add_fieldsets = (
        (None, {
            'fields': ('name', 'password1', 'password2', 'partner', 'is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions'),
        }),
    )
    ordering = ('name',)


@admin.register(User)
class UsersAdmin(CustomUserAdmin):
    list_display = ('name', 'partner', 'email', 'date_joined', 'is_active', 'is_staff', 'is_superuser')


