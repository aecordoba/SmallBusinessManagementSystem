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

from events.models import Event, News, Share
from partners.models import Partner, Country, State, City, Address, Person


class EventModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        event = Event.objects.create(name='Event_1', date='2026-01-01', time='01:00', attendants=50,
                                     description='Event_1 description.', charge=10.25, automatic=False)

        country = Country.objects.create(name='Country_1')
        state = State.objects.create(name='State_1', country=country)
        city = City.objects.create(name='City_1', state=state)
        address = Address.objects.create(address='Address_1', zip_code='000001', city=city, phone='55550001')
        person = Person.objects.create(identification='identification_1', id_number=10000001, social_security='100000/01',
                                       last_name='Last_name_1', first_name='First_Name_1 Middle_Name_1',
                                       email='last_name_1@mail.com', birthdate='1960-01-01', gender='male',
                                       address=address, cellphone='0015550001')
        partner = Partner.objects.create(person=person, partner_number=10001, incorporation='2026-01-01',
                                         position='psition_1', status='status_1')

        Share.objects.create(event=event, partner=partner, attendees=1, payment=0.0)

        News.objects.create(event=event, brief='News_1', description='News_1 description.', )

    def test_event_name_max_length(self):
        event = Event.objects.get(id=1)
        max_length = event._meta.get_field('name').max_length
        self.assertEqual(max_length, 30)

    def test_event_charge_max_digits(self):
        event = Event.objects.get(id=1)
        max_digits = event._meta.get_field('charge').max_digits
        self.assertEqual(max_digits, 10)

    def test_event_validity_max_length(self):
        event = Event.objects.get(id=1)
        max_length = event._meta.get_field('validity').max_length
        self.assertEqual(max_length, 15)

    def test_share_attendees_default(self):
        share = Share.objects.get(id=1)
        default = share._meta.get_field('attendees').default
        self.assertEqual(default, 1)

    def test_share_payment_max_digits(self):
        share = Share.objects.get(id=1)
        max_digits = share._meta.get_field('payment').max_digits
        self.assertEqual(max_digits, 10)

    def test_event_str(self):
        event = Event.objects.get(id=1)
        expected_str = event.name
        self.assertEqual(str(event), expected_str)

    def test_news_str(self):
        news = News.objects.get(id=1)
        expected_str = str(news.edition) + ' - ' + news.brief
        self.assertEqual(str(news), expected_str)

    def test_event_get_absolute_url(self):
        event = Event.objects.get(id=1)
        self.assertEqual(event.get_absolute_url(), '/events/1')

    def test_news_get_absolute_url(self):
        news = News.objects.get(id=1)
        self.assertEqual(news.get_absolute_url(), '/events/news/1')
