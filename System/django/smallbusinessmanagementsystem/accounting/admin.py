from django.contrib import admin
from .models import Accounting, Event, Share


@admin.register(Accounting)
class AccountingAdmin(admin.ModelAdmin):
    list_display = ('date', 'concept', 'description', 'debit', 'credit')


@admin.register(Event)
class EventsAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'time', 'creation', 'description', 'charge')


@admin.register(Share)
class ShareAdmin(admin.ModelAdmin):
    list_display = ('event', 'partner', 'attendees', 'payment')

