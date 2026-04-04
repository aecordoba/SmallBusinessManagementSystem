from django.db import models
from django.urls import reverse


class Country(models.Model):
    name = models.CharField(unique=True, max_length=35, help_text='Country')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('country-detail', args=[str(self.id)])

    class Meta:
        managed = False
        db_table = 'countries'
        ordering = ['name']
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'


class State(models.Model):
    name = models.CharField(max_length=35, help_text='State')
    country = models.ForeignKey(Country, models.DO_NOTHING, db_column='country', help_text='Country')

    def __str__(self):
        return f'{self.name} - {self.country}'

    def get_absolute_url(self):
        return reverse('state-detail', args=[str(self.id)])


    class Meta:
        managed = False
        db_table = 'states'
        ordering = ['name']
        verbose_name = 'State'
        verbose_name_plural = 'States'
        unique_together = (('name', 'country'),)


class City(models.Model):
    name = models.CharField(max_length=35, help_text='City')
    state = models.ForeignKey(State, models.DO_NOTHING, db_column='state', help_text='State')

    def __str__(self):
        return f'{self.name} - {self.state}'

    def get_absolute_url(self):
        return reverse('city-detail', args=[str(self.id)])

    class Meta:
        managed = False
        db_table = 'cities'
        ordering = ['name']
        verbose_name = 'City'
        verbose_name_plural = 'Cities'
        unique_together = (('name', 'state'),)


class Address(models.Model):
    address = models.CharField(max_length=30, help_text='Address')
    city = models.ForeignKey(City, models.DO_NOTHING, db_column='city', help_text='City')
    phone = models.CharField(max_length=10, blank=True, null=True, help_text='Phone number')

    def __str__(self):
        return f'{self.address} - {self.city}'

    def get_absolute_url(self):
        return reverse('address-detail', args=[str(self.id)])

    class Meta:
        managed = False
        db_table = 'addresses'
        ordering = ['address']
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'


class DocType(models.Model):
    name = models.CharField(unique=True, max_length=20, help_text='Document type')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('doctype-detail', args=[str(self.id)])

    class Meta:
        managed = False
        db_table = 'doc_types'
        ordering = ['name']
        verbose_name = 'Doc Type'
        verbose_name_plural = 'Doc Types'


class Sex(models.Model):
    name = models.CharField(unique=True, max_length=10, help_text='Sex')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('sex-detail', args=[str(self.id)])

    class Meta:
        managed = False
        db_table = 'sexes'
        ordering = ['name']
        verbose_name = 'Sex'
        verbose_name_plural = 'Sexes'


class Person(models.Model):
    doc_type = models.ForeignKey(DocType, models.DO_NOTHING, db_column='doc_type', help_text='Document type')
    doc_number = models.IntegerField(help_text='Document number')
    social_security = models.CharField(unique=True, max_length=15, blank=True, null=True, help_text='Country')
    last_name = models.CharField(max_length=30, help_text='Last name')
    first_name = models.CharField(max_length=30, help_text='First and middle name')
    birthdate = models.DateField(help_text='Birthdate')
    sex = models.ForeignKey(Sex, models.DO_NOTHING, db_column='sex', help_text='Sex')
    address = models.ForeignKey(Address, models.DO_NOTHING, db_column='address', help_text='Address')
    cellphone = models.CharField(max_length=10, blank=True, null=True, help_text='Cell phone number')

    def __str__(self):
        return f'{self.last_name}, {self.first_name} ({self.doc_type} {self.doc_number})'

    def get_absolute_url(self):
        return reverse('person-detail', args=[str(self.id)])

    class Meta:
        managed = False
        db_table = 'persons'
        ordering = ['last_name', 'first_name']
        verbose_name = 'Person'
        verbose_name_plural = 'Persons'
        unique_together = (('doc_type', 'doc_number'),)


class Position(models.Model):
    name = models.CharField(unique=True, max_length=20, help_text='Position')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('position-detail', args=[str(self.id)])

    class Meta:
        managed = False
        db_table = 'positions'
        ordering = ['name']
        verbose_name = 'Position'
        verbose_name_plural = 'Positions'


class PartnerStatus(models.Model):
    name = models.CharField(unique=True, max_length=20)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('partner-status-detail', args=[str(self.id)])

    class Meta:
        managed = False
        db_table = 'partner_status'
        ordering = ['name']
        verbose_name = 'Partner Status'
        verbose_name_plural = 'Partner States'


class Partner(models.Model):
    person = models.ForeignKey(Person, models.DO_NOTHING, db_column='person', help_text='Person')
    partner_number = models.IntegerField(unique=True, help_text='Partner number')
    incorporation = models.DateField(help_text='Incorporation date')
    position = models.ForeignKey(Position, models.DO_NOTHING, db_column='position', help_text='Position')

    def __str__(self):
        return f'{self.partner_number} ({self.person})'

    def get_absolute_url(self):
        return reverse('partner-detail', args=[str(self.id)])

    class Meta:
        managed = False
        db_table = 'partners'
        ordering = ['partner_number']
        verbose_name = 'Partner'
        verbose_name_plural = 'Partners'

