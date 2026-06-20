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

from django.contrib.auth.forms import PasswordResetForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import User
from partners.models import Partner
from django import forms


class CustomPasswordResetForm(PasswordResetForm):
    def get_users(self, email):
        users = User.objects.filter(partner__person__email=email, is_active=True)
        return list(users)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(partner__person__email=email, is_active=True).exists():
            raise ValidationError(_("This email is not registered."))
        return email


class UserForm(forms.Form):
    name = forms.CharField(label=_('Name'))
    partner = forms.ModelChoiceField(label=_('Partner'), queryset=Partner.objects.exclude(status='status_3'))
    is_active = forms.BooleanField(label=_('Active'), initial=True, required=False)
    is_staff = forms.BooleanField(label=_('Staff'), required=False)

    def __init__(self, *args, **kwargs):
        instance = kwargs.pop('instance', None)
        super().__init__(*args, **kwargs)
        if instance:
            self.fields['name'].initial = instance.name
            partners_to_exclude = User.objects.exclude(partner_id=None).exclude(partner_id=instance.partner.id).values_list('partner_id', flat=True)
            self.fields['partner'].queryset = Partner.objects.exclude(status='status_3').exclude(id__in=partners_to_exclude)
            self.fields['partner'].initial = instance.partner
            self.fields['is_active'].initial = instance.is_active
            self.fields['is_staff'].initial = instance.is_staff
        else:
            partners_to_exclude = User.objects.exclude(partner_id=None).values_list('partner_id', flat=True)
            self.fields['partner'].queryset = Partner.objects.exclude(status='status_3').exclude(id__in=partners_to_exclude)

    def clean_name(self):
        data = self.cleaned_data['name']
        if len(data) < 5 or len(data) > 30:
            raise ValidationError(_('The name must be between 5 and 30 characters long.'))
        return data
