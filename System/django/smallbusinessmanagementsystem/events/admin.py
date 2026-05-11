from django.contrib import admin
from .models import Event, Share, News


@admin.register(Event)
class EventsAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'time', 'creation', 'description', 'charge', 'automatic', 'validity')


@admin.register(Share)
class ShareAdmin(admin.ModelAdmin):
    list_display = ('event', 'partner', 'attendees', 'payment')


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('brief', 'event', 'edition', 'description')
