from django.db import models
from django.urls import reverse
from partners.models import Partner


class Event(models.Model):
    name = models.CharField(max_length=30, help_text='Event title')
    date = models.DateField(help_text='Event date')
    time = models.TimeField(blank=True, null=True, help_text='Event time')
    creation = models.DateTimeField(help_text='Creation date')
    description = models.TextField(blank=True, null=True, help_text='Event description')
    charge = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text='Event charge')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('event-detail', args=[str(self.id)])

    class Meta:
        managed = False
        db_table = 'events'
        ordering = ['-date', '-time']
        verbose_name = 'Event'
        verbose_name_plural = 'Events'


class Share(models.Model):
    event = models.ForeignKey(Event, models.DO_NOTHING, db_column='event', help_text='Event')
    partner = models.ForeignKey(Partner, models.DO_NOTHING, db_column='partner', help_text='Partner')
    attendees = models.IntegerField(blank=True, null=True, help_text='Attendees')
    payment = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text='Payment')

    def __str__(self):
        return f'{self.event}'

    def get_absolute_url(self):
        return reverse('share-detail', args=[str(self.id)])

    class Meta:
        managed = False
        db_table = 'share'
        ordering = ['-event', 'partner']
        verbose_name = 'Share'
        verbose_name_plural = 'Shares'


class Accounting(models.Model):
    date = models.DateField(help_text='Date')
    concept = models.CharField(max_length=30, help_text='Concept')
    description = models.TextField(blank=True, null=True, help_text='Concept detail')
    debit = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True, help_text='Debit')
    credit = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True, help_text='Credit')


    def __str__(self):
        return str(self.date) + ' ' + self.concept

    def get_absolute_url(self):
        return reverse('accounting-detail', args=[str(self.id)])

    class Meta:
        managed = False
        db_table = 'accounting'
        ordering = ['-date', 'concept']
        verbose_name = 'Accounting'
        verbose_name_plural = 'Accounting'
