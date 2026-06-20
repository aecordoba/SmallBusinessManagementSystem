#  		models.py			Jun 19, 2026
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

from django.db import models
from django.urls import reverse
from partners.models import Partner
from django.utils.translation import gettext_lazy as _


class Event(models.Model):
    VALIDITIES = (
        ('monthly', _('monthly')),
        ('weekly', _('weekly')),
        ('yearly', _('yearly'))
    )

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, help_text='Event title')
    date = models.DateField(help_text='Event date')
    time = models.TimeField(blank=True, null=True, help_text='Event time')
    attendants = models.IntegerField(blank=True, null=True)
    creation = models.DateTimeField(help_text='Creation date', auto_now_add=True)
    description = models.TextField(blank=True, null=True, help_text='Event description')
    charge = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text='Event charge')
    automatic = models.BooleanField(help_text='Apply to all partners')
    validity = models.CharField(max_length=15, choices=VALIDITIES, blank=True, null=True, help_text='Validity')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('event-detail', args=[str(self.id)])

    class Meta:
        db_table = 'events'
        ordering = ['date', 'time']
        verbose_name = 'Event'
        verbose_name_plural = 'Events'
        unique_together = (('name', 'date', 'time'),)


class Share(models.Model):
    id = models.AutoField(primary_key=True)
    event = models.ForeignKey(Event, models.DO_NOTHING, db_column='event', help_text='Event')
    partner = models.ForeignKey(Partner, models.DO_NOTHING, db_column='partner', help_text='Partner')
    attendees = models.IntegerField(default=1, help_text='Attendees')
    payment = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text='Payment')

    def __str__(self):
        return f'{self.event}'

    def get_absolute_url(self):
        return reverse('share-detail', args=[str(self.id)])

    class Meta:
        db_table = 'share'
        ordering = ['-event', 'partner']
        verbose_name = 'Share'
        verbose_name_plural = 'Shares'
        unique_together = (('partner', 'event'),)


class News(models.Model):
    id = models.AutoField(primary_key=True)
    event = models.ForeignKey(Event, models.DO_NOTHING, db_column='event', blank=True, null=True)
    edition = models.DateTimeField(auto_now_add=True)
    brief = models.TextField()
    description = models.TextField()

    def __str__(self):
        return str(self.edition) + ' - ' + self.brief

    def get_absolute_url(self):
        return reverse('news-detail', args=[str(self.id)])

    class Meta:
        db_table = 'news'
        ordering = ['-edition']
        verbose_name = 'News'
        verbose_name_plural = 'News'
