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
from accounting.models import Accounting


class AccountingModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Accounting.objects.create(date='2026-01-01', concept='Accounting_1', description='Accounting_1 description',
                                  credit=100000.01)

    def test_concept_max_length(self):
        accounting = Accounting.objects.get(id=1)
        max_length = accounting._meta.get_field('concept').max_length
        self.assertEqual(max_length, 30)

    def test_debit_max_digits(self):
        accounting = Accounting.objects.get(id=1)
        max_digits = accounting._meta.get_field('debit').max_digits
        self.assertEqual(max_digits, 15)

    def test_credit_max_digits(self):
        accounting = Accounting.objects.get(id=1)
        max_digits = accounting._meta.get_field('credit').max_digits
        self.assertEqual(max_digits, 15)

    def test_accounting_str(self):
        accounting = Accounting.objects.get(id=1)
        expected_str = str(accounting.date) + ' ' + accounting.concept
        self.assertEqual(str(accounting), expected_str)
