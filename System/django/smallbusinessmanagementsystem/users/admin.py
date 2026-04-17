from django.contrib import admin
from .models import User


@admin.register(User)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('name', 'partner', 'date_joined', 'is_active', 'is_staff', 'is_superuser')


