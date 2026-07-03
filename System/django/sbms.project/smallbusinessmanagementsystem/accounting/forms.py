#  		forms.py			Jun 20, 2026
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

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class AddAccountingForm(forms.Form):
    date = forms.DateField(label=_('Date'), widget=forms.DateInput(attrs={'type': 'date'}), localize=True)
    concept = forms.CharField(label=_('Concept'))
    description = forms.CharField(label=_('Description'), widget=forms.Textarea(attrs={'rows': 5, 'cols': 40}))
    debit = forms.DecimalField(label=_('Debit'), max_digits=15, decimal_places=2, localize=True, required=False)
    credit = forms.DecimalField(label=_('Credit'), max_digits=15, decimal_places=2, localize=True, required=False)

    def clean_date(self):
        data = self.cleaned_data['date']
        if data is None:
            raise ValidationError(_('Set a date.'))
        return data

    def clean_concept(self):
        data = self.cleaned_data['concept']
        if len(data) < 5 or len(data) > 30:
            raise ValidationError(_('The concept must be between 5 and 30 characters long.'))
        return data

    def clean_description(self):
        data = self.cleaned_data['description']
        if len(data) < 10 or len(data) > 100:
            raise ValidationError(_('The description must be between 10 and 100 characters long.'))
        return data

    def clean(self):
        cleaned_data = super().clean()
        debit = cleaned_data.get('debit')
        credut = cleaned_data.get('credit')
        if debit and credut:
            raise ValidationError({'debit': _('Debit and credit cannot be specified simultaneously.')})
        elif not debit and not credut:
            raise ValidationError({'debit': _('Debit and credit cannot be empty simultaneously.')})
        return cleaned_data
