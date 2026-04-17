from django.db import models
from django.urls import reverse


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
