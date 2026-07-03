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

from django.test import SimpleTestCase
from events.forms import CreateEventForm, CreateNewsForm
import random
import string


def generate_random_string(lenght):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=lenght))


class CreateEventFormTest(SimpleTestCase):
    def test_name_label(self):
        form = CreateEventForm()
        self.assertEqual(form.fields['name'].label, 'Name')

    def test_automatic_label(self):
        form = CreateEventForm()
        self.assertEqual(form.fields['automatic'].label, 'Automatic')

    def test_date_label(self):
        form = CreateEventForm()
        self.assertEqual(form.fields['date'].label, 'Date')

    def test_time_label(self):
        form = CreateEventForm()
        self.assertEqual(form.fields['time'].label, 'Time')

    def test_attendants_label(self):
        form = CreateEventForm()
        self.assertEqual(form.fields['attendants'].label, 'Attendants')

    def test_description_label(self):
        form = CreateEventForm()
        self.assertEqual(form.fields['description'].label, 'Description')

    def test_charge_label(self):
        form = CreateEventForm()
        self.assertEqual(form.fields['charge'].label, 'Charge')

    def test_validitylabel(self):
        form = CreateEventForm()
        self.assertEqual(form.fields['validity'].label, 'Validity')

    def test_name_min_lenght(self):
        data = {'name': 'Name', 'automatic': False, 'date': '2026-01-01', 'time': '00:00', 'attendants': 100,
                'description': 'Description_1', 'charge': 10000}
        form = CreateEventForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
        self.assertEqual(form.errors['name'], ['The name must be between 5 and 30 characters long.'])

    def test_name_max_lenght(self):
        data = {'name': generate_random_string(31), 'automatic': False, 'date': '2026-01-01', 'time': '00:00',
                'attendants': 100, 'description': 'Description_1', 'charge': 10000}
        form = CreateEventForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
        self.assertEqual(form.errors['name'], ['The name must be between 5 and 30 characters long.'])

    def test_empty_date(self):
        data = {'name': 'Name_1', 'automatic': False, 'date': '', 'time': '00:00', 'attendants': 100,
                'description': 'Description_1', 'charge': 10000}
        form = CreateEventForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn('date', form.errors)
        self.assertEqual(form.errors['date'], ['This field is required.'])

    def test_empty_charge_in_automatic_event(self):
        data = {'name': 'Name_1', 'automatic': True, 'date': '2026-01-01', 'description': 'Description_1', 'charge': ''}
        form = CreateEventForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn('charge', form.errors)
        self.assertEqual(form.errors['charge'], ['Automated events must have a charge.'])


class CreateNewsFormTest(SimpleTestCase):
    def test_event_label(self):
        form = CreateNewsForm()
        self.assertEqual(form.fields['event'].label, 'Event')

    def test_brief_label(self):
        form = CreateNewsForm()
        self.assertEqual(form.fields['brief'].label, 'Header')

    def test_description_label(self):
        form = CreateNewsForm()
        self.assertEqual(form.fields['description'].label, 'Description')

    def test_brief_min_lenght(self):
        data = {'brief': 'Brie', 'description': 'Description_1'}
        form = CreateNewsForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn('brief', form.errors)
        self.assertEqual(form.errors['brief'], ['You must enter a header.'])
