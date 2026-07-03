#  		test_forms.py			Jun 20, 2026
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

from django.test import TestCase
from partners.models import Country, State, City, Address, Person, Partner
from users.forms import UserForm
import random
import string


def generate_random_string(lenght):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=lenght))


class UserFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        country = Country.objects.create(name='Country_1')
        state = State.objects.create(name='State_1', country=country)
        city = City.objects.create(name='City_1', state=state)
        address = Address.objects.create(address='Address_1', zip_code='000001', city=city, phone='55550001')
        person = Person.objects.create(identification='identification_1', id_number=10000001,
                                       social_security='100000/01', last_name='Last_name_1',
                                       first_name='First_name_1 Middle_name_1', email='last_name_1@mail.com',
                                       birthdate='1960-01-01', gender='male', address=address, cellphone='0015550001')
        cls.partner = Partner.objects.create(person=person, partner_number=10001, incorporation='2026-01-01',
                                             position='psition_1', status='status_1')

    def test_partner_number_label(self):
        form = UserForm()
        self.assertEqual(form.fields['name'].label, 'Name')

    def test_first_name_label(self):
        form = UserForm()
        self.assertEqual(form.fields['partner'].label, 'Partner')

    def test_last_name_label(self):
        form = UserForm()
        self.assertEqual(form.fields['is_active'].label, 'Active')

    def test_doc_type_label(self):
        form = UserForm()
        self.assertEqual(form.fields['is_staff'].label, 'Staff')

    def test_name_min_lenght(self):
        data = {'name': 'name', 'partner': self.partner, 'is_active': True, 'is_staff': False}
        form = UserForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
        self.assertEqual(form.errors['name'], ['The name must be between 5 and 30 characters long.'])

    def test_name_max_lenght(self):
        data = {'name': generate_random_string(31), 'partner': self.partner, 'is_active': True, 'is_staff': False}
        form = UserForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
        self.assertEqual(form.errors['name'], ['The name must be between 5 and 30 characters long.'])
