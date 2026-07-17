#  		test_views.py			Jun 20, 2026
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

from datetime import date, timedelta
from django.contrib.auth.models import Permission
from django.test import TestCase
from django.urls import reverse
from accounting.models import Accounting
from partners.models import Country, State, City, Address, Person, Partner
from users.models import User


class AccountingAdditionTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Persons
        country = Country.objects.create(name='Country_1')
        state = State.objects.create(name='State_1', country=country)
        city = City.objects.create(name='City_1', state=state)
        address = Address.objects.create(address='Address_1', zip_code='000001', city=city, phone='55550001')
        person_1 = Person.objects.create(identification='identification_1', id_number=10000001,
                                         social_security='100000/01', last_name='Last_name_1',
                                         first_name='First_name_1 Middle_name_1', email='last_name_1@mail.com',
                                         birthdate='1960-01-01', gender='male', address=address, cellphone='0015550001')
        person_2 = Person.objects.create(identification='identification_1', id_number=10000002,
                                         social_security='100000/02', last_name='Last_name_2',
                                         first_name='First_name_2 Middle_name_2', email='last_name_2@mail.com',
                                         birthdate='1960-01-02', gender='male', address=address, cellphone='0015550002')
        # Partners
        partner_1 = Partner.objects.create(person=person_1, partner_number=10001, incorporation='2026-01-01',
                                           position='position_1', status='status_1')
        partner_2 = Partner.objects.create(person=person_2, partner_number=10002, incorporation='2026-01-02',
                                           position='position_1', status='status_1')
        # Users
        staff_user = User.objects.create_user(name='staff_user', partner=partner_1, password='password_1')
        User.objects.create_user(name='user', partner=partner_2, password='password_1')
        permission = Permission.objects.get(codename='add_accounting')
        staff_user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='view_accounting')
        staff_user.user_permissions.add(permission)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('add-accounting'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/accounting/add/')

    def test_logged_in_forbiden_resource(self):
        self.client.login(username='user', password='password_1')
        response = self.client.get(reverse('add-accounting'))
        self.assertEqual(response.status_code, 403)

    def test_logged_in_user_get_correct_template(self):
        self.client.login(username='staff_user', password='password_1')
        response = self.client.get(reverse('add-accounting'))
        self.assertEqual(str(response.context['user']), 'staff_user')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounting/add_accounting.html')

    def test_post_accounting_saved(self):
        self.client.login(username='staff_user', password='password_1')
        data = {'date': date.today(), 'concept': 'Concept_1', 'description': 'Description_1', 'credit': 10000000}
        response = self.client.post(reverse('add-accounting'), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('accounting'))
        self.assertEqual(Accounting.objects.count(), 1)


class AccountingListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Persons
        country = Country.objects.create(name='Country_1')
        state = State.objects.create(name='State_1', country=country)
        city = City.objects.create(name='City_1', state=state)
        address = Address.objects.create(address='Address_1', zip_code='000001', city=city, phone='55550001')
        person_1 = Person.objects.create(identification='identification_1', id_number=10000001,
                                         social_security='100000/01', last_name='Last_name_1',
                                         first_name='First_name_1 Middle_name_1', email='last_name_1@mail.com',
                                         birthdate='1960-01-01', gender='male', address=address, cellphone='0015550001')
        person_2 = Person.objects.create(identification='identification_1', id_number=10000002,
                                         social_security='100000/02', last_name='Last_name_2',
                                         first_name='First_name_2 Middle_name_2', email='last_name_2@mail.com',
                                         birthdate='1960-01-02', gender='male', address=address, cellphone='0015550002')
        # Partners
        partner_1 = Partner.objects.create(person=person_1, partner_number=10001, incorporation='2026-01-01',
                                           position='position_1', status='status_1')
        partner_2 = Partner.objects.create(person=person_2, partner_number=10002, incorporation='2026-01-02',
                                           position='position_1', status='status_1')
        # Users
        staff_user = User.objects.create_user(name='staff_user', partner=partner_1, password='password_1')
        User.objects.create_user(name='user', partner=partner_2, password='password_1')
        permission = Permission.objects.get(codename='view_accounting')
        staff_user.user_permissions.add(permission)
        # Accounting
        for index in range(15):
            suffix = f'{index:02d}'
            Accounting.objects.create(date=date.today() - timedelta(days=15 - index), concept='Concept_' + suffix,
                                      description='Description_' + suffix, credit=1000000 + index * 100)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('accounting'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/accounting/')

    def test_logged_in_forbiden_resource(self):
        self.client.login(username='user', password='password_1')
        response = self.client.get(reverse('accounting'))
        self.assertEqual(response.status_code, 403)

    def test_view_url_exists_at_desired_location(self):
        self.client.login(username='staff_user', password='password_1')
        response = self.client.get('/accounting/')
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(username='staff_user', password='password_1')
        response = self.client.get(reverse('accounting'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounting/accounting_list.html')

    def test_pagination_is_ten(self):
        self.client.login(username='staff_user', password='password_1')
        response = self.client.get(reverse('accounting'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'])
        self.assertEqual(len(response.context['accounting_list']), 10)

    def test_lists_all_accounting(self):
        self.client.login(username='staff_user', password='password_1')
        response = self.client.get(reverse('accounting') + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'])
        self.assertEqual(len(response.context['accounting_list']), 5)
