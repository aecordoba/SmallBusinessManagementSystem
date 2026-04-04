from django.contrib import admin
from .models import Address, City, Country, DocType, Partner, Person, Position, Sex, State


@admin.register(Country)
class CountriesAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(State)
class StatesAdmin(admin.ModelAdmin):
    list_display = ('name', 'country')


@admin.register(City)
class CitiesAdmin(admin.ModelAdmin):
    list_display = ('name', 'state')


@admin.register(Address)
class AddressesAdmin(admin.ModelAdmin):
    list_display = ('address', 'city', 'phone')


@admin.register(DocType)
class DocTypesAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Sex)
class SexesAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Person)
class PersonsAdmin(admin.ModelAdmin):
    list_display = ('doc_type', 'doc_number', 'social_security', 'last_name', 'first_name', 'birthdate', 'sex', 'address', 'cellphone')


@admin.register(Position)
class PositionsAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Partner)
class PartnersAdmin(admin.ModelAdmin):
    list_display = ('person', 'partner_number', 'incorporation', 'position')



