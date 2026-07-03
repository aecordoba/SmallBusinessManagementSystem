#  		test_models.py			Jun 20, 2026
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
from users.models import User


class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        country = Country.objects.create(name='Country_1')
        state = State.objects.create(name='State_1', country=country)
        city = City.objects.create(name='City_1', state=state)
        address = Address.objects.create(address='Address_1', zip_code='000001', city=city, phone='55550001')
        person = Person.objects.create(identification='identification_1', id_number=10000001,
                                       social_security='100000/01', last_name='Last_name_1',
                                       first_name='First_Name_1 Middle_Name_1', email='last_name_1@mail.com',
                                       birthdate='1960-01-01', gender='male', address=address, cellphone='0015550001')
        partner = Partner.objects.create(person=person, partner_number=10001, incorporation='2026-01-01',
                                         position='psition_1', status='status_1')

        User.objects.create(name='User_1', partner=partner, is_active=True, is_staff=False)

    def test_name_label(self):
        user = User.objects.get(id=1)
        field_label = user._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'Username')

    def test_name_max_length(self):
        user = User.objects.get(id=1)
        max_length = user._meta.get_field('name').max_length
        self.assertEqual(max_length, 30)

    def test_is_active_default(self):
        user = User.objects.get(id=1)
        default = user._meta.get_field('is_active').default
        self.assertTrue(default)

    def test_is_staff_default(self):
        user = User.objects.get(id=1)
        default = user._meta.get_field('is_staff').default
        self.assertFalse(default)

    def test_user_str(self):
        user = User.objects.get(id=1)
        expected_str = user.name
        self.assertEqual(str(user), expected_str)

    def test_user_get_absolute_url(self):
        user = User.objects.get(id=1)
        self.assertEqual(user.get_absolute_url(), '/users/1')
