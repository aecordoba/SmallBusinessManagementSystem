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
from .models import Person, City, Partner
from datetime import date


class PartnerForm(forms.Form):
    partner_number = forms.IntegerField(label=_('Partner number'))
    first_name = forms.CharField(label=_('First name'))
    last_name = forms.CharField(label=_('Last name'))
    doc_type = forms.ChoiceField(label=_('Document'), choices=Person.DOCUMENTS)
    doc_number = forms.IntegerField(label=_('Number'))
    social_security = forms.CharField(label=_('Social Security'))
    email = forms.EmailField(label=_('E-mail'))
    birthdate = forms.DateField(label=_('Birthdate'), widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}), localize=True)
    gender = forms.ChoiceField(label=_('Gender'), choices=Person.GENDERS)
    address = forms.CharField(label=_('Address'))
    zip_code = forms.CharField(label=_('ZIP Code'))
    city = forms.ModelChoiceField(queryset=City.objects.all(), widget=forms.Select(attrs={'style': 'width: 300px;'}))
    phone = forms.CharField(label=_('Phone number'), required=False)
    cellphone = forms.CharField(label=_('Cell phone number'), required=False)
    incorporation = forms.DateField(label=_('Incorporation'), widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}), localize=True)
    position = forms.ChoiceField(label=_('Position'), choices=Partner.POSITIONS)
    status = forms.ChoiceField(label=_('Status'), choices=Partner.STATUS)

    def __init__(self, *args, **kwargs):
        instance = kwargs.pop('instance', None)
        super().__init__(*args, **kwargs)
        if instance:
            self.fields['partner_number'].initial = instance.partner_number
            self.fields['first_name'].initial = instance.person.first_name
            self.fields['last_name'].initial = instance.person.last_name
            self.fields['doc_type'].initial = instance.person.doc_type
            self.fields['doc_number'].initial = instance.person.doc_number
            self.fields['social_security'].initial = instance.person.social_security
            self.fields['email'].initial = instance.person.email
            self.fields['birthdate'].localize = True
            self.fields['birthdate'].initial = instance.person.birthdate
            self.fields['gender'].initial = instance.person.gender
            self.fields['address'].initial = instance.person.address.address
            self.fields['zip_code'].initial = instance.person.address.zip_code
            self.fields['city'].initial = instance.person.address.city
            self.fields['phone'].initial = instance.person.address.phone
            self.fields['cellphone'].initial = instance.person.cellphone
            self.fields['incorporation'].localize = True
            self.fields['incorporation'].initial = instance.incorporation
            self.fields['position'].initial = instance.position
            self.fields['status'].initial = instance.status

    def clean_first_name(self):
        data = self.cleaned_data['first_name']
        if len(data) < 2 or len(data) > 30:
            raise ValidationError(_('The first name must be between 2 and 30 characters long.'))
        return data

    def clean_last_name(self):
        data = self.cleaned_data['last_name']
        if len(data) < 2 or len(data) > 30:
            raise ValidationError(_('The last name must be between 2 and 30 characters long.'))
        return data

    def clean_doc_number(self):
        data = self.cleaned_data['doc_number']
        if data < 1000000:
            raise ValidationError(_('Incorrect ID number.'))
        return data

    def clean_social_security(self):
        data = self.cleaned_data['social_security']
        if len(data) > 15:
            raise ValidationError(_('The social security number must be up to 15 characters long.'))
        return data

    def clean_birthdate(self):
        data = self.cleaned_data['birthdate']
        if data > date.today():
            raise ValidationError(_('Incorrect birthdate.'))
        return data

    def clean_address(self):
        data = self.cleaned_data['address']
        if len(data) < 5 or len(data) > 30:
            raise ValidationError(_('The address must be between 5 and 30 characters long.'))
        return data

    def clean_phone(self):
        data = self.cleaned_data['phone']
        if len(data) > 0 and len(data) < 8 or len(data) > 10:
            raise ValidationError(_('The phone number must be between 8 and 10 digits long (without hyphens).'))
        return data

    def clean_cellphone(self):
        data = self.cleaned_data['cellphone']
        if len(data) > 0 and len(data) < 8 or len(data) > 10:
            raise ValidationError(_('The cell phone number must be between 8 and 10 digits long (without hyphens).'))
        return data

