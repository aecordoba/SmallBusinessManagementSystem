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
from datetime import date, timedelta, time, datetime
from django.contrib.auth.models import Permission
from django.test import TestCase
from django.urls import reverse
from events.models import Event, News, Share
from partners.models import Country, State, City, Address, Person, Partner
from users.models import User


class EventCreationTest(TestCase):
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
        permission = Permission.objects.get(codename='add_event')
        staff_user.user_permissions.add(permission)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('create-event'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/events/create/')

    def test_logged_in_forbiden_resource(self):
        self.client.login(username='user', password='password_1')
        response = self.client.get(reverse('create-event'))
        self.assertEqual(response.status_code, 403)

    def test_logged_in_user_get_correct_template(self):
        self.client.login(username='staff_user', password='password_1')
        response = self.client.get(reverse('create-event'))
        self.assertEqual(str(response.context['user']), 'staff_user')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/create_event.html')

    def test_post_event_saved(self):
        self.client.login(username='staff_user', password='password_1')
        data = {'name': 'Name_1', 'date': date.today() + timedelta(days=15), 'description': 'Description_1',
                'charge': 5000, 'automatic': True, 'validity': 'monthly'}
        response = self.client.post(reverse('create-event'), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('events'))
        self.assertEqual(Event.objects.count(), 1)
        event = Event.objects.last()
        self.assertEqual(event.name, 'Name_1')


class NewsCreationTest(TestCase):
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
        permission = Permission.objects.get(codename='add_news')
        staff_user.user_permissions.add(permission)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('create-news'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/events/news/create/')

    def test_logged_in_forbiden_resource(self):
        self.client.login(username='user', password='password_1')
        response = self.client.get(reverse('create-news'))
        self.assertEqual(response.status_code, 403)

    def test_logged_in_user_get_correct_template(self):
        self.client.login(username='staff_user', password='password_1')
        response = self.client.get(reverse('create-news'))
        self.assertEqual(str(response.context['user']), 'staff_user')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/create_news.html')

    def test_post_news_saved(self):
        self.client.login(username='staff_user', password='password_1')
        event = Event.objects.create(name='Name_1', date=date.today() + timedelta(days=15), description='Description_1',
                                     automatic=False, time=time(10, 30), attendants=30, charge=15000)
        data = {'event': event.id, 'brief': 'Brief_1', 'description': 'Description_1'}
        response = self.client.post(reverse('create-news'), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('news'))
        self.assertEqual(News.objects.count(), 1)
        news = News.objects.last()
        self.assertEqual(news.brief, 'Brief_1')


class EventAttendTest(TestCase):
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
        partner = Partner.objects.create(person=person, partner_number=10001, incorporation='2026-01-01',
                                         position='position_1', status='status_1')
        User.objects.create_user(name='user', partner=partner, password='password_1')
        Event.objects.create(name='Name_1', date=date.today() + timedelta(days=15), description='Description_1',
                             automatic=False, time=time(10, 30), attendants=30, charge=15000)

    def test_redirect_if_not_logged_in(self):
        response = self.client.post(reverse('event-attend'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/events/attend/')

    def test_post_attend_saved(self):
        self.client.login(username='user', password='password_1')
        event = Event.objects.last()
        data = {'event_pk': event.id, 'user': 'user', 'attendees': 3}
        response = self.client.post(reverse('event-attend'), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('events-attendance-list'))
        share = Share.objects.last()
        self.assertEqual(share.attendees, 3)
        self.assertEqual(share.payment, 0)


class AllocatePaymentTest(TestCase):
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
        permission_codenames = ['add_share', 'change_share', 'delete_share']
        permission = Permission.objects.filter(codename__in=permission_codenames)
        staff_user.user_permissions.add(*permission)
        # Event
        event = Event.objects.create(name='Name_1', date=date.today() + timedelta(days=15), description='Description_1',
                                     automatic=False, time=time(10, 30), attendants=30, charge=15000)
        # Share
        Share.objects.create(event=event, partner=partner_2, attendees=3)

    def test_redirect_if_not_logged_in(self):
        response = self.client.post(reverse('allocate-payment'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/events/payment/')

    def test_logged_in_forbiden_resource(self):
        self.client.login(username='user', password='password_1')
        response = self.client.get(reverse('allocate-payment'))
        self.assertEqual(response.status_code, 403)

    def test_post_payment_saved(self):
        self.client.login(username='staff_user', password='password_1')
        event = Event.objects.last()
        partner = Partner.objects.last()
        data = {'event_pk': event.id, 'partner_pk': partner.id, 'pay': 30000}
        response = self.client.post(reverse('allocate-payment'), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('partner-attendance-list', kwargs={'pk': partner.id}))
        share = Share.objects.last()
        self.assertEqual(share.payment, 30000)


class RemoveAttendanceTest(TestCase):
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
        permission_codenames = ['add_share', 'change_share', 'delete_share']
        permission = Permission.objects.filter(codename__in=permission_codenames)
        staff_user.user_permissions.add(*permission)
        # Event
        event = Event.objects.create(name='Name_1', date=date.today() + timedelta(days=15), description='Description_1',
                                     automatic=False, time=time(10, 30), attendants=30, charge=15000)
        # Share
        Share.objects.create(event=event, partner=partner_2, attendees=3)

    def test_redirect_if_not_logged_in(self):
        response = self.client.post(reverse('remove-attendance'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/events/attendance/')

    def test_logged_in_forbiden_resource(self):
        self.client.login(username='user', password='password_1')
        response = self.client.get(reverse('remove-attendance'))
        self.assertEqual(response.status_code, 403)

    def test_post_remove_saved(self):
        self.client.login(username='staff_user', password='password_1')
        event = Event.objects.last()
        partner = Partner.objects.last()
        data = {'event_pk': event.id, 'partner_pk': partner.id}
        response = self.client.post(reverse('remove-attendance'), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('partner-attendance-list', kwargs={'pk': partner.id}))
        share_count = Share.objects.all().count()
        self.assertEqual(share_count, 0)


class AddSharingTest(TestCase):
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
        permission_codenames = ['add_share', 'change_share', 'delete_share']
        permission = Permission.objects.filter(codename__in=permission_codenames)
        staff_user.user_permissions.add(*permission)
        # Event
        Event.objects.create(name='Name_1', date=date.today() + timedelta(days=15), description='Description_1',
                             automatic=False, time=time(10, 30), attendants=30, charge=15000)

    def test_redirect_if_not_logged_in(self):
        response = self.client.post(reverse('add-sharing'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/events/sharing/')

    def test_logged_in_forbiden_resource(self):
        self.client.login(username='user', password='password_1')
        response = self.client.get(reverse('add-sharing'))
        self.assertEqual(response.status_code, 403)

    def test_post_sharing_saved(self):
        self.client.login(username='staff_user', password='password_1')
        event = Event.objects.last()
        partner = Partner.objects.last()
        data = {'event_pk': event.id, 'partner_pk': partner.id, 'attendees': 3, 'pay': 30000}
        response = self.client.post(reverse('add-sharing'), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('partner-attendance-list', kwargs={'pk': partner.id}))
        share = Share.objects.get(partner=partner, event=event)
        self.assertEqual(share.attendees, 3)
        self.assertEqual(share.payment, 30000)


class NewsListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.news_quantity = 8
        for news_ix in range(cls.news_quantity):
            News.objects.create(edition=datetime.now() - timedelta(days=news_ix),
                                brief=f'News_{news_ix}', description=f'News_{news_ix} description.')
        past_event = Event.objects.create(name='Past event', date=date.today() - timedelta(days=1),
                                          description='Description_1', automatic=False, time=time(10, 30),
                                          attendants=30, charge=15000)
        future_event = Event.objects.create(name='Future event', date=date.today() + timedelta(days=1),
                                            description='Description_2', automatic=False, time=time(10, 30),
                                            attendants=15, charge=19000)
        News.objects.create(event=past_event, edition=datetime.now() - timedelta(days=10), brief='News_Past_event',
                            description='News_Past_event description.')
        News.objects.create(event=future_event, edition=datetime.now() - timedelta(days=10), brief='News_Future_event',
                            description='News_Future_event description.')

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/events/news/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('news'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('news'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/news_list.html')

    def test_pagination_is_five_and_ordered(self):
        response = self.client.get(reverse('news'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'])
        self.assertEqual(len(response.context['news_list']), 5)
        news_list = [news.brief for news in response.context['news_list']]
        self.assertNotIn('News_Past_event', news_list)
        self.assertIn('News_Future_event', news_list)
        last_edition = None
        for index, news in enumerate(response.context['news_list']):
            if index != 0:
                self.assertTrue(news.edition <= last_edition)
            last_edition = news.edition

    def test_lists_all_news_and_ordered(self):
        response = self.client.get(reverse('news') + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'])
        self.assertEqual(len(response.context['news_list']), 4)
        news_list = [news.brief for news in response.context['news_list']]
        self.assertNotIn('News_Past_event', news_list)
        last_edition = None
        for index, news in enumerate(response.context['news_list']):
            if index != 0:
                self.assertTrue(news.edition <= last_edition)
            last_edition = news.edition


class NewsDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        News.objects.create(edition=datetime.now() + timedelta(days=15), brief='News_1',
                            description='News_1 description.')

    def test__get_correct_template(self):
        response = self.client.get(reverse('news-detail', args=[News.objects.last().id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/news_detail.html')


class EventsListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.events_quantity = 15
        for event_ix in range(cls.events_quantity):
            Event.objects.create(name=f'Event_{event_ix}', date=date.today() + timedelta(days=5 + event_ix),
                                 description=f'Event_{event_ix} description', automatic=False, time=time(10, 30),
                                 attendants=30, charge=1000 * event_ix)

        Event.objects.create(name='Automatic_event', date=date.today() + timedelta(days=5),
                             description='Automatic_event description', automatic=True, time=time(10, 30),
                             validity='monthly', charge=5000)
        Event.objects.create(name='Past_event', date=date.today() - timedelta(days=1),
                             description='Past_event description', automatic=False, time=time(10, 30),
                             attendants=20, charge=15000)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/events/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('events'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('events'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/event_list.html')

    def test_pagination_is_ten_and_ordered(self):
        response = self.client.get(reverse('events'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'])
        self.assertEqual(len(response.context['event_list']), 10)
        events_list = [event.name for event in response.context['event_list']]
        self.assertNotIn('Automatic_event', events_list)
        self.assertNotIn('Past_event', events_list)
        last_date = 0
        for event in response.context['event_list']:
            if last_date != 0:
                self.assertTrue(event.date >= last_date)
            last_date = event.date

    def test_lists_all_events_and_ordered(self):
        response = self.client.get(reverse('events') + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'])
        self.assertEqual(len(response.context['event_list']), 5)
        events_list = [event.name for event in response.context['event_list']]
        self.assertNotIn('Automatic_event', events_list)
        self.assertNotIn('Past_event', events_list)
        last_date = 0
        for event in response.context['event_list']:
            if last_date != 0:
                self.assertTrue(event.date >= last_date)
            last_date = event.date


class EventsAttendanceListViewTest(TestCase):
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
        partner = Partner.objects.create(person=person, partner_number=10001, incorporation='2026-01-01',
                                         position='position_1', status='status_1')
        User.objects.create_user(name='user', partner=partner, password='password_1')
        cls.events_quantity = 12
        for event_ix in range(cls.events_quantity):
            event = Event.objects.create(name=f'Event_{event_ix}', date=date.today() + timedelta(days=5 + event_ix),
                                         description=f'Event_{event_ix} description', automatic=False,
                                         time=time(10, 30), attendants=30, charge=1000 * event_ix)
            Share.objects.create(event=event, partner=partner, attendees=2, payment=500 * event_ix)
        unpaid_event = Event.objects.create(name='Unpaid_past_event', date=date.today() - timedelta(days=5),
                                            description='Unpaid_past_event description', automatic=False,
                                            time=time(10, 30), attendants=30, charge=1000)
        Share.objects.create(event=unpaid_event, partner=partner, attendees=2, payment=500)
        paid_event = Event.objects.create(name='Paid_past_event', date=date.today() - timedelta(days=6),
                                          description='Paid_past_event description', automatic=False,
                                          time=time(10, 30), attendants=30, charge=1000)
        Share.objects.create(event=paid_event, partner=partner, attendees=2, payment=2000)

    def test_redirect_if_not_logged_in(self):
        response = self.client.post(reverse('events-attendance-list'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/events/share/')

    def test_logged_in_user_get_correct_template(self):
        self.client.login(username='user', password='password_1')
        response = self.client.get(reverse('events-attendance-list'))
        self.assertEqual(str(response.context['user']), 'user')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/share_list.html')

    def test_pagination_is_ten_and_ordered(self):
        self.client.login(username='user', password='password_1')
        response = self.client.get(reverse('events-attendance-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['is_paginated'])
        self.assertEqual(len(response.context['share_list']), 10)
        events_list = [share.event.name for share in response.context['share_list']]
        self.assertNotIn('Paid_past_event', events_list)
        self.assertIn('Unpaid_past_event', events_list)
        last_date = 0
        for share in response.context['share_list']:
            if last_date != 0:
                self.assertTrue(share.event.date >= last_date)
            last_date = share.event.date

    def test_lists_all_attendance_and_ordered(self):
        self.client.login(username='user', password='password_1')
        response = self.client.get(reverse('events-attendance-list') + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['is_paginated'])
        self.assertEqual(len(response.context['share_list']), 3)
        events_list = [share.event.name for share in response.context['share_list']]
        self.assertNotIn('Paid_past_event', events_list)
        last_date = 0
        for share in response.context['share_list']:
            if last_date != 0:
                self.assertTrue(share.event.date >= last_date)
            last_date = share.event.date


class EventDetailViewTest(TestCase):
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
        partner = Partner.objects.create(person=person, partner_number=10001, incorporation='2026-01-01',
                                         position='position_1', status='status_1')
        User.objects.create_user(name='user', partner=partner, password='password_1')
        event = Event.objects.create(name='Event_1', date=date.today() + timedelta(days=5),
                                     description='Event_1 description', automatic=False, time=time(10, 30),
                                     attendants=30, charge=15000)
        Share.objects.create(partner=partner, event=event, attendees=2, payment=10000)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('event-detail', args=[Event.objects.last().id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/accounts/login/?next=/events/{Event.objects.last().id}')

    def test_logged_in_user_get_correct_template(self):
        self.client.login(username='user', password='password_1')
        response = self.client.get(reverse('event-detail', args=[Event.objects.last().id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.context['user']), 'user')
        self.assertTemplateUsed(response, 'events/event_detail.html')

    def test_correct_context_data(self):
        self.client.login(username='user', password='password_1')
        response = self.client.get(reverse('event-detail', args=[Event.objects.last().id]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['registered'])
        self.assertTrue(response.context['vacancies'], 28)


class PartnerAttendanceListViewTest(TestCase):
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
        permission_codenames = ['add_share', 'change_share', 'delete_share']
        permission = Permission.objects.filter(codename__in=permission_codenames)
        staff_user.user_permissions.add(*permission)
        User.objects.create_user(name='user', partner=partner_2, password='password_1')
        # Events
        event = Event.objects.create(name='Event', date=date.today() + timedelta(days=5),
                                     description='Event_1 description', automatic=False, time=time(10, 30),
                                     attendants=30, charge=15000)
        automatic_event = Event.objects.create(name='Automatic_event', date=date.today().replace(day=1),
                                               description='Automatic_event description', automatic=True,
                                               validity='monthly', charge=5000)
        paid_event = Event.objects.create(name='Paid_event',
                                          date=date.today().replace(month=date.today().month - 1, day=1),
                                          description='Paid_event description', automatic=True, validity='monthly',
                                          charge=5000)
        # Sharing
        Share.objects.create(partner=partner_2, event=event, attendees=2, payment=10000)
        Share.objects.create(partner=partner_2, event=automatic_event, attendees=1, payment=1000)
        Share.objects.create(partner=partner_2, event=paid_event, attendees=1, payment=50000)

        cls.events_quantity = 12
        for event_ix in range(cls.events_quantity):
            event = Event.objects.create(name=f'Event_{event_ix}', date=date.today() + timedelta(days=5 + event_ix),
                                         description=f'Event_{event_ix} description', automatic=False,
                                         time=time(10, 30), attendants=30, charge=1000 * event_ix + 1)
            Share.objects.create(event=event, partner=partner_2, attendees=2, payment=500 * event_ix + 1)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('partner-attendance-list', args=[Partner.objects.last().id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/accounts/login/?next=/events/share/{Partner.objects.last().id}')

    def test_logged_in_forbiden_resource(self):
        self.client.login(username='user', password='password_1')
        response = self.client.get(reverse('partner-attendance-list', args=[Partner.objects.last().id]))
        self.assertEqual(response.status_code, 403)

    def test_logged_in_user_get_correct_template(self):
        self.client.login(username='staff_user', password='password_1')
        response = self.client.get(reverse('partner-attendance-list', args=[Partner.objects.last().id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.context['user']), 'staff_user')
        self.assertTemplateUsed(response, 'events/partner_attendance_list.html')

    def test_get_correct_events_paginated_and_ordered(self):
        self.client.login(username='staff_user', password='password_1')
        response = self.client.get(reverse('partner-attendance-list', args=[Partner.objects.last().id]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['is_paginated'])
        self.assertEqual(len(response.context['share_list']), 10)
        events_list = [share.event.name for share in response.context['share_list']]
        self.assertNotIn('Paid_event', events_list)
        self.assertIn('Event', events_list)
        self.assertIn('Automatic_event', events_list)
        last_date = 0
        for share in response.context['share_list']:
            if last_date != 0:
                self.assertTrue(share.event.date >= last_date)
            last_date = share.event.date

    def test_lists_all_events_and_ordered(self):
        self.client.login(username='staff_user', password='password_1')
        response = self.client.get(reverse('partner-attendance-list', args=[Partner.objects.last().id]) + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['is_paginated'])
        self.assertEqual(len(response.context['share_list']), 4)
        events_list = [share.event.name for share in response.context['share_list']]
        self.assertNotIn('Paid_event', events_list)
        last_date = 0
        for share in response.context['share_list']:
            if last_date != 0:
                self.assertTrue(share.event.date >= last_date)
            last_date = share.event.date

    def test_correct_debt_for_event_attendance(self):
        self.client.login(username='staff_user', password='password_1')
        response = self.client.get(reverse('partner-attendance-list', args=[Partner.objects.last().id]))
        self.assertEqual(response.status_code, 200)
        events_list = [share.event.name for share in response.context['share_list']]
        self.assertIn('Automatic_event', events_list)
        for share in response.context['share_list']:
            if share.event.name == 'Automatic_event':
                self.assertTrue(share.debt == 4000)
                break


class AttendeesListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Event
        event = Event.objects.create(name='Event', date=date.today() + timedelta(days=5),
                                     description='Event_1 description', automatic=False, time=time(10, 30),
                                     attendants=50, charge=15000)
        # Partners and sharing
        country = Country.objects.create(name='Country_1')
        state = State.objects.create(name='State_1', country=country)
        city = City.objects.create(name='City_1', state=state)
        partner = None
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
            Share.objects.create(partner=partner, event=event, attendees=(index % 2) + 1, payment=(index % 2) * 15000)
        address = Address.objects.create(address='Address_staff', zip_code='000001', city=city,
                                         phone='55551000')
        person_1 = Person.objects.create(identification='identification_1', id_number=10000001,
                                         social_security='100000/99', last_name='Last_name_staff',
                                         first_name='First_name Middle_name',
                                         email='last_name_staff@mail.com', birthdate='1960-01-01', gender='male',
                                         address=address, cellphone='0015551000')
        partner_1 = Partner.objects.create(person=person_1, partner_number=10020, incorporation='2026-01-01',
                                           position='position_1', status='status_1')
        staff_user = User.objects.create_user(name='staff_user', partner=partner_1, password='password_1')
        User.objects.create_user(name='user', partner=partner, password='password_1')
        permission = Permission.objects.get(codename='management')
        staff_user.user_permissions.add(permission)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('list-attendees', args=[Event.objects.last().id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/accounts/login/?next=/events/attendees/{Event.objects.last().id}')

    def test_logged_in_forbiden_resource(self):
        self.client.login(username='user', password='password_1')
        response = self.client.get(reverse('list-attendees', args=[Event.objects.last().id]))
        self.assertEqual(response.status_code, 403)

    def test_logged_in_user_get_correct_template(self):
        self.client.login(username='staff_user', password='password_1')
        response = self.client.get(reverse('list-attendees', args=[Event.objects.last().id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.context['user']), 'staff_user')
        self.assertTemplateUsed(response, 'events/attendees_list.html')

    def test_get_correct_attendees_paginated_and_ordered(self):
        self.client.login(username='staff_user', password='password_1')
        response = self.client.get(reverse('list-attendees', args=[Event.objects.last().id]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['is_paginated'])
        self.assertEqual(len(response.context['attendees_list']), 10)
        partner_numbers_list = [share.partner.partner_number for share in response.context['attendees_list']]
        self.assertNotIn(10020, partner_numbers_list)
        last_partner_number = 0
        for share in response.context['attendees_list']:
            if last_partner_number != 0:
                self.assertTrue(share.partner.partner_number > last_partner_number)
            last_partner_number = share.partner.partner_number

    def test_lists_all_attendees_and_ordered(self):
        self.client.login(username='staff_user', password='password_1')
        response = self.client.get(reverse('list-attendees', args=[Event.objects.last().id]) + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['is_paginated'])
        self.assertEqual(len(response.context['attendees_list']), 5)
        partner_numbers_list = [share.partner.partner_number for share in response.context['attendees_list']]
        self.assertNotIn(10020, partner_numbers_list)
        last_partner_number = 0
        for share in response.context['attendees_list']:
            if last_partner_number != 0:
                self.assertTrue(share.partner.partner_number > last_partner_number)
            last_partner_number = share.partner.partner_number

    def test_correct_debt_for_event_attendee(self):
        self.client.login(username='staff_user', password='password_1')
        response = self.client.get(reverse('list-attendees', args=[Event.objects.last().id]))
        self.assertEqual(response.status_code, 200)
        partner_numbers_list = [share.partner.partner_number for share in response.context['attendees_list']]
        self.assertIn(10001, partner_numbers_list)
        for share in response.context['attendees_list']:
            if share.partner.partner_number == 10001:
                self.assertTrue(share.debt == 15000)
                break


class PartnerSharingListViewTest(TestCase):
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
        permission = Permission.objects.get(codename='add_share')
        staff_user.user_permissions.add(permission)
        # Events and sharing
        registered_event = Event.objects.create(name='Event_registered', date=date.today() + timedelta(days=20),
                                                description='Event_registered description', automatic=False,
                                                time=time(10, 30), attendants=30, charge=25000)
        Share.objects.create(event=registered_event, partner=partner_2, attendees=2, payment=500)
        full_event = Event.objects.create(name='Event_full', date=date.today() + timedelta(days=2),
                                          description='Event_full description', automatic=False, time=time(10, 30),
                                          attendants=15, charge=25000)
        Share.objects.create(event=full_event, partner=partner_1, attendees=15, payment=500)
        Event.objects.create(name='Automatic_event', date=date.today().replace(day=1),
                             description='Automatic_event description', automatic=True, validity='monthly', charge=5000)
        cls.events_quantity = 12
        for event_ix in range(cls.events_quantity):
            event = Event.objects.create(name=f'Event_{event_ix}', date=date.today() + timedelta(days=5 + event_ix),
                                         description=f'Event_{event_ix} description', automatic=False,
                                         time=time(10, 30), attendants=30, charge=1000 * event_ix)
            Share.objects.create(event=event, partner=partner_1, attendees=2, payment=500 * event_ix)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('partner-sharing', args=[Partner.objects.last().id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/accounts/login/?next=/events/share/partner/{Partner.objects.last().id}')

    def test_logged_in_forbiden_resource(self):
        self.client.login(username='user', password='password_1')
        response = self.client.get(reverse('partner-sharing', args=[Partner.objects.last().id]))
        self.assertEqual(response.status_code, 403)

    def test_logged_in_user_get_correct_template(self):
        self.client.login(username='staff_user', password='password_1')
        response = self.client.get(reverse('partner-sharing', args=[Partner.objects.last().id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.context['user']), 'staff_user')
        self.assertTemplateUsed(response, 'events/partner_sharing_list.html')

    def test_get_correct_events_paginated_and_ordered(self):
        self.client.login(username='staff_user', password='password_1')
        response = self.client.get(reverse('partner-sharing', args=[Partner.objects.last().id]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['is_paginated'])
        self.assertEqual(len(response.context['events_list']), 10)
        event_names_list = [event.name for event in response.context['events_list']]
        self.assertIn('Event_full', event_names_list)
        self.assertNotIn('Event_registerd', event_names_list)
        self.assertNotIn('Automatic_event', event_names_list)
        last_date = 0
        for event in response.context['events_list']:
            if last_date != 0:
                self.assertTrue(event.date > last_date)
            last_date = event.date

    def test_lists_all_events_and_ordered(self):
        self.client.login(username='staff_user', password='password_1')
        response = self.client.get(reverse('partner-sharing', args=[Partner.objects.last().id]) + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['is_paginated'])
        self.assertEqual(len(response.context['events_list']), 3)
        event_names_list = [event.name for event in response.context['events_list']]
        self.assertNotIn('Event_registerd', event_names_list)
        self.assertNotIn('Automatic_event', event_names_list)
        last_date = 0
        for event in response.context['events_list']:
            if last_date != 0:
                self.assertTrue(event.date > last_date)
            last_date = event.date

    def test_correct_vacancies_for_event(self):
        self.client.login(username='staff_user', password='password_1')
        response = self.client.get(reverse('partner-sharing', args=[Partner.objects.last().id]) + '?page=2')
        self.assertEqual(response.status_code, 200)
        event_names_list = [event.name for event in response.context['events_list']]
        self.assertNotIn('Event_1', event_names_list)
        for event in response.context['events_list']:
            if event.name == 'Event_1':
                self.assertTrue(event.vacancies == 28)
                break
