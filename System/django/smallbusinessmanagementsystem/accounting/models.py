from django.db import models
from partners.models import Partners


class Events(models.Model):
    name = models.CharField(max_length=30)
    date = models.DateField()
    time = models.TimeField(blank=True, null=True)
    creation = models.DateTimeField()
    description = models.TextField(blank=True, null=True)
    charge = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'events'


class Share(models.Model):
    event = models.ForeignKey(Events, models.DO_NOTHING, db_column='event')
    partner = models.ForeignKey(Partners, models.DO_NOTHING, db_column='partner')
    attendees = models.IntegerField(blank=True, null=True)
    payment = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'share'


class Accounting(models.Model):
    date = models.DateField()
    concept = models.CharField(max_length=30)
    description = models.TextField(blank=True, null=True)
    debit = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    credit = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'accounting'

