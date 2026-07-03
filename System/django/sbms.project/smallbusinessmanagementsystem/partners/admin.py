#  		admin.py			Jun 20, 2026
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
    list_display = ('identification', 'id_number', 'social_security', 'last_name', 'first_name', 'email', 'birthdate',
                    'gender', 'address', 'cellphone')


@admin.register(Partner)
class PartnersAdmin(admin.ModelAdmin):
    list_display = ('person', 'partner_number', 'incorporation', 'position')
