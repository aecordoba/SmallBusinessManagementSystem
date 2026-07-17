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
from partners.forms import PartnerForm
import random
import string
import datetime

from partners.models import Country, State, City


def generate_random_string(lenght):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=lenght))


class PartnerFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        country = Country.objects.create(name='Country_1')
        state = State.objects.create(name='State_1', country=country)
        cls.city = City.objects.create(name='City_1', state=state)

    def test_partner_number_label(self):
        form = PartnerForm()
        self.assertEqual(form.fields['partner_number'].label, 'Partner number')

    def test_first_name_label(self):
        form = PartnerForm()
        self.assertEqual(form.fields['first_name'].label, 'First name')

    def test_last_name_label(self):
        form = PartnerForm()
        self.assertEqual(form.fields['last_name'].label, 'Last name')

    def test_doc_type_label(self):
        form = PartnerForm()
        self.assertEqual(form.fields['identification'].label, 'Identification')

    def test_doc_number_label(self):
        form = PartnerForm()
        self.assertEqual(form.fields['id_number'].label, 'Number')

    def test_social_security_label(self):
        form = PartnerForm()
        self.assertEqual(form.fields['social_security'].label, 'Social Security')

    def test_email_label(self):
        form = PartnerForm()
        self.assertEqual(form.fields['email'].label, 'E-mail')

    def test_birthdate_label(self):
        form = PartnerForm()
        self.assertEqual(form.fields['birthdate'].label, 'Birthdate')

    def test_gender_label(self):
        form = PartnerForm()
        self.assertEqual(form.fields['gender'].label, 'Gender')

    def test_address_label(self):
        form = PartnerForm()
        self.assertEqual(form.fields['address'].label, 'Address')

    def test_zip_code_label(self):
        form = PartnerForm()
        self.assertEqual(form.fields['zip_code'].label, 'ZIP Code')

    def test_city_label(self):
        form = PartnerForm()
        self.assertEqual(form.fields['city'].label, 'City')

    def test_phone_label(self):
        form = PartnerForm()
        self.assertEqual(form.fields['phone'].label, 'Phone number')

    def test_cellphone_label(self):
        form = PartnerForm()
        self.assertEqual(form.fields['cellphone'].label, 'Cell phone number')

    def test_incorporation_label(self):
        form = PartnerForm()
        self.assertEqual(form.fields['incorporation'].label, 'Incorporation')

    def test_position_label(self):
        form = PartnerForm()
        self.assertEqual(form.fields['position'].label, 'Position')

    def test_status_label(self):
        form = PartnerForm()
        self.assertEqual(form.fields['status'].label, 'Status')

    def test_first_name_min_lenght(self):
        data = {'partner_number': 10001, 'first_name': 'F', 'last_name': 'Last_name_1',
                'identification': 'identification_1', 'id_number': 10000001, 'social_security': '100000/01',
                'email': 'last_name_1@mail.com', 'birthdate': '1960-01-01', 'gender': 'male', 'address': 'Address_1',
                'zip_code': '000001', 'city': self.city, 'phone': '55550001', 'cellphone': '0015550001',
                'incorporation': '2026-01-01', 'position': 'position_1', 'status': 'status_1'}
        form = PartnerForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn('first_name', form.errors)
        self.assertEqual(form.errors['first_name'], ['The first name must be between 2 and 30 characters long.'])

    def test_first_name_max_lenght(self):
        data = {'partner_number': 10001, 'first_name': generate_random_string(31), 'last_name': 'Last_name_1',
                'identification': 'identification_1', 'id_number': 10000001, 'social_security': '100000/01',
                'email': 'last_name_1@mail.com', 'birthdate': '1960-01-01', 'gender': 'male', 'address': 'Address_1',
                'zip_code': '000001', 'city': self.city, 'phone': '55550001', 'cellphone': '0015550001',
                'incorporation': '2026-01-01', 'position': 'position_1', 'status': 'status_1'}
        form = PartnerForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn('first_name', form.errors)
        self.assertEqual(form.errors['first_name'], ['The first name must be between 2 and 30 characters long.'])

    def test_last_name_min_lenght(self):
        data = {'partner_number': 10001, 'first_name': 'First_name_1 Middle_name_1', 'last_name': 'L',
                'identification': 'identification_1', 'id_number': 10000001, 'social_security': '100000/01',
                'email': 'last_name_1@mail.com', 'birthdate': '1960-01-01', 'gender': 'male', 'address': 'Address_1',
                'zip_code': '000001', 'city': self.city, 'phone': '55550001', 'cellphone': '0015550001',
                'incorporation': '2026-01-01', 'position': 'position_1', 'status': 'status_1'}
        form = PartnerForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn('last_name', form.errors)
        self.assertEqual(form.errors['last_name'], ['The last name must be between 2 and 30 characters long.'])

    def test_last_name_max_lenght(self):
        data = {'partner_number': 10001, 'first_name': 'First_name_1 Middle_name_1',
                'last_name': generate_random_string(31), 'identification': 'identification_1',
                'id_number': 10000001, 'social_security': '100000/01', 'email': 'last_name_1@mail.com',
                'birthdate': '1960-01-01', 'gender': 'male', 'address': 'Address_1', 'zip_code': '000001',
                'city': self.city, 'phone': '55550001', 'cellphone': '0015550001', 'incorporation': '2026-01-01',
                'position': 'position_1', 'status': 'status_1'}
        form = PartnerForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn('last_name', form.errors)
        self.assertEqual(form.errors['last_name'], ['The last name must be between 2 and 30 characters long.'])

    def test_id_number_min_value(self):
        data = {'partner_number': 10001, 'first_name': 'First_name_1 Middle_name_1', 'last_name': 'Last_name_1',
                'identification': 'identification_1', 'id_number': 999999, 'social_security': '100000/01',
                'email': 'last_name_1@mail.com', 'birthdate': '1960-01-01', 'gender': 'male', 'address': 'Address_1',
                'zip_code': '000001', 'city': self.city, 'phone': '55550001', 'cellphone': '0015550001',
                'incorporation': '2026-01-01', 'position': 'position_1', 'status': 'status_1'}
        form = PartnerForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn('id_number', form.errors)
        self.assertEqual(form.errors['id_number'], ['Incorrect ID number.'])

    def test_social_security_min_lenght(self):
        data = {'partner_number': 10001, 'first_name': 'First_name_1 Middle_name_1', 'last_name': 'Last_name_1',
                'identification': 'identification_1', 'id_number': 10000001,
                'social_security': generate_random_string(16), 'email': 'last_name_1@mail.com',
                'birthdate': '1960-01-01', 'gender': 'male', 'address': 'Address_1', 'zip_code': '000001',
                'city': self.city, 'phone': '55550001', 'cellphone': '0015550001', 'incorporation': '2026-01-01',
                'position': 'position_1', 'status': 'status_1'}
        form = PartnerForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn('social_security', form.errors)
        self.assertEqual(form.errors['social_security'],
                         ['The social security number must be up to 15 characters long.'])

    def test_birthdate_in_past(self):
        data = {'partner_number': 10001, 'first_name': 'First_name_1 Middle_name_1', 'last_name': 'Last_name_1',
                'identification': 'identification_1', 'id_number': 10000001, 'social_security': '100000/01',
                'email': 'last_name_1@mail.com', 'birthdate': datetime.date.today(), 'gender': 'male',
                'address': 'Address_1', 'zip_code': '000001', 'city': self.city, 'phone': '55550001',
                'cellphone': '0015550001', 'incorporation': '2026-01-01', 'position': 'position_1', 'status': 'status_1'
                }
        form = PartnerForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn('birthdate', form.errors)
        self.assertEqual(form.errors['birthdate'], ['Incorrect birthdate.'])

    def test_address_min_lenght(self):
        data = {'partner_number': 10001, 'first_name': 'First_name_1 Middle_name_1', 'last_name': 'Last_name_1',
                'identification': 'identification_1', 'id_number': 10000001, 'social_security': '100000/01',
                'email': 'last_name_1@mail.com', 'birthdate': '1960-01-01', 'gender': 'male', 'address': 'Addr',
                'zip_code': '000001', 'city': self.city, 'phone': '55550001', 'cellphone': '0015550001',
                'incorporation': '2026-01-01', 'position': 'position_1', 'status': 'status_1'}
        form = PartnerForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn('address', form.errors)
        self.assertEqual(form.errors['address'], ['The address must be between 5 and 30 characters long.'])

    def test_address_max_lenght(self):
        data = {'partner_number': 10001, 'first_name': 'First_name_1 Middle_name_1',
                'last_name': 'Last_name_1', 'identification': 'identification_1',
                'id_number': 10000001, 'social_security': '100000/01', 'email': 'last_name_1@mail.com',
                'birthdate': '1960-01-01', 'gender': 'male', 'address': generate_random_string(31),
                'zip_code': '000001', 'city': self.city, 'phone': '55550001', 'cellphone': '0015550001',
                'incorporation': '2026-01-01', 'position': 'position_1', 'status': 'status_1'}
        form = PartnerForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn('address', form.errors)
        self.assertEqual(form.errors['address'], ['The address must be between 5 and 30 characters long.'])

    def test_phone_empty(self):
        data = {'partner_number': 10001, 'first_name': 'First_name_1 Middle_name_1', 'last_name': 'Last_name_1',
                'identification': 'identification_1', 'id_number': 10000001, 'social_security': '100000/01',
                'email': 'last_name_1@mail.com', 'birthdate': '1960-01-01', 'gender': 'male', 'address': 'Address_1',
                'zip_code': '000001', 'city': self.city, 'phone': '', 'cellphone': '0015550001',
                'incorporation': '2026-01-01', 'position': 'position_1', 'status': 'status_1'}
        form = PartnerForm(data)
        self.assertTrue(form.is_valid())

    def test_phone_min_lenght(self):
        data = {'partner_number': 10001, 'first_name': 'First_name_1 Middle_name_1', 'last_name': 'Last_name_1',
                'identification': 'identification_1', 'id_number': 10000001, 'social_security': '100000/01',
                'email': 'last_name_1@mail.com', 'birthdate': '1960-01-01', 'gender': 'male', 'address': 'Address_1',
                'zip_code': '000001', 'city': self.city, 'phone': '5555001', 'cellphone': '0015550001',
                'incorporation': '2026-01-01', 'position': 'position_1', 'status': 'status_1'}
        form = PartnerForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn('phone', form.errors)
        self.assertEqual(form.errors['phone'],
                         ['The phone number must be between 8 and 10 digits long (without hyphens).'])

    def test_phone_max_lenght(self):
        data = {'partner_number': 10001, 'first_name': 'First_name_1 Middle_name_1',
                'last_name': 'Last_name_1', 'identification': 'identification_1',
                'id_number': 10000001, 'social_security': '100000/01', 'email': 'last_name_1@mail.com',
                'birthdate': '1960-01-01', 'gender': 'male', 'address': 'Address_1', 'zip_code': '000001',
                'city': self.city, 'phone': generate_random_string(11), 'cellphone': '0015550001',
                'incorporation': '2026-01-01', 'position': 'position_1', 'status': 'status_1'}
        form = PartnerForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn('phone', form.errors)
        self.assertEqual(form.errors['phone'],
                         ['The phone number must be between 8 and 10 digits long (without hyphens).'])

    def test_cellphone_empty(self):
        data = {'partner_number': 10001, 'first_name': 'First_name_1 Middle_name_1', 'last_name': 'Last_name_1',
                'identification': 'identification_1', 'id_number': 10000001, 'social_security': '100000/01',
                'email': 'last_name_1@mail.com', 'birthdate': '1960-01-01', 'gender': 'male', 'address': 'Address_1',
                'zip_code': '000001', 'city': self.city, 'phone': '55550001', 'cellphone': '',
                'incorporation': '2026-01-01', 'position': 'position_1', 'status': 'status_1'}
        form = PartnerForm(data)
        self.assertTrue(form.is_valid())

    def test_cellphone_min_lenght(self):
        data = {'partner_number': 10001, 'first_name': 'First_name_1 Middle_name_1', 'last_name': 'Last_name_1',
                'identification': 'identification_1', 'id_number': 10000001, 'social_security': '100000/01',
                'email': 'last_name_1@mail.com', 'birthdate': '1960-01-01', 'gender': 'male', 'address': 'Address_1',
                'zip_code': '000001', 'city': self.city, 'phone': '55550001', 'cellphone': '0015551',
                'incorporation': '2026-01-01', 'position': 'position_1', 'status': 'status_1'}
        form = PartnerForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn('cellphone', form.errors)
        self.assertEqual(form.errors['cellphone'],
                         ['The cell phone number must be between 8 and 10 digits long (without hyphens).'])

    def test_cellphone_max_lenght(self):
        data = {'partner_number': 10001, 'first_name': 'First_name_1 Middle_name_1',
                'last_name': 'Last_name_1', 'identification': 'identification_1',
                'id_number': 10000001, 'social_security': '100000/01', 'email': 'last_name_1@mail.com',
                'birthdate': '1960-01-01', 'gender': 'male', 'address': 'Address_1', 'zip_code': '000001',
                'city': self.city, 'phone': '55550001', 'cellphone': generate_random_string(11),
                'incorporation': '2026-01-01', 'position': 'position_1', 'status': 'status_1'}
        form = PartnerForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn('cellphone', form.errors)
        self.assertEqual(form.errors['cellphone'],
                         ['The cell phone number must be between 8 and 10 digits long (without hyphens).'])
