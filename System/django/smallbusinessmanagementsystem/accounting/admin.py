from django.contrib import admin
from .models import Accounting


@admin.register(Accounting)
class AccountingAdmin(admin.ModelAdmin):
    list_display = ('date', 'concept', 'description', 'debit', 'credit')


