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
from accounting.forms import AddAccountingForm
import random
import string


def generate_random_string(lenght):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=lenght))


class AddAccountFormTest(SimpleTestCase):
    def test_date_label(self):
        form = AddAccountingForm()
        self.assertEqual(form.fields['date'].label, 'Date')

    def test_concept_label(self):
        form = AddAccountingForm()
        self.assertEqual(form.fields['concept'].label, 'Concept')

    def test_description_label(self):
        form = AddAccountingForm()
        self.assertEqual(form.fields['description'].label, 'Description')

    def test_debit_label(self):
        form = AddAccountingForm()
        self.assertEqual(form.fields['debit'].label, 'Debit')

    def test_credit_label(self):
        form = AddAccountingForm()
        self.assertEqual(form.fields['credit'].label, 'Credit')

    def test_empty_date(self):
        data = {'date': '', 'concept': 'Concept_1', 'description': 'Description_1', 'debit': 10000, 'credit': ''}
        form = AddAccountingForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn('date', form.errors)
        self.assertEqual(form.errors['date'], ['This field is required.'])

    def test_concept_min_lenght(self):
        data = {'date': '2026-01-01', 'concept': 'Conc', 'description': 'Description_1', 'debit': 10000, 'credit': ''}
        form = AddAccountingForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn('concept', form.errors)
        self.assertEqual(form.errors['concept'], ['The concept must be between 5 and 30 characters long.'])

    def test_concept_max_lenght(self):
        data = {'date': '2026-01-01', 'concept': generate_random_string(31), 'description': 'Description_1',
                'debit': 10000, 'credit': ''}
        form = AddAccountingForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn('concept', form.errors)
        self.assertEqual(form.errors['concept'], ['The concept must be between 5 and 30 characters long.'])

    def test_description_min_lenght(self):
        data = {'date': '2026-01-01', 'concept': 'Concept_1', 'description': 'Descripti', 'debit': 10000, 'credit': ''}
        form = AddAccountingForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn('description', form.errors)
        self.assertEqual(form.errors['description'], ['The description must be between 10 and 100 characters long.'])

    def test_description_max_lenght(self):
        data = {'date': '2026-01-01', 'concept': 'Concept_1', 'description': generate_random_string(101),
                'debit': 10000, 'credit': ''}
        form = AddAccountingForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn('description', form.errors)
        self.assertEqual(form.errors['description'], ['The description must be between 10 and 100 characters long.'])

    def test_debit_and_credit_simultaneous(self):
        data = {'date': '2026-01-01', 'concept': 'Concept_1', 'description': 'Description_1', 'debit': 10000,
                'credit': 10000}
        form = AddAccountingForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn('debit', form.errors)
        self.assertEqual(form.errors['debit'], ['Debit and credit cannot be specified simultaneously.'])

    def test_debit_and_credit_empty(self):
        data = {'date': '2026-01-01', 'concept': 'Concept_1', 'description': 'Description_1', 'debit': '',
                'credit': ''}
        form = AddAccountingForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn('debit', form.errors)
        self.assertEqual(form.errors['debit'], ['Debit and credit cannot be empty simultaneously.'])
