from django.contrib import admin
from .models import Address, City, Country, Partner, Person, State


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
    list_display = ('address', 'zip_code', 'city', 'phone')


@admin.register(Person)
class PersonsAdmin(admin.ModelAdmin):
    list_display = ('doc_type', 'doc_number', 'social_security', 'last_name', 'first_name', 'email', 'birthdate', 'gender', 'address', 'cellphone')


@admin.register(Partner)
class PartnersAdmin(admin.ModelAdmin):
    list_display = ('person', 'partner_number', 'incorporation', 'position')
