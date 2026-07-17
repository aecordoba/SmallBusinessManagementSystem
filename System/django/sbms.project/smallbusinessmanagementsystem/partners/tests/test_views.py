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

from datetime import date, timedelta, datetime
from django.contrib.auth.models import Permission
from django.test import TestCase
from django.urls import reverse
from events.models import News, Event, Share
from partners.models import Country, State, City, Address, Person, Partner
from users.models import User


class IndexViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.partners_quantity = 2
        cls.news_quantity = 5

        country = Country.objects.create(name='Country_1')
        state = State.objects.create(name='State_1', country=country)
        city = City.objects.create(name='City_1', state=state)
        address = Address.objects.create(address='Address_1', zip_code='000001', city=city, phone='55550001')
        for partner_id in range(cls.partners_quantity):
            person = Person.objects.create(identification='identification_1', id_number=10000000 + partner_id,
                                           social_security=f'100000/{partner_id}', last_name=f'Last_name_{partner_id}',
                                           first_name=f'First_name_{partner_id} Middle_name_{partner_id}',
                                           email=f'last_name_{partner_id}@mail.com', birthdate='1960-01-01',
                                           gender='male', address=address, cellphone='0015550001')
            Partner.objects.create(person=person, partner_number=1000 + partner_id, incorporation='2026-01-01',
                                   position='psition_1', status='status_1')

        for news_id in range(cls.news_quantity):
            News.objects.create(edition=datetime.now() + timedelta(days=news_id),
                                brief=f'News_{news_id}', description=f'News_{news_id} description.')

    def test_index_url_exists_at_desired_location(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_index_accessible_by_name(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_idex_uses_correct_template(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_index_receives_correct_partners_quantity(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.context['partners_quantity'], IndexViewTest.partners_quantity)

    def test_index_receives_correct_news_quantity(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(len(response.context['aside_list']), 3)


class PartnerCreationTest(TestCase):
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
        permission = Permission.objects.get(codename='add_partner')
        staff_user.user_permissions.add(permission)
        # Events
        today = date.today()
        Event.objects.create(name='Past_Weekly_event_1', date=today - timedelta(days=(today.isoweekday() % 7) + 7),
                             description='Past weekly event 1 description', charge=1000, automatic=True,
                             validity='weekly')
        Event.objects.create(name='Past_Monthly_event_1',
                             date=(today.replace(day=1) - timedelta(days=1)).replace(day=1),
                             description='Past monthly event 1 description', charge=1000, automatic=True,
                             validity='monthly')
        Event.objects.create(name='Past_Yearly_event_1',
                             date=today.replace(day=1).replace(month=1, year=today.year - 1),
                             description='Past yearly event 1 description', charge=1000, automatic=True,
                             validity='yearly')
        Event.objects.create(name='Weekly_event_1', date=today - timedelta(days=today.isoweekday() % 7),
                             description='Weekly event 1 description', charge=1000, automatic=True, validity='weekly')
        Event.objects.create(name='Monthly_event_1', date=today.replace(day=1),
                             description='Monthly event 1 description', charge=1000, automatic=True, validity='monthly')
        Event.objects.create(name='Yearly_event_1', date=today.replace(day=1, month=1),
                             description='Yearly event 1 description', charge=1000, automatic=True, validity='yearly')
        Event.objects.create(name='Post_Weekly_event_1',
                             date=today - timedelta(days=today.isoweekday() % 7) + timedelta(days=7),
                             description='Post weekly event 1 description', charge=1000, automatic=True,
                             validity='weekly')
        Event.objects.create(name='Post_Monthly_event_1',
                             date=today.replace(day=1, month=today.month + 1),
                             description='Post monthly event 1 description', charge=1000, automatic=True,
                             validity='monthly')
        Event.objects.create(name='Post_Yearly_event_1',
                             date=today.replace(day=1, month=1, year=today.year + 1),
                             description='Post yearly event 1 description', charge=1000, automatic=True,
                             validity='yearly')

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('create-partner'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/partners/create/')

    def test_logged_in_forbiden_resource(self):
        self.client.login(username='user', password='password_1')
        response = self.client.get(reverse('create-partner'))
        self.assertEqual(response.status_code, 403)

    def test_authorized_user_get_correct_template(self):
        self.client.login(username='staff_user', password='password_1')
        response = self.client.get(reverse('create-partner'))
        self.assertEqual(str(response.context['user']), 'staff_user')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'partners/partner_form.html')

    def test_proposed_partner_number(self):
        self.client.login(username='staff_user', password='password_1')
        response = self.client.get(reverse('create-partner'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['create'])
        form = response.context['form']
        self.assertEqual(form.initial.get('partner_number'), 10003)

    def test_post_partner_saved(self):
        self.client.login(username='staff_user', password='password_1')
        data = {'address': 'Address_3', 'zip_code': '000003', 'city': City.objects.last().id, 'phone': '55550002',
                'identification': 'identification_1', 'id_number': 10000003, 'social_security': '100000/03',
                'last_name': 'Last_name_3', 'first_name': 'First_name_3 Middle_name_3', 'email': 'last_name_3@mail.com',
                'birthdate': '1960-01-03', 'gender': 'male', 'cellphone': '0015550003', 'partner_number': 10003,
                'incorporation': date.today(), 'position': 'position_1', 'status': 'status_1'}
        response = self.client.post(reverse('create-partner'), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('partners'))
        self.assertEqual(Partner.objects.count(), 3)
        partner = Partner.objects.last()
        self.assertEqual(Share.objects.filter(partner=partner).count(), 6)
        events = (Event.objects.filter(id__in=Share.objects.filter(partner=partner).values_list('event', flat=True)).
                  values_list('name', flat=True))
        self.assertIn('Yearly_event_1', events)
        self.assertIn('Monthly_event_1', events)
        self.assertIn('Weekly_event_1', events)
        self.assertIn('Post_Yearly_event_1', events)
        self.assertIn('Post_Monthly_event_1', events)
        self.assertIn('Post_Weekly_event_1', events)


class PartnerUpdateTest(TestCase):
    @classmethod
    def setUpTestData(cls):
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
        partner_1 = Partner.objects.create(person=person_1, partner_number=10001, incorporation='2026-01-01',
                                           position='psition_1', status='status_1')
        partner_2 = Partner.objects.create(person=person_2, partner_number=10002, incorporation='2026-01-02',
                                           position='psition_1', status='status_1')
        staff_user = User.objects.create_user(name='staff_user', partner=partner_1, password='password_1')
        User.objects.create_user(name='user', partner=partner_2, password='password_1')
        permission = Permission.objects.get(codename='change_partner')
        staff_user.user_permissions.add(permission)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('update-partner', args=[Partner.objects.last().id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/accounts/login/?next=/partners/update/{Partner.objects.last().id}')

    def test_logged_in_forbiden_resource(self):
        self.client.login(username='user', password='password_1')
        response = self.client.get(reverse('update-partner', args=[Partner.objects.last().id]))
        self.assertEqual(response.status_code, 403)

    def test_logged_in_user_get_correct_template(self):
        self.client.login(username='staff_user', password='password_1')
        response = self.client.get(reverse('update-partner', args=[Partner.objects.last().id]))
        self.assertEqual(str(response.context['user']), 'staff_user')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'partners/partner_form.html')

    def test_correct_instance(self):
        self.client.login(username='staff_user', password='password_1')
        url = reverse('update-partner', kwargs={'pk': Partner.objects.last().id})
        response = self.client.get(url)
        form = response.context['form']
        self.assertFalse(response.context['create'])
        self.assertEqual(form.fields['partner_number'].initial, Partner.objects.last().partner_number)


class PartnersListviewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        country = Country.objects.create(name='Country_1')
        state = State.objects.create(name='State_1', country=country)
        city = City.objects.create(name='City_1', state=state)
        for index in range(15):
            suffix = f'{index:02d}'
            address = Address.objects.create(address='Address_' + suffix, zip_code='000001', city=city,
                                             phone='555500' + suffix)
            person = Person.objects.create(identification='identification_1', id_number=100000 + index,
                                           social_security='100000/' + suffix, last_name='Last_name_' + suffix,
                                           first_name='First_name_' + suffix + ' Middle_name_' + suffix,
                                           email='last_name_' + suffix + '@mail.com', birthdate='1960-01-01',
                                           gender='male', address=address, cellphone='00155500' + suffix)
            partner = Partner.objects.create(person=person, partner_number=10000 + index, incorporation=date.today(),
                                             position='position_1', status='status_1')
            User.objects.create_user(name='user_' + suffix, partner=partner, password='password_' + suffix)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('partners'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/partners/')

    def test_view_url_exists_at_desired_location(self):
        self.client.login(username='user_00', password='password_00')
        response = self.client.get('/partners/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.login(username='user_00', password='password_00')
        response = self.client.get(reverse('partners'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(username='user_00', password='password_00')
        response = self.client.get(reverse('partners'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'partners/partner_list.html')

    def test_pagination_is_ten(self):
        self.client.login(username='user_00', password='password_00')
        response = self.client.get(reverse('partners'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'])
        self.assertEqual(len(response.context['partner_list']), 10)

    def test_lists_all_partners(self):
        self.client.login(username='user_00', password='password_00')
        response = self.client.get(reverse('partners') + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'])
        self.assertEqual(len(response.context['partner_list']), 5)

    def test_list_only_searched_partners_by_name(self):
        self.client.login(username='user_00', password='password_00')
        response = self.client.get(reverse('partners') + '?search_data=name_01')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['partner_list']), 1)
        partner = response.context['partner_list'][0]
        self.assertEqual(partner.partner_number, 10001)

    def test_list_only_searched_partners_by_number(self):
        self.client.login(username='user_00', password='password_00')
        response = self.client.get(reverse('partners') + '?search_data=10001')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['partner_list']), 1)
        partner = response.context['partner_list'][0]
        self.assertEqual(partner.person.last_name, 'Last_name_01')


class PartnersDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
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
        partner_1 = Partner.objects.create(person=person_1, partner_number=10001, incorporation='2026-01-01',
                                           position='psition_1', status='status_1')
        partner_2 = Partner.objects.create(person=person_2, partner_number=10002, incorporation='2026-01-02',
                                           position='psition_1', status='status_1')
        staff_user = User.objects.create_user(name='staff_user', partner=partner_1, password='password_1')
        User.objects.create_user(name='user', partner=partner_2, password='password_1')
        permission = Permission.objects.get(codename='view_partner')
        staff_user.user_permissions.add(permission)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('partner-detail', args=[1]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/partner/1')

    def test_logged_in_forbiden_resource(self):
        self.client.login(username='user', password='password_1')
        response = self.client.get(reverse('partner-detail', args=[1]))
        self.assertEqual(response.status_code, 403)

    def test_logged_in_user_get_correct_template(self):
        self.client.login(username='staff_user', password='password_1')
        response = self.client.get(reverse('partner-detail', args=[Partner.objects.last().id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.context['user']), 'staff_user')
        self.assertTemplateUsed(response, 'partners/partner_detail.html')


class PersonDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
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
        partner_1 = Partner.objects.create(person=person_1, partner_number=10001, incorporation='2026-01-01',
                                           position='psition_1', status='status_1')
        partner_2 = Partner.objects.create(person=person_2, partner_number=10002, incorporation='2026-01-02',
                                           position='psition_1', status='status_1')
        staff_user = User.objects.create_user(name='staff_user', partner=partner_1, password='password_1')
        User.objects.create_user(name='user', partner=partner_2, password='password_1')
        permission = Permission.objects.get(codename='view_person')
        staff_user.user_permissions.add(permission)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('person-detail', args=[1]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/person/1')

    def test_logged_in_forbiden_resource(self):
        self.client.login(username='user', password='password_1')
        response = self.client.get(reverse('person-detail', args=[Person.objects.last().id]))
        self.assertEqual(response.status_code, 403)

    def test_logged_in_user_get_correct_template(self):
        self.client.login(username='staff_user', password='password_1')
        response = self.client.get(reverse('person-detail', args=[Person.objects.last().id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.context['user']), 'staff_user')
        self.assertTemplateUsed(response, 'partners/person_detail.html')
