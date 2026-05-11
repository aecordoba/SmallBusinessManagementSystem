from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


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
    zip_code = models.CharField(max_length=8, help_text='ZIP Code')
    city = models.ForeignKey(City, models.DO_NOTHING, db_column='city', help_text='City')
    phone = models.CharField(max_length=10, blank=True, null=True, help_text='Phone number')

    def __str__(self):
        return f'{self.address} - ({self.zip_code}) {self.city}'

    def get_absolute_url(self):
        return reverse('address-detail', args=[str(self.id)])

    class Meta:
        managed = False
        db_table = 'addresses'
        ordering = ['address']
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'


class Person(models.Model):
    class Documents(models.TextChoices):
        DOCUMENT_1 = 'document_1', _('document_1')
        DOCUMENT_2 = 'document_2', _('document_2')
        DOCUMENT_3 = 'document_3', _('document_3')

    class Genders(models.TextChoices):
        MALE = 'male', _('male')
        FEMALE = 'female', _('female')
        OTHER = 'other', _('other')

    doc_type = models.CharField(max_length=20, choices=Documents.choices, default=Documents.DOCUMENT_1)
    doc_number = models.IntegerField(help_text='Document number')
    social_security = models.CharField(unique=True, max_length=15, blank=True, null=True, help_text='Social Security')
    last_name = models.CharField(max_length=30, help_text='Last name')
    first_name = models.CharField(max_length=30, help_text='First and middle name')
    email = models.EmailField(blank=True, null=True)
    birthdate = models.DateField(help_text='Birthdate')
    gender = models.CharField(max_length=15, choices=Genders.choices)
    address = models.ForeignKey(Address, models.DO_NOTHING, db_column='address', help_text='Address')
    cellphone = models.CharField(max_length=10, blank=True, null=True, help_text='Cell phone number')

    def __str__(self):
        return f'{self.last_name}, {self.first_name} - {_(self.doc_type)} {self.doc_number}'

    def get_absolute_url(self):
        return reverse('person-detail', args=[str(self.id)])

    class Meta:
        managed = False
        db_table = 'persons'
        ordering = ['last_name', 'first_name']
        verbose_name = 'Person'
        verbose_name_plural = 'Persons'
        unique_together = (('doc_type', 'doc_number'),)


class Partner(models.Model):
    class Positions(models.TextChoices):
        POSITION_1 = 'position_1', _('position_1')
        POSITION_2 = 'position_2', _('position_2')
        POSITION_3 = 'position_3', _('position_3')
        POSITION_4 = 'position_4', _('position_4')

    class Status(models.TextChoices):
        STATUS_1 = 'status_1', _('status_1')
        STATUS_2 = 'status_2', _('status_2')
        STATUS_3 = 'status_3', _('status_3')

    person = models.ForeignKey(Person, models.DO_NOTHING, db_column='person', help_text='Person')
    partner_number = models.IntegerField(unique=True, help_text='Partner number')
    incorporation = models.DateField(help_text='Incorporation date')
    position = models.CharField(max_length=15, choices=Positions.choices, default=Positions.POSITION_1)
    status = models.CharField(max_length=15, choices=Status.choices, default=Status.STATUS_1)

    def __str__(self):
        return f'{self.partner_number} - {self.person}'

    def get_absolute_url(self):
        return reverse('partner-detail', args=[str(self.id)])

    class Meta:
        managed = False
        db_table = 'partners'
        ordering = ['partner_number']
        verbose_name = 'Partner'
        verbose_name_plural = 'Partners'
        permissions = (("management", "Can manage the system"),)

