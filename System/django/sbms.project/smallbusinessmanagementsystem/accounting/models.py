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


class Accounting(models.Model):
    id = models.AutoField(primary_key=True)
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
        db_table = 'accounting'
        ordering = ['-date', 'concept']
        verbose_name = 'Accounting'
        verbose_name_plural = 'Accounting'
