from django.db import models


class Countries(models.Model):
    name = models.CharField(max_length=35)

    class Meta:
        managed = False
        db_table = 'countries'


class States(models.Model):
    name = models.CharField(max_length=35)
    country = models.ForeignKey(Countries, models.DO_NOTHING, db_column='country')

    class Meta:
        managed = False
        db_table = 'states'


class Cities(models.Model):
    name = models.CharField(max_length=35)
    state = models.ForeignKey('States', models.DO_NOTHING, db_column='state')

    class Meta:
        managed = False
        db_table = 'cities'


class Addresses(models.Model):
    address = models.CharField(max_length=30)
    city = models.ForeignKey('Cities', models.DO_NOTHING, db_column='city')
    phone = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'addresses'


class DocTypes(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'doc_types'


class Sexes(models.Model):
    name = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'sexes'


class Persons(models.Model):
    doc_type = models.ForeignKey(DocTypes, models.DO_NOTHING, db_column='doc_type')
    doc_number = models.IntegerField()
    last_name = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    birthdate = models.DateField()
    sex = models.ForeignKey('Sexes', models.DO_NOTHING, db_column='sex')
    address = models.ForeignKey(Addresses, models.DO_NOTHING, db_column='address')
    cellphone = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'persons'


class Positions(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'positions'


class Partners(models.Model):
    person = models.ForeignKey('Persons', models.DO_NOTHING, db_column='person')
    partner_number = models.IntegerField()
    pami_number = models.CharField(max_length=15, blank=True, null=True)
    incorporation = models.DateField()
    position = models.ForeignKey('Positions', models.DO_NOTHING, db_column='position')

    class Meta:
        managed = False
        db_table = 'partners'
