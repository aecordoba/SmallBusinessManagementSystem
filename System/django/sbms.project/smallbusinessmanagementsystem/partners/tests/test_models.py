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
from django.utils.translation import gettext_lazy as _


class PartnerModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        country = Country.objects.create(name='Country_1')
        state = State.objects.create(name='State_1', country=country)
        city = City.objects.create(name='City_1', state=state)
        address = Address.objects.create(address='Address_1', zip_code='000001', city=city, phone='55550001')
        person = Person.objects.create(doc_type='document_1', doc_number=10000001, social_security='100000/01',
                                       last_name='Last_name_1', first_name='First_Name_1 Middle_Name_1',
                                       email='last_name_1@mail.com', birthdate='1960-01-01', gender='male',
                                       address=address, cellphone='0015550001')
        Partner.objects.create(person=person, partner_number=10001, incorporation='2026-01-01', position='psition_1',
                               status='status_1')

    def test_doc_type_label(self):
        person = Person.objects.get(id=1)
        field_label = person._meta.get_field('doc_type').verbose_name
        self.assertEqual(field_label, 'Document type')

    def test_doc_number_label(self):
        person = Person.objects.get(id=1)
        field_label = person._meta.get_field('doc_number').verbose_name
        self.assertEqual(field_label, 'Document number')

    def test_social_security_label(self):
        person = Person.objects.get(id=1)
        field_label = person._meta.get_field('social_security').verbose_name
        self.assertEqual(field_label, 'Social Security')

    def test_country_name_max_length(self):
        country = Country.objects.get(id=1)
        max_length = country._meta.get_field('name').max_length
        self.assertEqual(max_length, 35)

    def test_state_name_max_length(self):
        state = State.objects.get(id=1)
        max_length = state._meta.get_field('name').max_length
        self.assertEqual(max_length, 35)

    def test_city_name_max_length(self):
        city = City.objects.get(id=1)
        max_length = city._meta.get_field('name').max_length
        self.assertEqual(max_length, 35)

    def test_person_str(self):
        person = Person.objects.get(id=1)
        expected_str = f'{person.last_name}, {person.first_name} - {_(person.doc_type)} {person.doc_number}'
        self.assertEqual(str(person), expected_str)

    def test_partner_str(self):
        partner = Partner.objects.get(id=1)
        expected_str = f'{partner.partner_number} - {partner.person.last_name}, {partner.person.first_name}'
        self.assertEqual(str(partner), expected_str)

    def test_person_get_absolute_url(self):
        person = Person.objects.get(id=1)
        self.assertEqual(person.get_absolute_url(), '/person/1')

    def test_partner_get_absolute_url(self):
        partner = Partner.objects.get(id=1)
        self.assertEqual(partner.get_absolute_url(), '/partner/1')
