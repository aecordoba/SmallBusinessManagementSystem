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


