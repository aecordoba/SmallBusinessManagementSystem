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
from django.utils.translation import gettext_lazy as _


class Country(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=35, help_text='Country')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('country-detail', args=[str(self.id)])

    class Meta:
        db_table = 'countries'
        ordering = ['name']
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'


class State(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=35, help_text='State')
    country = models.ForeignKey(Country, models.DO_NOTHING, db_column='country', help_text='Country')

    def __str__(self):
        return f'{self.name} - {self.country}'

    def get_absolute_url(self):
        return reverse('state-detail', args=[str(self.id)])

    class Meta:
        db_table = 'states'
        ordering = ['name']
        verbose_name = 'State'
        verbose_name_plural = 'States'
        unique_together = (('name', 'country'),)


class City(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=35, help_text='City')
    state = models.ForeignKey(State, models.DO_NOTHING, db_column='state', help_text='State')

    def __str__(self):
        return f'{self.name} - {self.state}'

    def get_absolute_url(self):
        return reverse('city-detail', args=[str(self.id)])

    class Meta:
        db_table = 'cities'
        ordering = ['name']
        verbose_name = 'City'
        verbose_name_plural = 'Cities'
        unique_together = (('name', 'state'),)


class Address(models.Model):
    id = models.AutoField(primary_key=True)
    address = models.CharField(max_length=30, help_text='Address')
    zip_code = models.CharField(max_length=8, help_text='ZIP Code')
    city = models.ForeignKey(City, models.DO_NOTHING, db_column='city', help_text='City')
    phone = models.CharField(max_length=10, blank=True, null=True, help_text='Phone number')

    def __str__(self):
        return f'{self.address} - ({self.zip_code}) {self.city}'

    def get_absolute_url(self):
        return reverse('address-detail', args=[str(self.id)])

    class Meta:
        db_table = 'addresses'
        ordering = ['address']
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'


class Person(models.Model):

    DOCUMENTS = (
        ('document_1', _('document_1')),
        ('document_2', _('document_2')),
        ('document_3', _('document_3'))
    )

    GENDERS = (
        ('male', _('male')),
        ('female', _('female')),
        ('other', _('other'))
    )

    id = models.AutoField(primary_key=True)
    doc_type = models.CharField(max_length=20, choices=DOCUMENTS, default='document_1')
    doc_number = models.IntegerField(help_text='Document number')
    social_security = models.CharField(unique=True, max_length=15, blank=True, null=True, help_text='Social Security')
    last_name = models.CharField(max_length=30, help_text='Last name')
    first_name = models.CharField(max_length=30, help_text='First and middle name')
    email = models.EmailField(blank=True, null=True)
    birthdate = models.DateField(help_text='Birthdate')
    gender = models.CharField(max_length=15, choices=GENDERS)
    address = models.ForeignKey(Address, models.DO_NOTHING, db_column='address', help_text='Address')
    cellphone = models.CharField(max_length=10, blank=True, null=True, help_text='Cell phone number')

    def __str__(self):
        return f'{self.last_name}, {self.first_name} - {_(self.doc_type)} {self.doc_number}'

    def get_absolute_url(self):
        return reverse('person-detail', args=[str(self.id)])

    class Meta:
        db_table = 'persons'
        ordering = ['last_name', 'first_name']
        verbose_name = 'Person'
        verbose_name_plural = 'Persons'
        unique_together = (('doc_type', 'doc_number'),)


class Partner(models.Model):
    POSITIONS = (
        ('position_1', _('position_1')),
        ('position_2', _('position_2')),
        ('position_3', _('position_3')),
        ('position_4', _('position_4'))
    )

    STATUS = (
        ('status_1', _('status_1')),
        ('status_2', _('status_2')),
        ('status_3', _('status_3'))
    )

    id = models.AutoField(primary_key=True)
    person = models.ForeignKey(Person, models.DO_NOTHING, db_column='person', help_text='Person')
    partner_number = models.IntegerField(unique=True, help_text='Partner number')
    incorporation = models.DateField(help_text='Incorporation date')
    position = models.CharField(max_length=15, choices=POSITIONS, default='position_1')
    status = models.CharField(max_length=15, choices=STATUS, default='status_1')

    def __str__(self):
        return f'{self.partner_number} - {self.person.last_name}, {self.person.first_name}'

    def get_absolute_url(self):
        return reverse('partner-detail', args=[str(self.id)])

    class Meta:
        db_table = 'partners'
        ordering = ['partner_number']
        verbose_name = 'Partner'
        verbose_name_plural = 'Partners'
        permissions = (("management", "Can manage the system"),)
